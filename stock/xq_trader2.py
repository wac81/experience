#coding=utf8
import easytrader

user = easytrader.use('xq')
user.prepare('xq.json')
print user.balance
# user.buy(SH600027)