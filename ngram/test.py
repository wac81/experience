# -*- coding:utf-8 -*-
from __future__ import print_function

import jieba
from ngram_code import ngrams, everygrams, skipgrams


def test_ngrams(text):
    """ngrams: 返回迭代器, bigram/trigram 均使用 ngram 实现"""
    N = 3
    sequence = jieba.lcut(text)
    ngram_list = ngrams(sequence=sequence, n=N)

    print("ngram, n=" + str(N))
    for ngram_term in ngram_list:
        print("/".join(ngram_term))


def test_everygrams(text):
    """everygrams: 返回文字序列所有可能的 ngram"""
    sequence = jieba.lcut(text)
    ngram_list = everygrams(sequence=sequence, min_len=1, max_len=-1)

    last_n = 0
    cnt = 1
    last_cnt = 0
    print("everygrams")
    for ngram_term in ngram_list:
        N = len(ngram_term)
        if last_n != N:
            if last_cnt != 0:
                print("total count: " + str(last_cnt))
            print("-----------------")
            print(str(N) + "-Gram")
            cnt = 0
        last_n = N
        print("/".join(ngram_term))
        cnt += 1
        last_cnt = cnt
    print("total count: " + str(last_cnt))


def test_skipgrams(text):
    """skipgrams: 返回所有的 skipgram"""
    N = 2   # ngram 维度
    K = 2   # skip 步长
    sequence = jieba.lcut(text)
    ngram_list = skipgrams(sequence=sequence, n=N, k=K)

    print("skip grams, n=" + str(N) + ", k=" + str(K))
    for ngram_term in ngram_list:
        print("/".join(ngram_term))


if __name__ == "__main__":
    text = "鲁迅老师生前是一位革命家，死后仍然是。"
    # test_ngrams(text)
    # test_everygrams(text)
    test_skipgrams(text)







