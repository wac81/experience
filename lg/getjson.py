# -*- coding: utf-8 -*-
__author__ = 'ancheng'
import json

with open("./sss.json", "r") as f:
    for l in f:
        d = json.loads(l,encoding='utf-8')
