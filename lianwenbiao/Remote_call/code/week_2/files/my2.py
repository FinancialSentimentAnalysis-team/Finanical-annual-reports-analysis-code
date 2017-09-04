# encoding:utf-8

"""
File: my2.py
Author:  Charles Yee
Date: 2017/7/20
Version: python 2.7.13
Desc:
"""
import treetaggerwrapper

tagger = treetaggerwrapper.TreeTagger(TAGDIR="D:\intern\\nlp\\tools\\tree-tagger-windows-3.2\TreeTagger")

s = "1996".decode("utf-8")
print s.isdigit()

tags = tagger.tag_text("september".decode("utf-8"))
for tag in tags:
    print tag.split()[2]
