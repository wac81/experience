import urllib,urllib2

url = 'http://image.sinajs.cn/newchart/daily/n/%s.gif'


# 600004  603999   sh
stock_code_start_sh = 600004
stock_code_end_sh = 603999

# 000002  002815   sz
stock_code_start_sz = 2
stock_code_end_sz = 2815

min_headers_size = 10

stock_codes_sh = [code for code in range(stock_code_start_sh, stock_code_end_sh)] #603996

stock_codes_sz = [code for code in range(stock_code_start_sz, stock_code_end_sz)]

# for code in stock_codes_sh:
#     if len(str(code)) < 6:
#         code = ''.join('0' for _ in range(6 - len(str(code)))) + str(code)
#
#     img = urllib2.urlopen(url % ('sh' + str(code))).read()
#     if len(img) < min_headers_size:
#         continue
#     with file('data_raw/sh'+str(code) + '.jpg', "wb") as f:
#         f.write(img)
#
#
#         # urllib.urlretrieve(url % ('sh'+str(code)), 'data_raw/sh'+str(code) + '.gif')  # s=urllib.urlretrieve(url,path)
#
#
# for code in stock_codes_sz:
#     if len(str(code)) < 6:
#         code = ''.join('0' for _ in range(6 - len(str(code)))) + str(code)
#     img = urllib2.urlopen(url % ('sz' + str(code))).read()
#     if len(img) < min_headers_size:
#         continue
#     with file('data_raw/sz'+str(code) + '.jpg', "wb") as f:
#         f.write(img)
#
#
#
#
# # delete file size equal zero
import os
filePath = './data2'
# filePath = './sh600230.gif'
# for parent ,dirnames , filenames in os.walk(filePath):
#     for filename in filenames:
#         if os.path.getsize(os.path.join(filePath, filename)) == 0:
#             os.remove(os.path.join(filePath, filename))



# convert gif to jpg
from PIL import Image
for parent ,dirnames , filenames in os.walk(filePath):
    for filename in filenames:
        im = Image.open(os.path.join(filePath, filename))
        print filename
        try:
            im.convert('RGB').save(os.path.join(filePath, filename), 'JPEG')
        except:
            os.remove(os.path.join(filePath, filename))
