from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

es = Elasticsearch()
# es = Elasticsearch([{u'host': u'127.0.0.1', u'port': 9200}])
ses = SignatureES(es)

# ses.add_image('http://i3.s2.dpfile.com/pc/90444b48dbad1e94ed6c60d907554c24%28700x700%29/thumb.jpg')
ses.add_image('./image_database/1.jpg')
ses.add_image('./image_database/2.png')
ses.add_image('./image_database/3.jpg')
ses.add_image('./image_database/4.jpg')
ses.add_image('./image_database/5.jpg')
ses.add_image('./image_database/6.jpg')


# ses.add_image('http://life.gd.sina.com.cn/ul/2008/1126/U1425P697DT20081126183443.jpg')
# ses.add_image('http://i3.s2.dpfile.com/2010-11-15/5838770_b.jpg%28240c180%29/thumb.jpg')
# print ses.search_image('http://www.chinapp.com/uploadfile/2014/1113/20141113111459375.jpg')
print ses.search_image('./image_database/3.jpg')


# print ses.search_image('https://upload.wikimedia.org/wikipedia/commons/e/e0/Caravaggio_-_Cena_in_Emmaus.jpg')