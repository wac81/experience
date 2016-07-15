# -*- coding: utf-8 -*-
# create by wuancheng
# test proxy ip is OK
import httplib2
import json

testurl = u"http://baidu.com"
proxylist_location = u"./proxylist.txt"
pass_proxylist_location = u"./passproxylist.txt"
timeout = 5

class proxyitem(object):
    def __init__(self,object):
        # self.type = object[0]     # type
        self.ip = str(object[0])     # ip
        self.port = int(object[1].strip('\n'))     # post

def testProxy(proxyitem):
    http = httplib2.Http(proxy_info=httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, proxyitem.ip, proxyitem.port),timeout=timeout)
    try:
        resp, content = http.request(testurl, method='GET', headers={'cache-control':'no-cache'})
    except:
        print (proxyitem.ip + str(proxyitem.port) + 'time out or error \n')
        return False


    if (resp.status == 200):
        return True
    else:
        return False

with open(proxylist_location) as file:
    with open(pass_proxylist_location,'w') as writefile:
        for line in file:
            p = proxyitem(line.split(u':'))
            if testProxy(p):
                print (line+' pass \n')
                writefile.write(line)

