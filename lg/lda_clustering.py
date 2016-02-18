# -*- coding: utf-8 -*-
__author__ = 'ancheng'


from gensim import corpora, models, similarities
import logging
import jieba
import codecs
import jieba.posseg as pseg
import json
import re

# logging.basicConfig(format=’%(asctime)s:%(levelname)s:%(message)s’,level=logging.INFO)

documents = ["一年了，目前没有什么故障，也没有他们说的国产车小故障多；洗干净车还是很新的。个人平时开车很小心、停车也注意，没有刮擦过【吐槽】保险要到期了，天天收到保险公司的电话，烦人的保险公司。对这车还是比较满意的。",
             "目前的油费统计一下 总加油量：917.44L|总加油金额：6095元|总天数：375天|平均油耗：7.05L|平均油费:0.48元/公里 我还会继续追加口碑的",
             "柴油版真的很爽，夏天开空调不影响动力；声音不大（怠速时有一点哒哒的声音，比柴油皮卡小太多，网上说柴油不好什么的，最好到经销商处实地看看），公路上基本听不见发电机的所以（除非到安静的环境），绝对完爆汽油机。",
             "【最不满意的一点】暂时没有不满意，以后在追加评论【空间】没说的，大够用，安逸啊。【动力】2.0T柴油没说的，启步不用给油，挂1挡方离合器就走，起步后上2挡不用油门30+的速度。",
             "【操控】升级版爽啊，真的爽。档位有吸入感，没有网上说的2退1困难，听人说不如自己去看，我就是这样购车的。油耗】7个左右，柴油没说的，【舒适性】13580的车，绝对比得上合资的，绝对超值。",
             "外观】媳妇、父母、儿子、朋友满意，不多说。【内饰】内饰可以，5个人去了一次大理，车内木有异味，比某些合资车真的很值得。【性价比】超值，国产车做到这份上，够意思。论坛说这车什么的都有，如果他们说的是真的，这车还能上销售榜第一名吗？",
             "【其它描述】我同媳妇都是工薪族，靠工资养家存点钱都不容易，一直没有购车的欲望，2014年儿子中考，9月份就要到市区去读书高中，家里到市区40多公里，儿子住校，必须要一辆车接送儿子。",
             "去年我们战友聚会，战友陶勇开的是长安cs35顶配自动挡，外观漂亮，小巧，试驾、乘坐后感觉cs35各方面不错，通过观察战友大半年的使用效果，没有发现产奶事件",
             "唯一不足的是减震过坎时候有响声，没有其他的大毛病，cs35打动了我的心，所以决定入手。当准备好购车银子的时候，长安出了75，75的样子一个字“帅”，说实话75比35大，后箱能放平，自动档，各种配置很高啊，多次看陈震的视频，“中毒”更深了，非75不买的感觉。",
             "天天到之家去泡75的论坛，关注75的动向。论坛中看到贵州cs75的群，加入群准备一起团购。当听说cs75在四方河有展车的时候，第一时间赶到四方河去看车。",
             "喊上多年的老友李哥（老师傅，20多年的老师傅，驾驶过各种车辆都），一到车店迫不及待地直奔75，我们左看右看，上看下看，打开发动机盖子，后背箱。李哥看后说如果这个价位，真的可以入手，准备下订单订购的时候，发现这个地方的销售同其他地方的不一样。",
             "我们到过其他销售汽车的地方，都有人招呼，这个店没人招呼，有一点不一样啊，心里疙瘩一下，万一下了单子，主动权在他们手上，到时候自己给自己找麻烦啊。<br/>将心中的想法告诉李哥，他也是这个意见，我们决定不下单，转身走了。",
             "我到省里参加培训，结束的时候，喊上几个同事一起到四方河，还是老样子，更没有下单的欲望了。（说明一下长安也是好车，只是销售不给力哦）",
             "7月初儿子的成绩下来了，考上了市一中，媳妇叫我赶紧买车，考虑到订车也要一段时间，如果没有75，买35也可以，赶紧联系安顺、遵义长安店。问战友购车的店（清镇",
             "说有不是导航版的自动档，只是加2000，送贴膜什么的，这个价格能接收，在7月8号喊上李哥、媳妇一道去清镇，那里有35嘛，唉！不说了，赶紧到贵阳四方河看看，去了还是老样子，没人招呼没人理睬，门口有几台75，店内有2台35，找到一个销售问了，没有现车，必须订车，看销售的态度",
             "算了，直接去孟关看车去，转身走人。到了孟关之前，电话问一战友，建议去长城的柴油版，用手机查论坛，好多的档位不好挂，声音大，漏风什么的，总之一大堆H6不好，最后看到一句话，好不好到销售店去看嘛，这车不好的话，销量能排第一？"
             "的确，应该去看看。到了孟关，下高速就看见长城，直奔长城去，热情的招呼，销售带去看车，让我们和茶、喝饮料等他去取车钥匙，娶到钥匙后，说不能试驾，只能听发动机的声音，试了4台，一下选中了中国红的柴油版。刷卡，购车，直接回家。回家慢慢研究，有倒车摄像头、有前右侧摄像头",
             "这下停车方便了。有电子稳定系统，无钥匙启动，一键收后视镜。。。还没研究完。目前已经买好保险，购置税上了，就等上牌了，过一段时间再来追加评论。追加：目前发现如下一些功能。1、自动雨刷好用，这几天下雨，开自动跑高速无压力；2、H6带有220V电源（150w），不愧为旅行车。",
             "、一键折叠倒车镜。倒车有摄像头，右前盲区也有摄像头。4、有自动灯光，告诉过隧道，自动开启，昨天黄昏回家用自动，才知道自动的好处。5、车管所N多人上牌，居然没发现是柴油的。目前油耗6.9 2014年7月21日 收到汽车之家“金属质感车标” ",
             "2014年7月27日 云南旅游回来，全程1640公里，用柴油100.24升，5人全程空调；隧道自动灯光、途中部分路段遇到下雨，自动雨刷会开启，还学会玩手动档的巡航。晚上回家仪表灯有些刺眼，一路不爽，开始骂长城，途中加油站上网查询，才知道调仪表灯亮度的方法，唉！错怪长城了。6月6号出厂的车，7月7号买的车，感觉这车良心车，朋友都说车好，没有异味",
             "味道还很大。准备去做地盘装甲，用手机弯下去拍照，发现出厂时候已经有装甲了。赞一个，真的可以"
             ]
