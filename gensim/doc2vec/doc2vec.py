# -*- coding:utf-8 -*-
# gensim modules
from gensim import corpora, models, similarities
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import re
import codecs
import jieba.posseg as pseg
stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
modelfilename = 'doc2vec.model'
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
        if (word not in customstopwords and len(word)>0 and flag in [u'n',u'nr',u'ns',u'nt',u'nz',u'ng',u't',u'tg',u'f',u'v',u'vd',u'vn',u'vf',u'vx',u'vi',u'vl',u'vg', u'a',u'an',u'ag',u'al',u'm',u'mq',u'o',u'x']):

            # ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
            return_words.append(word.encode('utf-8'))
    return result,return_words
class DirOfPlainTextCorpus(object):
    # SPLIT_SENTENCES = re.compile("[.!?:]\s+")

    def __init__(self, dirname):
        self.dirname = dirname
        # self.tagedDocs = None

    def __iter__(self):
        if os.path.isfile(self.dirname):
            for uid, line in enumerate(open(self.dirname)):
                yield TaggedDocument(delNOTNeedWords(line)[1], ['sentence'+str(uid)])
        else:
            for fn in os.listdir(self.dirname):
                for uid, line in enumerate(open(os.path.join(self.dirname, fn))):
                    yield TaggedDocument(delNOTNeedWords(line)[1], ['sentence'+str(uid)])



filename = 'smzdm_one.txt'
limit = 0.6
model = Doc2Vec(DirOfPlainTextCorpus(filename),size=10, window=3, min_count=3, workers=4,min_alpha=0.002)


model.save(modelfilename)

#########新句子查询相似度
doc = u'这牛奶价格高'
inf_vec = model.infer_vector(delNOTNeedWords(doc)[1])
sims = model.docvecs.most_similar([inf_vec])
print sims

lines = []
for line in open(filename):
    lines.append(line)

for s in sims:
    if s[1] > limit:
        print lines[s[0]]
#########

#########训练集内部句子查询相似度
docvec = model.docvecs[14]  #两种表达方式
docvec = model.docvecs['sentence14']    #两种表达方式
sims = model.docvecs.most_similar([docvec])
print sims
