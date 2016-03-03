# -*- coding:utf-8 -*-
from __future__ import print_function
import numpy as np
import os
import sys
import jieba
import time
import jieba.posseg as pseg
import pprint as pp
import codecs
import multiprocessing
import json
# import matplotlib.pyplot as plt
from svm_sentiment_grocery import txt2list
from gensim.models import Word2Vec,Phrases


# auto_brand = codecs.open("Automotive_Brand.txt", encoding='utf-8').read()


def json_dict_from_file(json_file,fieldnames=None,isdelwords=True):
    """
    load json file and generate a new object instance whose __name__ filed
    will be 'inst'
    :param json_file:
    """
    obj_s = []
    with open(json_file) as f:
        for line in f:
            object_dict = json.loads(line)
            if fieldnames==None:
                obj_s.append(object_dict)
            else:
                # for fieldname in fieldname:
                    if set(fieldnames).issubset(set(object_dict.keys())):
                        one = []
                        for fieldname in fieldnames:
                            if isdelwords and fieldname == 'content':
                                one.append(delNOTNeedWords(object_dict[fieldname])[1])
                            else:
                                one.append(object_dict[fieldname])
                        obj_s.append(one)
    return obj_s
def delNOTNeedWords(content,customstopwords=None):
    # words = jieba.lcut(content)
    if customstopwords == None:
        import os
        file_stop_words = "stopwords.txt"
        if os.path.exists(file_stop_words):
            stop_words = codecs.open(file_stop_words, encoding='UTF-8').read()
            customstopwords = stop_words

    result=''
    return_words = []
    # for w in words:
    #     if w not in stopwords:
    #         result += w.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    words = pseg.lcut(content)

    for word, flag in words:
        # print word.encode('utf-8')
        tempword = word.encode('utf-8').strip(' ')
        if (word not in customstopwords and len(tempword)>0 and flag in [u'n',u'nr',u'ns',u'nt',u'nz',u'ng',u't',u'tg',u'f',u'v',u'vd',u'vn',u'vf',u'vx',u'vi',u'vl',u'vg', u'a',u'an',u'ag',u'al',u'm',u'mq',u'o',u'x']):
            # and flag[0] in [u'n', u'f', u'a', u'z']):
            # ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += tempword # +"/"+str(w.flag)+" "  #去停用词
            return_words.append(tempword)
    return result,return_words



if __name__ == '__main__':

    file_name = "./smzdm_one.txt"

    files = open(file_name)
    s_list = []
    for line in files:
        s_list.append(delNOTNeedWords(line)[1])

    # s_list, vocab, word_idx = txt2list(file_name, return_mod=3, is_filter=True)
    # file_name = "./coralqq.json"
    # s_list = json_dict_from_file(file_name,['content'],True)
    #
    # s_list = [d[0] for d in s_list]

    feature_size = 50
    content_window = 4
    freq_min_count = 2
    # threads_num = 4
    negative = 3   #best采样使用hierarchical softmax方法(负采样，对常见词有利)，不使用negative sampling方法(对罕见词有利)。
    iter = 20

    print("word2vec...")
    tic = time.time()
    bigram_transformer = Phrases(s_list)
    model = Word2Vec(bigram_transformer[s_list], size=feature_size, window=content_window, min_count=freq_min_count, iter=iter, workers=multiprocessing.cpu_count())
    toc = time.time()
    print("Word2vec completed! Elapsed time is %s." % (toc-tic))

    while 1:
        print("请输入想测试的单词： ", end='\b')
        t_word = sys.stdin.readline()
        if "quit" in t_word:
            break
        try:

            results = model.most_similar([t_word.decode('utf-8').strip('\n').strip('\r').strip(' ')],topn=30)
        except:
            continue
        # results = model.most_similar(negative=[u'豪车'],topn=5)
        for t_w, t_sim in results:
            # if any ([t_w==ab for ab in auto_brand.split(u'\r\n')]):      #过滤品牌
            print(t_w, " ", t_sim)

