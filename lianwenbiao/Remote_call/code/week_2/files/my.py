# encoding:utf-8

"""
File: test_py.py
Author:  Charles Yee
Date: 2017/7/19
Version: python 2.7.13
Desc:
"""

from nltk.stem import WordNetLemmatizer

if __name__ == '__main__':
    word = 'Officers'
    ler=WordNetLemmatizer()
    print ler.lemmatize(word)
