#coding=utf8
from api import *
from webtrader import WebTrader
from cli import *
from httpserver import *

def copy(path):
    c = read_file(path)
    with open(path, 'wb') as f:
        f.write(c)

def initialize(context):
    user = use('xq')
    user.prepare('xq.json')
    # 打印持仓、资金状况
    log.info(user.position)
    log.info(user.balance)