# -*- coding:utf-8 -*-

import codecs
import re
import math
from operator import itemgetter, attrgetter

#初始化否定词/程度词
set_neg_prefix = set(a.strip() for a in codecs.open('dict/neg_prefix.txt','r','utf-8').readlines())
set_very_prefix = set(a.strip() for a in codecs.open('dict/very_prefix.txt','r','utf-8').readlines())

#初始化负向词和正向词
set_negative_word = set()
for line in codecs.open('dict/negative.txt','r','utf-8').readlines():
    if line.strip() != '':
        set_negative_word.add(line.strip())
set_positive_word = set()
for line in codecs.open('dict/positive.txt','r','utf-8').readlines():
    if line.strip() != '':
        set_positive_word.add(line.strip())

#初始化NTUSD词典
dict_word_score = {}
dict_negword_score = {}
dict_posword_score = {}
for line in codecs.open('dict/opinion_word.txt','r','utf-8').readlines():
    if line.strip() != '':
        currList = line.split(',')
        currWord = currList[0]
        currScore = float(currList[1])
        if (currScore > 0.0 or currScore < 0.0) and currWord not in dict_word_score.keys():
            div = 1.0
            if currScore > 0.0:
                div = 1.618
            dict_word_score[currWord] = currScore / div
        if (currScore > 0.0) and currWord not in dict_posword_score.keys():
            dict_posword_score[currWord] = currScore / 1.618
        if (currScore < 0.0) and currWord not in dict_negword_score.keys():
            dict_negword_score[currWord] = currScore

#补充NTUSD词典
lostCount = 0
for currWord in set_negative_word:
    if currWord not in dict_word_score.keys() and currWord.endswith(u'的') == False and currWord != u'东西':
        lostCount+=1
        #print currWord
        dict_word_score[currWord] = -0.08
for currWord in set_positive_word:
    if currWord not in dict_word_score.keys() and currWord.endswith(u'的') == False:
        lostCount+=1
        #print currWord
        dict_word_score[currWord] = 0.08

'''
基于增强的NTUSD词典计算输入语句的情感程度
'''
def sentiment(input_text):
    sentiment_acc_score = 0.0
    posi_score = 0.0
    nega_score = 0.0
    content = input_text
    for curr_word in dict_word_score.keys():
        if curr_word in content:
            word_count = content.count(curr_word)
            for curr_neg_prefix in set_neg_prefix:
                word_count -= content.count(curr_neg_prefix + curr_word)
            for curr_very_prefix in set_very_prefix:
                word_count += content.count(curr_very_prefix + curr_word)
            if word_count == 1:
                sentiment_acc_score += dict_word_score[curr_word]
                if dict_word_score[curr_word] > 0.0:
                    posi_score += dict_word_score[curr_word]
                elif dict_word_score[curr_word] < 0.0:
                    nega_score += dict_word_score[curr_word]
            elif word_count > 1:
                sentiment_acc_score += dict_word_score[curr_word] + dict_word_score[curr_word] * math.log(word_count - 0.9)
                if dict_word_score[curr_word] > 0.0:
                    posi_score += dict_word_score[curr_word] + dict_word_score[curr_word] * math.log(word_count - 0.9)
                elif dict_word_score[curr_word] < 0.0:
                    nega_score += dict_word_score[curr_word] + dict_word_score[curr_word] * math.log(word_count - 0.9)
    return sentiment_acc_score

novelName = 'data/yanzhiyoudu'
listSentence = []
i = 0
for line in codecs.open(novelName + '.txt','r','utf-8').readlines():
    i += 1
    print str(i)
    if line.strip() != '':
        listSentence.append(line.strip())
listPoint = []
currPoint = ''
for curri in range(len(listSentence)):
    if curri % 10 == 0:
        if currPoint != '':
            listPoint.append(currPoint)
        currPoint = ''
    else:
        currPoint += listSentence[curri]
fow = codecs.open(novelName + '_format_filter.txt', 'w', 'utf-8')
fow1 = codecs.open(novelName + '_sent_result1_filter.txt', 'w', 'utf-8')
fow2 = codecs.open(novelName + '_sent_result2_filter.txt', 'w', 'utf-8')
for currPoint in listPoint:
    currScore = sentiment(currPoint)
    if currScore > -2.5 and currScore < 1.0:
        continue
    else:
        fow.write(currPoint.replace('\n',''))
        fow.write('\n')
        fow1.write(str(currScore))
        fow1.write('\n')
        fow2.write(str(math.fabs(currScore)))
        fow2.write('\n')
fow.close()
fow1.close()
fow2.close()
