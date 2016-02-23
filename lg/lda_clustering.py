# -*- coding: utf-8 -*-
__author__ = 'ancheng'


from gensim import corpora, models, similarities
import logging
import jieba
import codecs
import jieba.posseg as pseg
import json
import re

#文档主题数量
topicnum = 8
#文档相似度下线 超过此下限的文档在聚类中取出(0,1)
doc_distance_limit = 0.8



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
        if (word not in customstopwords and flag[0] in [u'n', u'f', u'a',  u'v', u'd',u'z']):
            # ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
            return_words.append(word.encode('utf-8'))
    return result,return_words


# texts = [[word for word in jieba.lcut(delstopwords(document))] for document in documents]
datafilename = '/home/wac/data/chunwan.json'

documents = json_dict_from_file(datafilename,['content','reposts'],False)
# repost = json_dict_from_file(datafilename,'content',False)
# repostrepost = sorted(documents, key=lambda x: -x[1])
# print repostrepost[0][1],repostrepost[0][0].encode("utf-8")
# print repostrepost[1][1],repostrepost[1][0].encode("utf-8")
# print repostrepost[2][1],repostrepost[2][0].encode("utf-8")
# print repostrepost[3][1],repostrepost[3][0].encode("utf-8")


# texts = json_dict_from_file(datafilename,['content'])
texts = [delNOTNeedWords(d[0])[1] for d in documents]
dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]  # 生成词袋
tfidf = models.TfidfModel(corpus)
copurs_tfidf = tfidf[corpus]
lda = models.LdaModel(copurs_tfidf, id2word=dictionary, num_topics=topicnum)
print(lda.print_topics(1)[0][1])
print(lda.print_topics(2)[0][1])


#句子聚类
corpus_lda = lda[copurs_tfidf]
index = similarities.MatrixSimilarity(corpus_lda)

# temparray = [[] for i in range(topicnum)]
numarray = [[] for i in range(topicnum)]
repostsnum = []
# 矩阵运算,理论上是求逆矩阵,然后排序取最大相似
for id,doc in enumerate(corpus_lda):
    temp = sorted(doc, key=lambda x: -x[1])
    item = list(temp[0])
    item[0] = id
    item = tuple(item)
    if item[1] > doc_distance_limit:
        numarray[temp[0][0]].append(item)

# for id,doc in enumerate(corpus_lda):
#     for docid,item in enumerate(doc):
#         item = list(item)
#         item[0] = id
#         item = tuple(item)
#         temparray[docid].append(item)
for one in numarray:
    temp = 0
    for x in one:
        reposts = int(documents[x[0]][1])
        temp = temp + reposts
    repostsnum.append(temp)


for id,itemone in enumerate(numarray):
    sort_sims = sorted(itemone, key=lambda item: -item[1])
    # print sort_sims
    print documents[sort_sims[0][0]][0]
    print sort_sims[0][1]
    print len(numarray[id])
    print repostsnum[id]

