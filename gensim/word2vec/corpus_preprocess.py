# -*- coding:utf-8 -*-
from __future__ import print_function
import xlrd
import xlwt
import sys
import json
import jieba
import jieba.posseg as pseg
import os
import re
import codecs
import time


#########################################################
# Corpus pre-process

def strip_tags(s):
    """
    Strips HTML tags.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440481
    :param s:   string
    :return:    string
    """
    in_tag = [False]

    def chk(c):
        if in_tag[0]:
            in_tag[0] = (c != '>')
            return False
        elif c == '<':
            in_tag[0] = True
            return False
        return True
    return ''.join(c for c in s if chk(c))


def clean_comment(str_in):
    """
    过滤汽车评论
    :param str_in:  unicode or str
    :return:
    """
    str_out = str_in
    pattern_strip = [
        re.compile(u"引用"r'.*'u"发表的回复"),
        re.compile(r'.*'u"发表在"),
    ]
    for t_p in pattern_strip:
        str_out = re.sub(t_p, "", str_out).strip(" ")
    str_out = strip_tags(str_out)
    return str_out


def delete_stop_words(str_in, is_filter=False, return_list=False):
    """
    去停用词
    :param str_in:  string
    :param return_list: 是否返回列表，False表示返回字符串
    :param is_filter: 是否启用词性过滤
    :return:    string
    """

    # 取停用词
    path_stop_words = "./"
    file_stop_words = "stopwords.txt"

    if os.path.exists(path_stop_words + file_stop_words):
        stop_words = codecs.open(path_stop_words + file_stop_words, encoding='UTF-8').read()
    else:
        print("No stop words given: ", path_stop_words + file_stop_words)
        stop_words = []

    # 取过滤列表
    if is_filter:
        # filter_polar = ['/x', '/zg', '/uj', '/ul', '/e', '/d', '/uz', '/y']
        filter_polar = [u'n', u'f', u'a', u'z']
    else:
        filter_polar = None

    # 去停用词，去指定词性
    t_content_a = ""
    t_list = []
    for word, flag in pseg.cut(str_in):
        if word in stop_words:
            continue
        if filter_polar is None:
            t_content_a += word
            t_list.append(word)
        elif flag[0] in filter_polar:
            t_content_a += word
            t_list.append(word)
        else:
            continue

    # return 选项
    if return_list:
        return t_list
    else:
        return t_content_a


################################################################
# Get corpus from difference files

def get_sentiment_artificial_mark(corpus_path_in, files, sheet_num=None, line_num=None):
    """
    从手工标记的 excel 中导入 训练集, 文件路径为./Corpus/SentimentArtificialMark
    ***注意***：所给的训练集行数必须超过 100 个
    :param line_num:
    :param sheet_num:
    :param corpus_path_in:
    :param files: [filename1, filename2, ...]
    :return:    [(label1, text1), (label2, text2), ...]
    """
    train_set = []
    min_line_in_sheet = 100
    for t_file in files:
        data = xlrd.open_workbook(corpus_path_in + t_file)
        sheets = data.sheet_names()  # [sheet1, sheet2, ...]
        count = 0
        for sheet in sheets:
            if sheet_num is not None and count >= sheet_num:
                break
            t_rows = data.sheet_by_name(sheet).nrows
            if t_rows < min_line_in_sheet:
                # 排除所有训练不足min_line_in_sheet行的语料 因为有些可能是表格的说明
                print("Lines in %s is short of %s, we deleted it." % (t_file + '/' + sheet, min_line_in_sheet))
                continue

            count_line = 0
            for t_line in range(t_rows):
                if line_num is not None and count_line >= line_num:
                    break
                print(sheet, "line", t_line)
                t_label = str(data.sheet_by_name(sheet).cell(t_line, 0).value).encode('utf-8') + '_' + \
                          str(data.sheet_by_name(sheet).cell(t_line, 1).value).split('.')[0].encode('utf-8')
                t_content = data.sheet_by_name(sheet).cell(t_line, 2).value
                print(t_content)
                if type(t_content) is not unicode:
                    t_content = str(data.sheet_by_name(sheet).cell(t_line, 2).value)
                t_content = clean_comment(t_content)
                t_text = delete_stop_words(t_content.encode('utf-8'))
                train_set.append((t_label, t_text))
                count_line += 1
            count += 1
    return train_set


def get_xls_train_set(files, num_text):
    """
    Get train set from excel(.xls)
    :param files: List of file names.
    :param num_text: Texts line read each train.
    :return:    List of tuple [(label, text), (_, _),(,)]
    """
    train_set = []
    for t_file in files:
        data = xlrd.open_workbook(t_file)
        table = data.sheet_by_index(0)
        num_line = min(table.nrows, num_text)
        print("Read %s lines from %s." % (num_line, t_file))
        for t_line in range(num_line):
            train_set.append((t_file.split("/")[-1].split(".")[0], table.cell(t_line, 0).value.encode('utf-8')))
    return train_set


def get_txt_train_set(files, num_text):
    """
    Get train set from text(.txt), label 在文本内
    :param files: List of file names.
    :param num_text: Texts line read each train.
    :return:    List of tuple [(label, text), (_, _),(,)]
    """
    import re
    train_set = []
    count_line = 1
    for t_file in files:
        if t_file.split('.')[-1] != "txt":
            raise "****** Wrong file type during train set, a .txt file excepted ******"
        fp = open(t_file, 'rb')
        contents = fp.readlines()
        fp.close()
        for t_content in contents:
            if count_line > num_text:
                break
            pattern = re.search(r'([0-9]+)(\s+)(.*)', t_content)
            if pattern:
                t_label = pattern.group(1)
                t_text = pattern.group(3)
            else:
                print("ERROR: re wrong in line_%s: %s" % (count_line, t_content))
                break
            train_set.append((t_label, t_text))
            count_line += 1
    return train_set


