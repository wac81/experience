# -*- coding:utf-8 -*-
from __future__ import print_function
import numpy as np
import os
import sys
import jieba
import time
import jieba.posseg as pseg
import pprint as pp
# import matplotlib.pyplot as plt
from corpus_preprocess import txt2list, xls2list, json_dict_from_file, delete_stop_words, clean_comment
from gensim.models import Word2Vec
import codecs

def get_text_from_tuple(tuple_in):
    """
    假设语料都是 clean 过得，这里不做 clean 和去停用词的工作
    :param tuple_in: [(label1, text1), (label2, text2), ...]
    :return: [[text1], [text2], ...] 返回生成器
    """
    for _, text in tuple_in:
        yield list(jieba.cut(text))

auto_brand = codecs.open("Automotive_Brand.txt", encoding='gb2312').read()

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        json_list = json_dict_from_file(self.dirname,"content")
        for json_dict in json_list:
            # try:
            content = delete_stop_words(clean_comment(json_dict['content']), return_list=True)
            # content = delete_stop_words(clean_comment(json_dict), return_list=True)
            # return content
            yield content
            # except KeyError:
            #     print (KeyError)
            #     continue


if __name__ == '__main__':

    file_name = "./autohome.json"
    save_model = "./word2vec.model"
    # s_list, vocab, word_idx = txt2list(file_name, return_mod=3, is_filter=True)
    # s_list, vocab, word_idx = xls2list(file_name, return_mod=3, is_filter=True)
    # s_list = MySentences(file_name)



    feature_size = 400
    content_window = 10
    freq_min_count = 3
    threads_num = 4
    negative = 4   # best采样使用hierarchical softmax方法(负采样，对常见词有利)，不使用negative sampling方法(对罕见词有利)。
    t_iter = 10

    print("word2vec...")
    tic = time.time()
    if os.path.isfile(save_model):
        model = Word2Vec.load(save_model)
        print("Loaded word2vec model")
    else:
        s_list = json_dict_from_file(file_name,"content")
        model = Word2Vec(s_list, size=feature_size, window=content_window, iter=t_iter, min_count=freq_min_count, workers=threads_num)
        toc = time.time()
        print("Word2vec completed! Elapsed time is %s." % (toc-tic))
        model.save(save_model)
        print("Word2vec Saved!")





    """
    品牌维度
    """
    brand =[u'性能',
            u'配置',
            u'操控',
            u'油耗',
            u'耗油',
            u'服务',
            u'安全',
            u'舒适',
            u'品牌',
            u'外观',
            u'价格',
            u'用途']
    for b in brand:
        print("============= 请输入想测试的单词（多个单词用空格隔开） ============")
        pos_word = b
        print("--------"+pos_word+"--------")
        neg_word = []
        num_word = 50
        try:
            results = model.most_similar(pos_word, neg_word, num_word)
        except Exception as e:
            print(e)
            continue
        for t_w, t_sim in results:
            print(t_w, " ", t_sim)
    """
    汽车品牌
    """
    # for b in auto_brand.split(u'\r\n'):
    #     print("============= 请输入想测试的单词（多个单词用空格隔开） ============")
    #     pos_word = b
    #     print("--------"+pos_word+"--------")
    #     neg_word = []
    #     num_word = 500
    #     try:
    #         results = model.most_similar(pos_word, neg_word, num_word)
    #     except Exception as e:
    #         print(e)
    #         continue
    #     for t_w, t_sim in results:
    #         if any ([t_w==ab for ab in auto_brand.split(u'\r\n')]):      #过滤品牌
    #             print(t_w, " ", t_sim)

    # while 1:
    #     print("============= 请输入想测试的单词（多个单词用空格隔开） ============")
    #     print("positive: ", end='\b')
    #     pos_word = sys.stdin.readline().decode('utf-8').strip('\n').strip('\r').strip(' ').split(' ')
    #     if "quit" in pos_word:
    #         break
    #     neg_word = []
    #     print("How many words you want to print: ", end='\b')
    #     num_word = int(sys.stdin.readline().decode('utf-8').strip('\n').strip('\r').strip(' '))
    #     try:
    #         results = model.most_similar(pos_word, neg_word, num_word)
    #     except Exception as e:
    #         print(e)
    #         continue
    #     for t_w, t_sim in results:
    #         if any ([t_w==ab for ab in auto_brand.split(u'\r\n')]):      #过滤品牌
    #             print(t_w, " ", t_sim)





