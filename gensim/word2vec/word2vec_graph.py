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
# import matplotlib.pyplot as plt
from svm_sentiment_grocery import txt2list
from gensim.models import Word2Vec,Phrases


auto_brand = codecs.open("Automotive_Brand.txt", encoding='gb2312').read()


def get_text_from_tuple(tuple_in):
    """
    假设语料都是 clean 过得，这里不做 clean 和去停用词的工作
    :param tuple_in: [(label1, text1), (label2, text2), ...]
    :return: [[text1], [text2], ...] 返回生成器
    """
    for _, text in tuple_in:
        yield list(jieba.cut(text))



class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


if __name__ == '__main__':

    file_name = "./result.txt"
    s_list, vocab, word_idx = txt2list(file_name, return_mod=3, is_filter=True)

    feature_size = 400
    content_window = 10
    freq_min_count = 3
    threads_num = 4
    negative = 4   #best采样使用hierarchical softmax方法(负采样，对常见词有利)，不使用negative sampling方法(对罕见词有利)。
    iter = 10

    print("word2vec...")
    tic = time.time()
    bigram_transformer = Phrases(s_list)
    model = Word2Vec(bigram_transformer[s_list], size=feature_size, window=content_window, min_count=freq_min_count, negative=negative, iter=iter, workers=threads_num)
    toc = time.time()
    print("Word2vec completed! Elapsed time is %s." % (toc-tic))

    while 1:
        print("请输入想测试的单词： ", end='\b')
        t_word = sys.stdin.readline()
        if "quit" in t_word:
            break
        results = model.most_similar([t_word.decode('utf-8').strip('\n').strip('\r').strip(' ')],topn=30)
        # results = model.most_similar(negative=[u'豪车'],topn=5)
        for t_w, t_sim in results:
            if any ([t_w==ab for ab in auto_brand.split(u'\r\n')]):      #过滤品牌
                print(t_w, " ", t_sim)

