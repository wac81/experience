from gensim import corpora, models, similarities
import logging
import jieba
import codecs
import jieba.posseg as pseg

stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
flagList=['v','vd','vn','vshi','vyou','vf','vx','vl','vg','x','w','o','zg','uj','m','b','r','m','u','y','e','p','q','z','f']#停用词性
def delstopwords(content):
    stopwordSet = set(stopwords.split('\n'))
    result=[]
    words = jieba.posseg.cut(content)
    for i in words:
        flag=0#判断词性是否是否在flagList中
        if i.word not in stopwordSet : #去停用词和其他词性，比如非名词动词等
            for f in flagList:
                if f == i.flag:
                    flag+=1
        if flag==0:
            result.append( i.word)
            flag=0
    return result

# texts = [[word for word in jieba.lcut(delstopwords(document))] for document in documents]
def getWordCloud(documents):
    # texts = [delstopwords(document) for document in documents]
    # for i in texts:
    #     print(i)
    texts=[]
    for document in documents:
        if len(document)>1:#去空
            texts.append(delstopwords(document))
    if len(texts)<2:
        return u'数据太少'
    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]  # 生成词袋
    tfidf = models.TfidfModel(corpus)
    copurs_tfidf = tfidf[corpus]
    lda = models.LdaModel(copurs_tfidf, id2word=dictionary, num_topics=10)
    return (lda.show_topics(1)[0][1])