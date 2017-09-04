# encoding:utf-8

"""
File: my4.py
Author:  Charles Yee
Date: 2017/7/21
Version: python 2.7.13
Desc:
"""

import os
import re


def func_1():
    ss = "HK$’000  "
    tmp = re.sub(r"[^A-Za-z0-9]", '', ss)
    print tmp

    if re.search("HK\d", tmp):
        print "Yes"
    else:
        print "No"


def func_2():
    ss = "HK ’000"
    if re.search("HK\s+’\d+", ss):
        print "Yes"
    else:
        print "No"


def func_3():
    tmp = "Chairman’s “dsfdsfsfs”Statement “Freedom”"
    tmp = re.sub("“|”", "\"", tmp)

    print tmp


def func_4():
    tmp = "“Freedom”Chairman’s Statement".decode('utf-8')
    line_content = re.sub(r"[^A-Za-z0-9,.’]", ' ', tmp).strip()
    print line_content


def func_5():
    path = "e:"
    if os.listdir(path):
        print "Yes"


if __name__ == '__main__':
    func_5()
