# encoding:utf-8

"""
File: py3.py
Author:  Charles Yee
Date: 2017/7/20
Version: python 2.7.13
Desc:
"""
from nltk.corpus import PlaintextCorpusReader
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.book import FreqDist
from treetaggerwrapper import TreeTagger


def load_corpus(c_root, file_name=None):
    """
    加载自己的语料
    :param c_root:语料文本所在的地址
    :return: PlaintextCorpusReader 文本名列表
    """
    # 指定需要加载文本的目录及文件类型
    c_reader = PlaintextCorpusReader(c_root,
                                     "Board_of_Directors_back_step2.txt")
    # 得到文本名列表
    f_list = c_reader.fileids()
    return c_reader, f_list


def lemmatizer(word_list):
    """
    使用词典进行词形还原
    :param word_list: 单词列表
    :return:
    """
    ret = []
    wn_lem = WordNetLemmatizer()

    for word in word_list:
        # 注意先转换成小写
        ret.append(wn_lem.lemmatize(word.lower()))
    return ret


def treetager_stem(word_list):
    ret = []
    tagger = TreeTagger(TAGDIR="D:\intern"
                               "\\nlp\\tools\\tree-tagger-windows-3.2\TreeTagger")
    for word in word_list:
        # 对于数字，tagger 一律还原成 @card@
        if word.isdigit():
            ret.append(word)
        else:
            tags = tagger.tag_text(word.lower())
            for tag in tags:
                ret.append(tag.split()[2])
    return ret


def filter_stop_words(word_list):
    """
    停用词过滤
    :param word_list:
    :return:
    """
    ret = []
    for word in word_list:
        if word.lower() not in stopwords.words('english') and len(word) > 2:
            ret.append(word)
    return ret


def count_word_freq(c_reader, f):
    """
    计算词频
    :param c_reader:
    :param f:
    :return:
    """
    words = c_reader.words(f)

    # 词形还原
    tree_words = treetager_stem(words)
    # 停用词过滤
    filter_words = filter_stop_words(tree_words)
    w_freq = FreqDist(filter_words)

    return w_freq


def save_word_freq(w_freq, f_path, f_name):
    """
    保存词频为文本文件
    :param w_freq:
    :param f_path:
    :param f_name:
    :return:
    """
    # 去掉多余的后缀名
    f_name = f_name.replace("_step2.txt", "")
    with open(f_path + f_name + '_treetagger_step3.txt', "w") as txt_f:
        for word, freq in w_freq.items():
            # 设定格式: 左对齐，20位宽的字符，左对齐，6位宽的数字
            str_line = "%-20s%-6d\n" % (word.encode("utf-8"), freq)
            txt_f.write(str_line)


if __name__ == '__main__':
    corpus_root = "E:\codes\pycharm\\nlp\\financial_reports_processing\week_2\\files\\"
    corpus_reader, file_list = load_corpus(corpus_root)
    for f in file_list:
        word_freq = count_word_freq(corpus_reader, f)
        save_word_freq(word_freq, corpus_root, f)
