# encoding:utf-8

"""
File: my3.py
Author:  Charles Yee
Date: 2017/7/20
Version: python 2.7.13
Desc:
"""
import re

if __name__ == '__main__':
    line="home 34"
    print re.findall('([A-Za-z]+)\s+([0-9]+)', line)