# documents = [u"一年了，目前没有什么故障，也没有他们说的国产车小故障多；洗干净车还是很新的。个人平时开车很小心、停车也注意，没有刮擦过【吐槽】保险要到期了，天天收到保险公司的电话，烦人的保险公司。对这车还是比较满意的。",
#              u"目前的油费统计一下 总加油量：917.44L|总加油金额：6095元|总天数：375天|平均油耗：7.05L|平均油费:0.48元/公里 我还会继续追加口碑的"]


# stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
# print stopwords


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

                obj_s.append(delNOTNeedWords(object_dict[fieldname])[1])
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
        if (word not in customstopwords and flag[0] in [u'n', u'f', u'a', u'z']):
            # ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
            return_words.append(word.encode('utf-8'))
    return result,return_words

# texts = [[word for word in jieba.lcut(delstopwords(document))] for document in documents]
texts = json_dict_from_file('/home/wac/data/hotWeibo_9200.json','content')
dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]  # 生成词袋
tfidf = models.TfidfModel(corpus)
copurs_tfidf = tfidf[corpus]
lda = models.LdaModel(copurs_tfidf, id2word=dictionary, num_topics=20)
print(lda.print_topics(1)[0][1])
print(lda.print_topics(2)[0][1])


#句子聚类
corpus_lda = lda[copurs_tfidf]
index = similarities.MatrixSimilarity(corpus_lda)
# sort_sims = sorted(enumerate(corpus_lda), key=lambda item: -item[1])
temparray =  [[] for i in range(20)]
result = []
# np.ndarray()
for id,doc in enumerate(corpus_lda):
    for docid,item in enumerate(doc):
        item = list(item)
        item[0] = id
        item = tuple(item)
        temparray[docid].append(item)
    # print doc
sort_sims = sorted(temparray[0], key=lambda item: -item[1])
print sort_sims
print documents[sort_sims[0][0]]
sort_sims = sorted(temparray[1], key=lambda item: -item[1])
print sort_sims
print documents[sort_sims[0][0]]
sort_sims = sorted(temparray[2], key=lambda item: -item[1])
print sort_sims
print documents[sort_sims[0][0]]