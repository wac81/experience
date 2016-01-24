# 去停用词

import codecs
import jieba.posseg as pseg
stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
# print stopwords

def delNOTNeedWords(content,stopwords):
    # words = jieba.lcut(content)
    result=''
    # for w in words:
    #     if w not in stopwords:
    #         result += w.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词

    words = pseg.lcut(content)

    for word, flag in words:
        # print word.encode('utf-8')
        if (word not in stopwords and flag not in ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    return result