# -*- coding:utf-8 -*-
from __future__ import print_function
from tgrocery import Grocery
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

"""
文件描述：
使用 tgGrocery 中的 SVM 模型
取文件 训练模型 去停用词 预测 打分
"""


########################################################
# functions

def sentiment_train(gro_name, train_set):
    """
    tgGrocery svm train
    :param gro_name:
    :param train_set:
    :return:
    """
    gro_ins = Grocery(gro_name)
    # gro_ins.load()
    gro_ins.train(train_set)
    print("Is trained? ", gro_ins.get_load_status())
    gro_ins.save()


#########################################################
# Get train set

def strip_tags(s):
    """
    Strips HTML tags.
    Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440481
    :param s:
    :return:
    """
    intag = [False]

    def chk(c):
        if intag[0]:
            intag[0] = (c != '>')
            return False
        elif c == '<':
            intag[0] = True
            return False
        return True
    return ''.join(c for c in s if chk(c))


def clean_comment(str_in):
    """
    过滤汽车评论
    :param str_in:  unicode or str
    :return:
    """
    pattern_1 = re.compile(u"引用"r'.*'u"发表的回复")
    pattern_2 = re.compile(r'.*'u"发表在")
    str_out = re.sub(pattern_1, "", str_in).strip(" ")
    str_out = re.sub(pattern_2, "", str_out).strip(" ")
    str_out = strip_tags(str_out)
    return str_out


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


def json_dict_from_file(json_file):
    """
    load json file and generate a new object instance whose __name__ filed
    will be 'inst'
    """
    obj_s = []
    with open(json_file) as f:
        for line in f:
            object_dict = json.loads(line)
            obj_s.append(object_dict)
    return obj_s


def txt2list(fname_in, return_mod=3, is_filter=False):
    """
    从一个文本文件中取每行作为一句话，作为 Word2Vec的训练集。
    :param fname_in:    带输入的文件名（单个文件）
    :param return_mod:  返回模式，也就是返回的结果的个数
    :param is_filter:   是否针对词性去词
    :return:    s_list, vocab, word_idx
    """
    # Get file content
    if "result" in fname_in:
        print("Input file is a result file.")
        fp = open(fname_in, 'rb')
        t_s = []
        sa = fp.read().split('\r')
        for i in sa:
            if "content:" in i:
                print("before: ", i)
                ss = delete_stop_words(clean_comment(i.split(":", 1)[1]))
                print("after: ", ss)
                if len(ss.strip('\n').strip('\r').strip(' ')) == 0:
                    continue
                t_s.append(ss)
            else:
                continue
        fp.close()
    else:
        fp = open(fname_in, 'rb')
        t_s = []
        for i in fp.readlines():
            if "content:" in i:
                t_s.append(delete_stop_words(clean_comment(i)))
            else:
                continue
        fp.close()

    # 此处可以自己设定
    s_polar = []

    if is_filter:
        # filter_polar = [u'x', u'zg', u'uj', u'ul', u'e', u'd', u'uz', u'y',u'v']
        filter_polar = [u'n',u'f',u'a',u'z']
    else:
        filter_polar = None

    for t_i in t_s:
        temp = []
        for word, flag in pseg.cut(t_i):
            if filter_polar is None:
                temp.append(word)
            elif flag[0]  in filter_polar:
                temp.append(word)
        s_polar.append(temp)

    # Create something output
    s_list = s_polar
    vocab = list(sorted(reduce(lambda x, y: x | y, (set(ss_l) for ss_l in s_list))))
    word_idx = dict((c, i) for i, c in enumerate(vocab))
    for t_i in vocab:
        print(t_i, "-", end='\b')
    print("\r")

    if return_mod == 1:
        return s_list
    elif return_mod == 2:
        return s_list, vocab
    elif return_mod == 3:
        return s_list, vocab, word_idx


#########################################################
# Delete stop words

def delete_stop_words(str_in):
    """
    去停用词
    :param str_in:  string
    :return:    string
    """
    path_stop_words = "./"
    file_stop_words = "stopwords.txt"

    t_list = list(jieba.cut(str_in))
    if os.path.exists(path_stop_words + file_stop_words):
        stop_words = codecs.open(path_stop_words + file_stop_words, encoding='UTF-8').read()
    else:
        print("No stop words given: ", path_stop_words + file_stop_words)
        stop_words = []

    t_content_a = ""
    for i in t_list:
        if i in stop_words:
            continue
        else:
            t_content_a += i.encode('utf-8')
    return t_content_a


#####################################################################
# predict label from models
# ***注意***：目前的预测模型都是基于 tgGrovery 的 SVM 模型

def predict_from_post(grocery_in):
    """
    从 post.txt 文件中读取文本进行预测的过程
    ***注意***： post.txt 的位置最好不要变
    :param grocery_in:
    :return:
    """
    file_path = "./"
    file_name = "post.txt"
    t_tic = time.time()
    t_text = delete_stop_words(clean_comment(codecs.open(file_path + file_name, encoding='UTF-8').read()))
    t_pre_result = grocery_in.predict(delete_stop_words(t_text))
    t_toc = time.time()

    t_label = t_pre_result.predicted_y
    print("Sentiment: ", t_label)
    print("How much: ", t_pre_result.dec_values[t_label])
    print("Elapsed time of predict is: %s s" % (t_toc-t_tic))


def predict_for_json(grocery_in, json_file, to_json_file):
    """

    :param grocery_in:
    :param to_json_file:
    :param json_file:
    :return:
    """
    tag_name = "autoTags"
    fout = open(to_json_file, 'a')
    json_list = json_dict_from_file(json_file)
    for json_dict in json_list:
        json_dict_temp = json_dict
        content = clean_comment(json_dict['content'])
        t_pre_result = grocery_in.predict(content)
        t_label = t_pre_result.predicted_y
        json_dict_temp[tag_name] = t_label
        fout.write((json.dumps(json_dict_temp) + '\r\n').encode('utf-8'))
        print("----------------------------------------------------")
        print("content: %s" % content)
        print("autoTags: %s" % t_label)
        # print("Write complete!")
    fout.close()


def predict_for_one(grocery_in):
    """
    Predict label for one sentents you enter.
    :param grocery_in:  Grocery instance.
    :return:    print in stdout.
    """
    while 1:
        print("Enter the sentence you want to test(\"quit\" to break): ", end='\b')
        t_text = sys.stdin.readline()
        if "quit" in t_text:
            break
        t_pre_result = grocery_in.predict(t_text)
        t_label = t_pre_result.predicted_y
        # if max(pre_result.dec_values) < 0.03:
        #     label = "neutral"
        print("Sentiment: ", t_label)
        print("How much: ", max(t_pre_result.dec_values))


def get_scores(predicts):
    """

    :param predicts:  Class of Geometric Margin.
    :return:
    """
    scores = {}
    index = (max(predicts.dec_values))


########################################################
# main
if __name__ == "__main__":
    import time
    grocery_name = "./meter"
    corpus_path = "./Corpus/"
    max_line_num_once = 1000000  # 每个文件中读取的最大行数

    tic = time.time()
    file_list = [
        corpus_path + "neg.xls",
        corpus_path + "pos.xls"
    ]
    train_src = get_xls_train_set(file_list, max_line_num_once)

    sentiment_train(grocery_name, train_src)
    toc = time.time()
    print("Elapsed time of training is: ", toc - tic)

    grocery = Grocery(grocery_name)
    grocery.load()

    predict_for_one(grocery)