def get_class_txt_train_set(file_path_in, files):
    """
    从带分类的文本文件中取语料，取自LDA程序, label 为文本名，新闻文本
    :param files: List of file names.
    :param file_path_in:
    :return:    List of tuple [(label, text), (_, _),(,)]
    """
    import re
    train_set = []
    for t_file in files:
        t_label = re.search(r'(.*)(_)(.*)$', t_file).group(1)
        t_content = open(file_path_in + t_file, 'rb').read()
        t_content = clean_comment(t_content)
        t_content = delete_stop_words(t_content)
        print("Read contents from %s." % t_file)
        train_set.append((t_label, t_content))
    return train_set


def json_dict_from_file(json_file,fieldname=None):
    """
    load json file and generate a new object instance whose __name__ filed
    will be 'inst'
    :param json_file:
    """
    obj_s = []
    with open(json_file) as f:
        for line in f:
            object_dict = json.loads(line)
            if fieldname==None:
                obj_s.append(object_dict)
            elif object_dict.has_key(fieldname):

                obj_s.append(delete_stop_words(clean_comment(object_dict[fieldname]), return_list=True))
    return obj_s


def txt2list(f_name_in, return_mod=3, is_filter=False):
    """
    从一个文本文件中取每行作为一句话，作为 Word2Vec的训练集。
    :param f_name_in:    带输入的文件名（单个文件）
    :param return_mod:  返回模式，也就是返回的结果的个数
    :param is_filter:   是否针对词性去词
    :return:    s_list, vocab, word_idx
    """

    # Get file content
    if "result" in f_name_in:
        print("Input file is a result file.")
        fp = open(f_name_in, 'rb')
        t_s = []
        sa = fp.read().split('\r')
        for i in sa:
            if "content:" in i:
                print("before: ", i)
                ss = delete_stop_words(clean_comment(i.split(":", 1)[1]), is_filter, return_list=True)
                if len(''.join(ss).strip('\n').strip('\r').strip(' ')) == 0:
                    continue
                print("after: ", ''.join(ss))
                t_s.append(ss)
            else:
                continue
        fp.close()
    else:
        fp = open(f_name_in, 'rb')
        t_s = []
        for i in fp.readlines():
            if "content:" in i:
                t_s.append(delete_stop_words(clean_comment(i), is_filter, return_list=True))
            else:
                continue
        fp.close()

    # Create something output
    s_list = t_s
    vocab = list(sorted(reduce(lambda x, y: x | y, (set(ss_l) for ss_l in s_list))))
    word_idx = dict((c, i) for i, c in enumerate(vocab))
    print("********** vocabulary ************")
    for t_i in vocab:
        print(t_i)
    print('\r')
    print("length = ", len(vocab))
    print("********** end of vocabulary ************")

    # return 选项
    if return_mod == 1:
        return s_list
    elif return_mod == 2:
        return s_list, vocab
    elif return_mod == 3:
        return s_list, vocab, word_idx


def xls2list(f_name_in, return_mod=3, is_filter=False, sheet_num=None, line_num=None):
    """
    从手工标记的excel文件中取每行作为一句话，作为 Word2Vec的训练集。
    :param f_name_in:    带输入的文件名（单个文件）
    :param return_mod:  返回模式，也就是返回的结果的个数
    :param is_filter:   是否针对词性去词
    :param sheet_num:
    :param line_num:
    :return:    s_list, vocab, word_idx
    """
    min_line_in_sheet = 100
    train_set = []
    data = xlrd.open_workbook(f_name_in)
    sheets = data.sheet_names()  # [sheet1, sheet2, ...]
    count = 0

    # 取文件中所有的 sheet
    for sheet in sheets:
        if sheet_num is not None and count >= sheet_num:
            break
        t_rows = data.sheet_by_name(sheet).nrows
        if t_rows < min_line_in_sheet:
            # 排除所有训练不足min_line_in_sheet行的语料 因为有些可能是表格的说明
            print("Lines in %s is short of %s, we deleted it." % (f_name_in + '/' + sheet, min_line_in_sheet))
            continue

        # 取 sheet 中所有的 line
        count_line = 0
        for t_line in range(t_rows):
            if line_num is not None and count_line >= line_num:
                break
            print(sheet, "line", t_line)
            t_content = data.sheet_by_name(sheet).cell(t_line, 2).value
            if type(t_content) is not unicode:
                t_content = str(data.sheet_by_name(sheet).cell(t_line, 2).value)

            # process
            print("before: ", t_content)
            t_text = delete_stop_words(clean_comment(t_content), is_filter, return_list=True)
            # delete empty
            if len(''.join(t_text).strip('\n').strip('\r').strip(' ')) == 0:
                continue
            print("after: ", ''.join(t_text))

            train_set.append(t_text)
            count_line += 1
        count += 1

    # Create something output
    s_list = train_set
    vocab = list(sorted(reduce(lambda x, y: x | y, (set(ss_l) for ss_l in s_list))))
    word_idx = dict((c, i) for i, c in enumerate(vocab))
    print("********** vocabulary ************")
    for t_i in vocab:
        print(t_i)
    print('\r')
    print("length = ", len(vocab))
    print("********** end of vocabulary ************")

    # return 选项
    if return_mod == 1:
        return s_list
    elif return_mod == 2:
        return s_list, vocab
    elif return_mod == 3:
        return s_list, vocab, word_idx






