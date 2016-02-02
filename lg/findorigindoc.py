# -*- coding: utf-8 -*-
__author__ = 'ancheng'


from gensim import corpora, models, similarities
import logging
import jieba
import codecs
import jieba.posseg as pseg
import json
import time
# logging.basicConfig(format=’%(asctime)s:%(levelname)s:%(message)s’,level=logging.INFO)

documents = [
    [u"空灵绝尘，倚天琊绝美独立。清冷孤傲，守相思不悔情深。初见，陆雪琪。",'4818','201511281052'],
    [u"小七，15岁生日快乐。[蛋糕]我们会陪你继续感受爱与纯真。",'3432','201512062006'],
    [u"古灵精怪，持轩辕仗剑江湖。逍遥洒脱，但求情义双全。初逢，曾书书。",'992','201512062031'],
    [u"斩龙剑出，一身傲骨。浩然正气，立于天地之间。龙首峰弟子，林惊羽。",'1162','201512072002'],
    [u"剑眉星目，清朗俊美。初入青云，玉清殿上，展聪颖天资。@TFBOYS-王俊凯",'153030','201512081803'],
    [u"台上出现了另一个女儿！张歆艺 竟然和叶一云 牵起了手，还跟张国立 老师说自己是女婿，吓死宝宝了[doge][doge][doge]这是啥剧情，姚晨也来了",'9','201512081449'],
    [u"#张歆艺出柜叶一云#五官已毁，放开那女孩，让我来",'8','201512081548'],
    [u"导演@陈思诚 与@王宝强 演绎深厚兄弟情。MV纪录了两人”兄弟一路相随“的情谊，从十年前的《士兵突击》到现在的《唐人街探案》，当年战友“伍六一”@邢佳栋 “高城”@演员张国强 “史今”@张译 更是出镜助阵。#1231唐人街探案#",'45','201512081426'],
    [u"#士兵突击十年再聚首#十年前后，典型的仗着你喜欢我我就欺负你。",'19','201512082001']
            ]


messagefile = './message_liuxiaolingtong.json'   #message文件位置

similarity_limit = 0.8   #相似度下限

reposts_limit = 1 #转发下限
#input文本
input = [u'六小龄童未得到春晚邀请的事情在持续发酵',u'20797',u'201601281702'],

#########################################################

def getjson(filename):
    doc = []
    with open(filename, "r") as f:
        for l in f:
            d = json.loads(l,encoding='utf-8')

            if "reposts" in d.keys() and d["reposts"]>=0:
                doc.append(d)

        return doc

# documents = []
documents = getjson(messagefile)



def delNOTNeedWords(content,customstopwords=None):
    # words = jieba.lcut(content)
    if customstopwords == None:
        import os
        file_stop_words = "stopwords.txt"
        if os.path.exists(file_stop_words):
            stop_words = codecs.open(file_stop_words, encoding='UTF-8').read()
            customstopwords = stop_words

    result=''
    # for w in words:
    #     if w not in stopwords:
    #         result += w.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    words = pseg.lcut(content)

    for word, flag in words:
        # print word.encode('utf-8')
        if (word not in customstopwords and flag[0] in [u'n', u'f', u'a', u'z']):
            # ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    return result


# texts = [[word for word in jieba.lcut(delstopwords(document))] for document in documents]
texts = [jieba.lcut(delNOTNeedWords(document["content"])) for document in documents]
dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]  # 生成词袋
tfidf = models.TfidfModel(corpus)
copurs_tfidf = tfidf[corpus]
lsi = models.LsiModel(copurs_tfidf, id2word=dictionary, num_topics=20)
index = similarities.MatrixSimilarity(lsi[corpus])
input_bow = dictionary.doc2bow(jieba.lcut(delNOTNeedWords(''.join(input[0]))))
input_lsi = lsi[input_bow]
print input_lsi
sims = index[input_lsi]
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print (sort_sims)

# print (documents[sort_sims[0][0]])

output = []
count = 0
oldtime = 0
counts = []
for d in sort_sims:
    # if documents[d[0]]["reposts"]>=reposts_limit:
    #     print d[1],documents[0]["reposts"]
    date = documents[d[0]]["tC"]["$date"]
    date = date[:-5].replace(u'T',u' ')
    tempdate = time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
    time = int(tempdate/10000000)
    count = count + 1
    if oldtime!=time:
        counts.append(float(count))
        count = 0
        oldtime = time

    if (d[1]>=similarity_limit and documents[d[0]]["reposts"]>=reposts_limit):
        output.append(documents[d[0]])



# output_date = output.sort(lambda a,b:a[2]-b[2])
# try:
output_date = sorted(output,key=lambda x:x["tC"]["$date"])
# except TypeError:
#     print TypeError
x_reposts = []
x_date = []
for item in output_date:
    print(item["content"].encode("utf-8")+" "+ str(item["reposts"])+" "+item["tC"]["$date"].encode("utf-8"))
    x_reposts.append(float(item["reposts"]))
    x_date.append(item["tC"]["$date"].encode("utf-8"))

import matplotlib.pyplot as plt
# import time
y = x_reposts

dates = []
for d in x_date:
    d = d[:-5].replace(u'T',u' ')
    tempdate = time.mktime(time.strptime(d,'%Y-%m-%d %H:%M:%S'))
    # print tempdate
    dates.append(tempdate/1000000000)
x = dates

# z = np.cos(x**2)

plt.figure(figsize=(80,50))
plt.plot(x,y,color="red",linewidth=2)
plt.plot(x,counts,"b--",label="$cos(x^2)$",color="green")
plt.xlabel("Time(s)")
plt.ylabel("Reposts")
plt.title("find origin content")
# plt.ylim(-1.2,1.2)
plt.legend()
plt.show()