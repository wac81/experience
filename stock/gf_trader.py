#coding=utf8
'''
广发证券必须安装pytesseract，用于验证
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