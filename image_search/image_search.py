from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

es = Elasticsearch()
# es = Elasticsearch([{u'host': u'127.0.0.1', u'port': 9200}])
ses = SignatureES(es)

# ses.add_image('http://i3.s2.dpfile.com/pc/90444b48dbad1e94ed6c60d907554c24%28700x700%29/thumb.jpg')
# ses.add_image('./image_database/1.jpg')
# # ses.add_image('./image_database/2.png')
# ses.add_image('./image_database/3.jpg')
# ses.add_image('./image_database/4.jpg')
# ses.add_image('./image_database/5.jpg')
# ses.add_image('./image_database/6.jpg')

# ses.add_image('http://www.shslsygs.com/u/19/T1LcaiFclcXXXXXXXX_%21%210-item_pic.jpg')
# ses.add_image('http://o4.xiaohongshu.com/discovery/w640/df5312e38c884eba42c2d9dd678687d8_640_640_92.jpg')
# ses.add_image('http://img1.mpimg.cn/large/2013/12/5/9d7f8b91-cf52-4c17-a507-c82edf0de0ea.jpg')
# ses.add_image('http://s.wasu.tv/mams/pic/201412/23/06/20141223062553589e32fa6e7.jpg')
#
# ses.add_image('http://www.chinapp.com/uploadfile/2014/1113/20141113111459375.jpg')
# ses.add_image('http://qcloud.dpfile.com/pc/LIJMqt4nechuCZI4J_jx0m9-ePQAZ_OnmJBM0Zw9SxQiqVcQhdSu6R9ktTgdkBrRTYGVDmosZWTLal1WbWRW3A.jpg')
# ses.add_image('http://new-img1.ol-img.com/122/308/liVgJf6PeLgag.jpg')
#
#
# ses.add_image('http://pic13.997788.com/pic_search/00/26/88/70/se26887098.jpg')


# k = ses.search_image('http://gdgs.chinaxinge.com/uploadfile/200812/20081224234731808.jpg')
#
# print k


# ses.add_image('http://life.gd.sina.com.cn/ul/2008/1126/U1425P697DT20081126183443.jpg')
# # ses.add_image('http://i3.s2.dpfile.com/2010-11-15/5838770_b.jpg%28240c180%29/thumb.jpg')
# print ses.search_image('http://www.chinapp.com/uploadfile/2014/1113/20141113111459375.jpg')
print ses.search_image('./image_database/3.jpg')


# print ses.search_image('https://upload.wikimedia.org/wikipedia/commons/e/e0/Caravaggio_-_Cena_in_Emmaus.jpg')