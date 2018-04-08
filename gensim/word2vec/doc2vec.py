# -*- coding:utf-8 -*-
from gensim import models
# gensim .models.Word2Vec
import jieba, gensim
import multiprocessing
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
TaggededDocument = gensim.models.doc2vec.TaggedDocument

save_filename = 'doc2vec.model'
sentences = [
    u'还记得上次放出的奔驰GLE vs 奥迪Q7 vs 路虎揽胜运动版 vs 雷克萨斯RX vs 保时捷卡宴 vs 宝马X5静态测评篇么？动态测评戳这里→',
    u'【格策与杰森斯坦森体验奥迪试驾】日前拜仁球星格策前往奥地利基茨比厄尔，体验奥迪试驾活动，他也在这里遇到了国际著名影星杰森·斯坦森，两人一道享受了驾驶奥迪驰骋雪地的畅快。',
    u'由一汽-大众奥迪与腾讯强强联手，动感时尚的奥迪A3强力助阵，致力于打造青春激扬的潮流视听盛宴。作为盛会的主角之一，奥迪A3极致践行未来科技，流畅动感的操控体验，触碰未来，就在此时此刻。尊享会独播预约戳：',
    u'2016，海关又有大动作，罚没物资将以更公平、公正、公开的网络拍卖方式处置。今早10点，24辆大连海关罚没车在@淘宝拍卖会 进行网络首拍，引来众多消费者关注。受关注最多的是57万起拍的卡宴和44万起拍的奥迪Q7。据悉，此次拍卖将持续到14日早上10点。',
    u'今夜有个孬子数着奥迪的标志问是不是奥运五环',
    u'今天带溪坐出租 没见过手柄式的车窗开关 一直使劲弄 我说你给人车弄坏了人家叔叔要你把爸的车拿来换 立马回答我说不行 后来她丹姨问她我家车跟你家的车换换吧？ 想都不想就说不换 她丹姨说 擦！还看不上咱家奥迪咧[泪] 哎！傻孩子啊 她家车可以换你爹两车了',
    u'祝设计一部每位设计师2016年业绩过200万，做首席，开奥迪。特别谢谢我们最最敬爱的“吴刚”经理，辛苦了！',
    u'其实我是个哑巴，平时说话都是伪装的 2、医生叫我多进行光合作用，不要熬夜了。3、最低奋斗目标：农妇 山泉 有点田。4、开奥迪,穿迪奥,没事就吃奥利奥 5、水至清则无鱼，人至贱则无敌。6、每个成功的男人背后，都会有一个吃饱了没事做的女人。。。',
    u'#奥迪时刻#你心中最理想的未来奥迪车是什么样的？根据空气动力学的设计思想，一群大学生们脑洞大开，通过将木质材料与奥迪车身线条结合，创作了极具视觉震撼力的奥迪未来车模型。学生们个性鲜明的设计在呈现了一场华丽的视觉盛宴的同时，也让人们对未来奥迪车型有了更多期待。',
    u'日了狗了以后有钱也不买奥迪',
    u'打滴滴专车，和司机一路神聊。得知，所谓运管钓鱼执法滴滴司机，每天罚没5/6千万。说的比较凶的是前天西站，一奥迪司机拒不下车接受处罚，车玻璃被直接砸了。一运管协管的被司机咬断指头，更有未报的中关村运管罚的兴起，却被抵當家底出来做滴滴的司机白刀入红刀一刀封喉的传说',
    u'奥迪h-tron quattro最新概念设计图曝光。',
    u'朵女郎姐妹花做清清裤三个月 一人一辆奥迪到手[强][强]加入朵女郎 买车很任性[鼓掌][鼓掌]相信的就赶紧跟我干#朵女郎清清裤#',
    u'好吧，刚才文字知道你们不好意思转。德国优秀娱乐汽车节目GRIP带你直击保时捷，宝马，大众秘密车库 。ps 明还有奥迪，欧宝，福特，雪铁龙。',
    u'今天去厦门事情没办成，却把别人的奥迪给撞了。晚上要去剪头发，又没剪成，忙到刚完回来，倒霉的一天，现在喝一杯热牛奶压压惊',
    u'【2015[同意]款奥迪 S3 Cabriolet 敞篷版官图发布】新车搭载2.0升TFSI涡轮增压四缸发动机，最大功率300马力，峰值扭矩380Nm，整重1620kg，破百5.4秒，百公里平均油耗7.1升，新车将在日内瓦车展首发，售价48500欧元起，折合人民币40.5万元',
    u'前方奥迪司机开远光配合哈士奇给我来了个大[doge]沃日。你们都能想象到什么了吧',
    u'据说奔驰，宝马，奥迪都会用的车子空气净化器，他到底长得什么样的！猛戳进来细细看看，真不敢相信还有这么给力的活动【1月23日-26日上市活动，99元彪悍价格】速来围观，抢到手才是自己的！',
    u'【新一代奥迪Q3问世】目前的测试车仍裹上了一层伪装，但从暴露出来的头灯可以看到，新设计的灯腔很新颖，而且这应该是一套作为选配的全LED头灯组。因为考虑到新一代A3都已经可选配全LED头灯，改款Q3肯定也不会落伍。',
    u'【13奥迪A7/3.0T】黑色黑内，无匙进入，无匙起动，座椅加热，手自一体，倒车影像，前后电眼，后尾翼，全时四驱，后独立空调',
    u'日本明星出水麻衣，非常清纯的童颜巨乳MM,喜欢的宅男很多哦~~~班路上，千里车流，万里人潮。望大街内外，车行如龟，司机烦躁，一步不动，总是红灯憋出niao。交通如此多焦，引无数大款上公交。惜奥迪A6，慢如蜗牛。奔驰宝马，无处发飙。一代天骄，兰博基尼，泪看电驴儿把车超。',
    u'奥迪A1 1.4T刷ECU，这车采用最新EA211发动机高功率版本程序，通过我们ECU调教后车子油门反应速度灵敏，推背感明显比原来增强，加速更直接[赞]',
    u'买的白色，外观秀气，适合女孩子开。方向盘小巧精致适合女孩子开。加速不错，减震还行，开高速不飘。起步肉。总体很满意',
    u'人和车的缘分大概就像人和人的缘分一样吧 说不出太多的好 甚至说不出口的喜欢，但就是买了三星半是因为我买完就降价好多 再给我一次机会 不知道会不会选择cc 尚酷或者凯迪拉克，或者换成1.8t ~~~ 毕竟没体验过~~~',
    u'我见过最有用的团队激励方式是，每个月老板都会带领全体员工去各个4S店转转，从奔驰宝马奥迪转到长城比亚迪奇瑞。[吃惊][吃惊]特别有效果。',
    u'''1月22日，具体说是今日晚间，一汽-大众奥迪新款A6L将正式宣布上市，新款车型在设计上有一定的变化，最大的看点是在动力总成上有较大的调整，用1.8T发动机将取代现款的2.0T发动机，用3.0T低功率发动机取代2.8L自吸发动机。另外，同时上市的还有奥迪新款S6车型。
　　小贴士：A6L是奥迪在华的行政级豪华座驾；主打公商务用车市场



　　作为中期改款车型，新款奥迪A6L在外观上的变化并不十分明显，主要是前大灯、后尾灯、前脸以及排气管等细节有调整。前脸延续了经典的六边形进气格栅，大气沉稳。仔细看，新款车型前包围造型有一定的改变，中网格栅与保险杠下唇采用分层设计，让前脸更加有层次感。



　　前脸最大的亮点是前大灯的改变，换上了新样式的LED日间行车灯，灯带的造型非常时尚。根据配置的高低不同，新车将有LED大灯、LED矩阵大灯以及氙气大灯可选。



　　新 款车型车尾的变化很小，后备箱盖下方增加了一条镀铬饰条，并且对排气管的样式进行了调整，现款A6L的排气管均为圆筒状，而新款则改为扁平状，运动感会更 强一些。采用了全新样式的LED尾灯灯组，转向灯点亮时LED灯组会从内之外依次点亮，形成流动般的效果，很有科技感。



　　新款A6L车身尺寸上也有些许的调整，新车的长宽高分别为5036×1874×1466（mm），轴距为3012mm。车身长度、高度分别比之前增加了21mm、11mm，宽度和轴距则与现款保持一致，这些变化主要因为车身包围的设计改变所导致。



　　内饰方面，设计没有太大的改变，运动版车型搭载的三辐方向盘相比普通版本的四辐方向盘要年轻一些，并且带有换挡拨片。新款车型采用了全新的挡把样式，据说更符合人体工程学。





　　MMI多媒体系统依然采用8英寸显示屏，不过显示核心升级为NVIDIA Tegra 3四核处理器，显示效果更流畅。另外新车增加了车载移动网络，插入SIM卡就可以上网。系统还自带移动热点，为手机提供Wi-Fi上网功能。



　　动力总成方面，新款奥迪A6L的调整最为明显。TFSI三款车型搭载的是一台1.8TFSI涡轮增压发动机，其最大输出功率为190Ps/4200-6200rpm，峰值扭矩为320Nm/1400-4100rpm；30 FSI车型配备的是2.5L V6自然吸气发动机，其最大输出功率为204Ps/6000-6500rpm，峰值扭矩为250Nm/3000-4750rpm。传动系统与1.8TFSI发动机匹配的是7速双离合变速箱，与2.5L V6发动机匹配的是CVT变速箱。



　　





　　新款奥迪A6L取消了2.8L自然吸气发动机，取而代之是的3.0T低功率发动机。45 TFSI quattro与50 TFSI quattro车型均搭载的是3.0T机械增压发动机，低功率版最大输出功率为272Ps/4780-6500rpm，峰值扭矩为400Nm /2150-4780rpm，高功率版最大输出功率为333Ps/5500-6500rpm，峰值扭矩为440Nm/2900-5300rpm。传动系统 与发动机匹配的是7速双离合变速箱。

　　编辑点评：奥迪新款A6L在外观和内饰上的变化相对较小，最大的看点在于其换装的新动力总成，在动力输出上没有变化，但具有更好的燃油经济性，而且降低了新款A6L的价格门槛，对新车在2016年的市场表现是一个利好！''',
    u'''有一种浪漫叫：奥迪宝马都做不到！
2016年1月23日 23:22 阅读 13498
　　最近流行着一种浪漫，叫奔驰怀挡情怀！
　　▼

　　作为一个有情怀的德系汽车品牌（咳咳...），早期进入国内的奔驰也采用过传统的换档杆，但奔驰估计是为了不愿放弃老祖宗留下来的好东西，把一向引以为豪的“怀挡”设计情怀给继承了下来，目前奔驰在国内的全系几乎所有车型都覆盖了怀挡，这已经成了奔驰的一大特色，不过这也意味着奔驰车在国内也就没手动挡了。

　　奔驰是卖情怀还是装逼，为什么奔驰会这么做呢？据说号称是节约中间那一点空间，问题是那上面又不能坐人，节约个毛。

　　不过也有很多人质疑奔驰怀档如果误操作咋办？砖家是这么说的：怀档有时速限制，高于一定速度就无法换挡，而且最重要的是怀挡从行进的D档到驻车P档，只需要轻按一下，注意是一下，一个挂档动作......而排档从行进D档到驻车P档则需要跨过空挡N，倒档R，最后再到驻车P......怀挡一个步骤就完成的动作，还有撒好纳闷的。

　　但是德系BBA，奔驰另外两个兄弟宝马和奥迪，却一直坚持着用排档。

　　知道为什么奔驰与宝马、奥迪不同！坚持采用怀挡设计吗？因为奔驰才是男人的车，奔驰对“人性的释怀与客户的需求”探索到了极致。

　　不愧为奔驰大哥，现在才发现奔驰的怀档优势，才恍然奔驰的良苦用心，公社君还是太年轻了。

　　但是也有妹纸表示严重不服，奔驰也可以是女人的车，这是奔驰妹纸的态度！

　　文艺君彻底被奔驰的怀挡征服了，攒钱买大奔去！'''

]

import codecs
import jieba.posseg as pseg
stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
# print stopwords
feature_size = 100
content_window = 10
freq_min_count = 1
threads_num = 4
negative = 2   #best
iter = 1

def delNOTNeedWords(content,stopwords):
    # words = jieba.lcut(content)
    result=''
    # for w in words:
    #     if w not in stopwords:
    #         result += w.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词

    words = pseg.lcut(content)

    for word, flag in words:
        # print word.encode('utf-8')
        if (word not in stopwords and flag[0] in [u'n',u'f',u'a',u'z']): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    return result

documents = []
# y = np.concatenate(np.ones(len(docs)))
for i, text in enumerate(sentences):
    # word_list = text.split(' ')
    text = delNOTNeedWords(text, stopwords)
    word_list = jieba.lcut(text)
    l = len(word_list)
    document = TaggededDocument(word_list, tags=[i])
    documents.append(document)


# bigram_transformer = models.Phrases(input)
model = models.Doc2Vec(documents, size=feature_size, window=content_window, min_count=freq_min_count, negative=negative, iter=iter, workers=multiprocessing.cpu_count())
# print model.index2word
model.save(save_filename)
f = model.most_similar([u'奥迪'])
for k in f:
    print k[0].encode('utf-8'),k[1]