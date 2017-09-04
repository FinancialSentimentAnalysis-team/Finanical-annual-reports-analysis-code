# encoding:utf-8

"""
File: py5.py
Author:  Charles Yee
Date: 2017/7/21
Version: python 2.7.13
Desc:
"""
import csv
import os
import re
import string
import sys

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding('utf-8')

prep = ['at', 'in', 'of', 'by', 'about', 'for', 'from', 'except', 'since',
        'near', 'with', 'Inside', 'outside', 'onto', 'into', 'throughout',
        'without', 'unpon', 'above', 'across', 'after', 'along', 'among',
        'around', 'before', 'behind', 'below', 'beneath', 'beside', 'between',
        'beyond', 'down', 'off', 'on', 'over', 'through', 'to', 'towards',
        'under', 'up', 'within', 'as', 'during', 'past', 'till', 'until']
pronoun = ['I', 'me', 'we', 'us', 'my', 'myself', 'ourselves', "i'm",
           'he', 'she', ' his', 'her', 'they', 'them', 'himself',
           'themselves', 'herself', 'their', 'it', 'its', 'itself',
           'that', 'those', 'these', 'this', "it's", 'you', 'your',
           'yourself', 'yourselves', 'all', 'any', 'another', 'both',
           'each', 'every', 'either', 'every', 'few', 'little', 'many',
           'much', 'no', 'none', 'neither', 'one', 'other', 'some']
article = ['a', 'an', 'the']
be_verb = ['is', 'am', 'are', 'was', 'were', 'being', 'been']


def load_corpus(corpus_root):
    corpus_reader = PlaintextCorpusReader(corpus_root, '.*\.txt')
    file_list = corpus_reader.fileids()
    return corpus_reader, file_list


def filter_punctuation(finder):
    """
    过滤词汇中的标点符号或者长度小于1的词汇
    :param finder: BigramCollocationFinder
    :return: BigramCollocationFinder
    """
    # 这一步有问题
    finder.apply_word_filter(lambda w: len(w) == 1
                                       or len([char for char in w if char in string.punctuation]) > 0)
    return finder


def Bigrams_freq(tokens):
    """
    计算双连词频率
    :param tokens:
    :return:
    """
    # 建立双连词 finder
    finder = BigramCollocationFinder.from_words(tokens)

    # 去掉标点符号
    finder = filter_punctuation(finder)

    # 排序 先按频率排，再按字母字典序排
    bi_collocations = sorted(finder.ngram_fd.items(),
                             key=lambda t: (-t[1], t[0]))
    return bi_collocations


def Trigrams_freq(tokens):
    """
    计算三联词频率
    :param tokens:
    :return:
    """
    finder = TrigramCollocationFinder.from_words(tokens)
    finder = filter_punctuation(finder)
    tri_collocations = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    return tri_collocations


def filter_stop_words(data):
    """
    过滤停用词 包括双连词和三联词
    :param data: 数据
    :return:
    """
    stop_word = stopwords.words('english')
    flag = True

    # filter eg:cid cid cid
    # 过滤掉重复的连词
    if len(set(data)) == 1:
        flag = False

    # filter eg: an_th_xv
    # 过滤掉最大长度不超过3的连词
    elif max([len(e) for e in data]) < 3:
        flag = False

    # 只要出现代词和介词就过滤
    elif len([e for e in data if e in pronoun or e in prep]) > 0:
        flag = False
    elif len([e for e in data if e in be_verb]) > 0:
        flag = False
    # bigram 只要出现冠词就过滤
    elif len(data) == 2 and len([e for e in data if e in article]) > 0:
        flag = False
    # trigram 不在首位出现的冠词直接过滤
    elif len(data) == 3 and (data[-1] in article or data[-2] in article):
        flag = False

    # 数字或者数字开头过滤
    elif len([e for e in data if re.match("\d+(th|st|nd|rd|hk)*$", e)]) > 0:
        flag = False
    # 是mr或者ms直接过滤
    elif len([e for e in data if re.match("(mr)|(ms)", e)]) > 0:
        flag = False

    return flag


def save_into_csv(data, result_path):
    """
    存到 csv 文件中
    :param data:
    :param result_path:
    :return:
    """
    print 'start to handld %s' % result_path
    with open(result_path, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['collocations', 'frequency'])
        for key, value in data.items():
            # 过滤停用词
            if filter_stop_words(key):
                writer.writerow(['_'.join(key), value])
    f.close()
    print 'create %s successfully' % result_path


def process_root(c_root):
    """
    加载语料，计算双连词和三联词，最后存储于csv文件
    :param c_root:
    :param result_path_bi_root:
    :param result_path_tri_root:
    :return:
    """
    corpus_reader, file_list = load_corpus(c_root)
    bi_dict = nltk.defaultdict(int)
    tri_dict = nltk.defaultdict(int)

    for f in file_list:
        tokens = corpus_reader.words(f)
        tokens = [token.lower() for token in tokens]

        bi_collocations = Bigrams_freq(tokens)

        for e in bi_collocations:
            bi_dict[e[0]] += e[1]

        tri_collocations = Trigrams_freq(tokens)
        for e in tri_collocations:
            tri_dict[e[0]] += e[1]

    csv_paths = "/".join(c_root.split("/")[:5]) + "/csv_files"
    if not os.path.exists(csv_paths):
        os.makedirs(csv_paths)

    bi_csv_name = csv_paths + "/" + c_root.split("/")[6] + "_" + c_root.split("/")[7] + "_bi_gram.csv"
    ti_csv_name = csv_paths + "/" + c_root.split("/")[6] + "_" + c_root.split("/")[7] + "_ti_gram.csv"

    try:
        save_into_csv(bi_dict, bi_csv_name)
        save_into_csv(tri_dict, ti_csv_name)
    except Exception, msg:
        print msg


def process(stock_no, period):
    txt_path = "F:/xunlei/CharlesYee/financial_reports" \
               "/" + stock_no + "/filter_files/"

    year_list = os.listdir(txt_path)

    for year in year_list:
        # 不可累加
        # txt_path = txt_path + year + "/" + period
        txt_path_in = txt_path + year + "/" + period

        # 防止出现缺失 Annual 或者 Interim
        if not os.path.exists(txt_path_in):
            continue

        process_root(txt_path_in)


if __name__ == '__main__':
    # process("00590", "Annual")
    # process("00590", "Interim")
    #
    process("00001", "Annual")
    process("00001", "Interim")
