#coding=utf8
from api import *
from webtrader import WebTrader
from cli import *
from httpserver import *

def copy(path):
    c = read_file(path)
    with open(path, 'wb') as f:
        f.write(c)

def loading(context):
    ''' 登陆 '''
    global user
    user = use('xq')
    user.prepare('xq.json')

def initialize(context):
    g.security = ['600132.XSHG','600600.XSHG']
    run_daily(loading, 'before_open')
    run_daily(trade,'open')
    run_daily(check, 'after_close')

def trade(context):
    '''
    交易
    雪球组合的净值为1，easytrader使用1:1000000的比例放大。
    price*amout为雪球组合的改变比例。
    如下所示，如果price=10000，如果amount=1，比例则为1%；如果amount=10，比例则为10%
    '''
    user.buy(g.security[0][:6], price=10000, amount=1) #买入1%
    user.sell(g.security[1][:6], price=10000, amount=1) #卖出1%

def check(context):
    ''' 获取信息并输出 '''
    log.info('获取今日委托单:')
    log.info('今日委托单:', user.entrust)
    log.info('-'*30)
    log.info('获取资金状况:')
    log.info('资金状况:', user.balance )
    log.info('enable_balance(可用金额):', user.balance[0]['enable_balance'])
    log.info('-'*30)
    log.info('持仓:')
    log.info('获取持仓:', user.position)
    log.info('enable_amount(可卖数量):', user.position[0]['enable_amount'])