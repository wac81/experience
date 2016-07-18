# -*- coding:utf-8 -*-
import tushare as ts

f = ts.get_hist_data('600848') #一次性获取全部日k线数据


#一次性获取当前交易所有股票的行情数据
import tushare as ts

f = ts.get_today_all()