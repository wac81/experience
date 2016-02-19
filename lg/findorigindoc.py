# -*- coding: utf-8 -*-
__author__ = 'ancheng'


from gensim import corpora, models, similarities
import logging
import jieba
import codecs
import jieba.posseg as pseg
import json
import time,datetime
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


# messagefile = './message_liuxiaolingtong.json'   #message文件位置
# messagefile = './weibo.json'   #message文件位置
messagefile = '/home/wac/data/hotWeibo_9200.json'
similarity_limit = 0.7   #相似度下限

reposts_limit = 0 #转发下限
#input文本
# input = [u'《沁园春·买票》：“春节又到，中华大地，有钱飞机，没钱站票。望长城内外，大包小包。大河上下，民工滔滔。早起晚睡，达旦通宵，欲与票贩试比高。须钞票。看人山人海，一票难保。车票如此难搞，引无数英雄竞折腰。昔秦皇汉武，见此遁逃；唐宗宋祖，更是没招！一代天骄，成吉思汗，只好骑马往回飙。',u'20797',u'201601281702']
# input = [u'#金报印象#1、湖北省旅游局升格更名为旅游发展委；2、春节红包抽样调查38%市民预算超5000；3、铁警侦破假车票案起获6000张空票版；4、张帅止步澳网八强有望冲刺里约奥运；5、顾客“找茬”获赔47万；6、桑塔纳抢道撞坏宾利车。更多精彩，详见http://t.cn/RbuBA34',u'20797',u'201601281702']
# input = [u'#致我们终将到来的爱情#吕逸涛滚出导演圈关于六小龄童不上春晚，我觉得大家不要再骂了，毕竟节目已经都被毙了。领导之间的事情我们也管不了 大家应该互相体谅一下，不要动不动在别人微博底下骂人，骂人不好，他自己有脑子。我们应该站起来打，能动手的尽量不要动口。能见到导演的帮我补一脚，谢谢',u'20797',u'201601281702']
# input = [u'【为何开年市场这么惨？因为这“三个预期差”】尽管市场对经济下行预期一致，但汇股债三市仍显示剧烈震荡，表明预期差始终存在。华泰证券认为，2016年存在三个预期差，形成强烈的不确定性：人民币、港币汇率的大幅震荡；春节前降准大概率落空；“供给侧改革”可能不是以一种快速出清的方式展现。',u'20797',u'201601281702']
input = [u'@春节晚会微吧 看到六小龄童春晚节目被毙只好去上戏曲春晚的消息挺可惜的。其实他只需要上去耍通棍子零点大门一开猴哥高喊“俺老孙来也”配上大闹天宫的音乐大家就会看得很开心吧宁可请一个韩国棒子都要抹杀掉真正的国粹下一个猴年春晚要12年后他已经快六十岁了。这个必须转!六小龄童真的影响了一代人',u'20797',u'201601281702']



#########################################################

def getjson(filename):
    doc = []
    with open(filename, "r") as f:
        for l in f:
            d = json.loads(l,encoding='utf-8')
            if "reposts" in d.keys() and d["reposts"]>=0:
                doc.append(d)
        return doc

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
        if (word not in customstopwords and flag[0] in  [u'n', u'f', u'a', u'd',u'z']):
            # ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    return result

def convert_time(timestr):
    date = timestr[:-5].replace(u'T',u' ')
    datetimeObj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    tempdate = int(datetimeObj.strftime("%Y%m%d%H%M"))
    return tempdate

documents = getjson(messagefile)
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
valuecount = 0
valuecounts = []
for d in sort_sims:
    if "tC" in documents[d[0]].keys() and documents[d[0]]["tC"]!=None and "$date" in documents[d[0]]["tC"].keys():
            valuecount = valuecount + 1
            if (d[1]>=similarity_limit and documents[d[0]]["reposts"]>=reposts_limit):
                if convert_time(documents[d[0]]["tC"]["$date"])>201600000000:
                    output.append(documents[d[0]])
                    valuecounts.append(float(valuecount))
                    valuecount = 0

# output_date = output.sort(lambda a,b:a[2]-b[2])
output_date = sorted(output,key=lambda x:x["tC"]["$date"])
x_reposts = []
x_date = []
for item in output_date:
    print(item["content"].encode("utf-8")+" "+ str(item["reposts"])+" "+item["tC"]["$date"].encode("utf-8"))
    x_reposts.append(float(item["reposts"]))
    x_date.append(convert_time(item["tC"]["$date"]))

y = x_reposts
x = x_date
import matplotlib.pyplot as plt

# plt.figure(figsize=(200,50))
plt.figure()
plt.plot(x,y,color="red",linewidth=2)
print (valuecounts,len(x),len(valuecounts))
plt.plot(x,valuecounts,"b--",label="$cos(x^2)$",color="green")
plt.xlabel("Time(s)")
plt.ylabel("Reposts")
plt.title("find origin content")
# plt.ylim(-1.2,1.2)
plt.legend()
plt.show()