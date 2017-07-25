# encoding:utf-8

"""
File: py2.py
Author:  Charles Yee
Date: 2017/7/19
Version: python 2.7.13
Desc:
"""
import os
import re


def _is_invalid_line(line_txt):
    """
    判断当前行是否是无效行
    :param line_txt:
    :return: 布尔值
    """
    if line_txt == '':
        return True

    # 过滤不合法字符
    tmp = re.sub(r"[^A-Za-z0-9]", '', line_txt)
    # 如果全是数字或者长度小于3，则直接过滤
    if tmp.isdigit() or len(tmp) <= 3:
        return True

    # 搜索cid
    if re.search("(cid\d+)+", tmp):
        return True
    # 注意所有空格已被替换
    if re.search("HK\d+", tmp) and len(line_txt.split()) == 1:
        return True

    return False


def _is_title(line_txt):
    """
    判断当前文本行是否是标题/目录
    :param line_txt:输入的文本行
    :return:
    """
    conj_words = ['or', 'and', 'at', 'in', 'by', 'with', 'of']
    # 一般而言标题/目录不会出现is
    sentence_words = ['is']

    words = line_txt.split()

    is_title = True

    # 依据驼峰法判断每个除了介词外所有词的首字母是否大写
    for word in words:
        if word not in conj_words and not word[0].isupper():
            is_title = False

    return is_title


def deal_with_sentence(line_txt):
    """
    处理单行文本
    :param txt_path: 文本路径
    :param txt_name: 文本名
    :return:
    """
    # 过滤特殊字符
    # 保留所有格(中文所有格去掉?)$留不留?
    line_content = re.sub(r"[^A-Za-z0-9,.’]", ' ', line_txt) \
        .decode("utf-8", 'ignore').strip()

    # 检查是否是标题
    if _is_title(line_content):
        line_content += '\n'
    else:
        # 检查最后一个字符是否是停句符
        if line_content[-1] == '.':
            line_content += '\n'
        # 不是停句符只加上空格以分隔单词
        else:
            line_content += ' '
    return line_content


def _filter_invalid_title(txt_f):
    """
    从文本文件中删除没有意义的标题行：
    仅保留和正文最接近的标题行
    :return:
    """
    result_content = ""
    last_title = ""

    while True:
        line = txt_f.readline()
        if line == "":
            break
        elif line == '\n':
            continue
        elif _is_title(line):
            last_title = line + "\n"
        else:
            result_content += last_title
            result_content += line
            last_title = ''
    return result_content


def split_chunk(txt_path, txt_name):
    """
    将所有内容按无效行分割分成块，以显示文章的结构，便于调试
    和后续的处理
    """
    # 最后要写入的结果
    result_content = ''
    chunk_content = ''

    with open(txt_path + "/" + txt_name + ".txt", "rb") as txt_f:

        while True:
            line = txt_f.readline()
            # 当第一次读取到了无效行
            if _is_invalid_line(line.strip()):

                # 并且当前块内容不为空，则取出这一块进行处理
                # 这样防止连续空行
                if chunk_content != '':
                    result_content += chunk_content
                    # 每块之间添加一个空行
                    result_content += '\n'
                    chunk_content = ''

                # 如果读到了文件末尾，则结束
                if line == '':
                    break
                    # 如果此时块内容为空则直接忽略
            else:
                # 块内内容添加
                line = deal_with_sentence(line)
                chunk_content += line

    paths = "/".join(txt_path.split('/')[:5]) + "/filter_files/" \
            + "/".join(txt_path.split('/')[-2:])
    if not os.path.exists(paths):
        os.makedirs(paths)

    with open(paths + "/" + txt_name + "_back.txt", "w") as txt_f:
        txt_f.write(result_content.encode("utf-8"))

    with open(paths + "/" + txt_name + "_back.txt", "r") as txt_f:
        result_content = _filter_invalid_title(txt_f)

    if os.path.exists(paths + "/" + txt_name + "_back2.txt"):
        os.remove(paths + "/" + txt_name + "_back2.txt")

    with open(paths + "/" + txt_name + "_back.txt", "w") as txt_f:
        txt_f.write(result_content)


def process(stock_no, period):
    txt_path = "F:/xunlei/CharlesYee/financial_reports" \
               "/" + stock_no + "/txt_files/"

    year_list = os.listdir(txt_path)

    for year in year_list:
        # 不可累加
        # txt_path = txt_path + year + "/" + period
        txt_path_in = txt_path + year + "/" + period

        # 防止出现缺失 Annual 或者 Interim
        if not os.path.exists(txt_path_in):
            continue

        file_list = os.listdir(txt_path_in)
        for txt_name in file_list:
            txt_name = txt_name.replace(".txt", "")
            split_chunk(txt_path_in, txt_name)


if __name__ == '__main__':
    # process("00590", "Annual")
    process("00590", "Interim")

    process("00001", "Annual")
    process("00001", "Interim")
    print "finished!"
