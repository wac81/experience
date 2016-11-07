# -*- coding:utf-8 -*-

import codecs
import math
import novel_sentiment

novelName = 'data/yanzhiyoudu'
#将小说读入内存数据结构
listSentence = []
i = 0
for line in codecs.open(novelName + '.txt','r','utf-8').readlines():
    i += 1
    print str(i)
    if line.strip() != '':
        listSentence.append(line.strip())
#每10行合为一行
listPoint = []
currPoint = ''
for curri in range(len(listSentence)):
    if curri % 10 == 0:
        if currPoint != '':
            listPoint.append(currPoint)
        currPoint = ''
    else:
        currPoint += listSentence[curri]
#将格式化后的小说写入文件，并将每行的情感值写入文件。
fow = codecs.open(novelName + '_format.txt', 'w', 'utf-8')
fow1 = codecs.open(novelName + '_sent_result1.txt', 'w', 'utf-8')
fow2 = codecs.open(novelName + '_sent_result2.txt', 'w', 'utf-8')
for currPoint in listPoint:
    currScore = novel_sentiment.sentiment(currPoint)
    #过滤情感不强烈的行
    if currScore > -3.0 and currScore < 1.0:
        continue
    else:
        fow.write(currPoint.replace('\n',''))
        fow.write('\n')
        fow1.write(str(currScore))
        fow1.write('\n')
        fow2.write(str(math.fabs(currScore)))
        fow2.write('\n')
fow.close()
fow1.close()
fow2.close()
