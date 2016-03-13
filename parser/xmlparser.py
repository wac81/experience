# -*- coding:utf-8 -*-

# Element.iter(tag=None)：遍历该Element所有后代，也可以指定tag进行遍历寻找。
#
# Element.findall(path)：查找当前元素下tag或path能够匹配的直系节点。
#
# Element.find(path)：查找当前元素下tag或path能够匹配的首个直系节点。
#
# Element.text: 获取当前元素的text值。
#
# Element.get(key, default=None)：获取元素指定key对应的属性值，如果没有该属性，则返回default值。
#
# 第二个是ElementTree对象，获取方法
# tree=ET.parse(文件或者xml字符串),
#
# tree即ElementTree对象，常用的方法有
#
# getroot() ：获取根元素
#
# find(match) :找到顶层的第一个和match配对的元素
#
# findall(match): 找到所有匹配的子元素
#
# 第三个是Element对象，即元素，也是最重要的
# ElementTree调用函数的返回值通常是Element元素，其常用的方法有
#
# tag: 获取tag值
#
# text ：获取元素的文本内容
#
# attrib :获取元素的属性，通常是字典数据类型，上边提到过，如{"ID":"07509876"}
#
# getchildren() :获取元素的子元素


# 当要获取属性值时，用attrib方法。
# 当要获取节点值时，用text方法。
# 当要获取节点名时，用tag方法。

import xml.etree.cElementTree as ET

tree = ET.ElementTree(file='/home/wac/data/zhwiki-20160203-pages-articles-multistream.xml')

#得到第一个匹配country标签的Element对象
# text = tree.find("country")
# print text
# for sub_tag in text:
#         print sub_tag.text
for elem in tree.findall('text'):
    print elem.tag, elem.attrib
    print elem.text
