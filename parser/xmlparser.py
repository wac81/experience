# -*- coding:utf-8 -*-
import xml.etree.cElementTree as ET

tree = ET.ElementTree(file='/home/wac/data/2.xml')

#得到第一个匹配country标签的Element对象
text = tree.find("country")
print text

for sub_tag in text:
        print sub_tag.text
for elem in tree.iter('country'):
    # if 'text' in elem.tag:
    print elem.tag, elem.attrib
        # print elem.attri
# root = tree.getroot()
#
# print (root.tag, root.attrib)