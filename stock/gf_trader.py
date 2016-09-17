#coding=utf8
'''
广发证券必须安装pytesseract，用于验证
a、Python-tesseract支持python2.5及更高版本；  sudo pip install pytesseract

b、Python-tesseract需要安装PIL（Python Imaging Library） ，来支持更多的图片格式；sudo apt-get install python-imaging
mac:sudo port install tesseract  or brew install tesseract

c、Python-tesseract需要安装tesseract-ocr安装包。sudo apt-get install tesseract-ocr

'''
import easytrader
import os
import json
path = os.path.dirname(os.path.abspath(__file__))


from io import open

# def file2dict(path):
#     with open(path, encoding='utf-8') as f:
#         return json.load(f)
#
# j = file2dict(os.path.join(path,'gf.json'))


user = easytrader.use('gf')

user.prepare(os.path.join(path,'gf.json'))
print user.balance
# user.buy(SH600027)