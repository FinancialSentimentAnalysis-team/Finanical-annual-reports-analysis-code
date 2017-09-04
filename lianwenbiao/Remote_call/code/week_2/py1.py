# encoding:utf-8

"""
File: py1.py
Author:  Charles Yee
Date: 2017/7/19
Version: python 2.7.13
Desc:
"""
import os
from StringIO import StringIO

from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def _pdf_to_text(pdf_file, pages=None):
    """
    pdf解析
    当文档是可抽取的时候，取出其布局中横向的BOX框中的文字，
    得到的格式较为规整
    否则直接使用 TextConverter 取出文字
    :param pdf_file: 打开的pdf文件
    :param pages: 解析的页面数目
    :return: 解析的字符串
    """
    # # 设定抽取的页面的数量
    # if not pages:
    #     page_nums = set()
    # else:
    #     page_nums = set(pages)

    result_contents = ''
    parser = PDFParser(pdf_file)
    document = PDFDocument(parser)

    # 资源管理器
    manager = PDFResourceManager()

    # 如果文档是可抽取的
    if document.is_extractable:
        print "is extractable"
        # 转换器
        # pageno 不能为 set ?
        device = PDFPageAggregator(manager, laparams=LAParams())
        # 解释器
        interpreter = PDFPageInterpreter(manager, device)

        # 逐页处理页面
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 得到布局
            layout = device.get_result()
            for x in layout:
                # 取出横向的BOX框内文字
                if isinstance(x, LTTextBoxHorizontal):
                    result_contents += x.get_text().encode('utf-8') + "\n"

    else:  # 如果文档不可抽取
        outfp = StringIO()
        device = TextConverter(manager, outfp, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, device)
        rotation = 0
        for page in PDFPage.get_pages(pdf_file, check_extractable=False):
            # 此处 rotate 有何作用?
            page.rotate = (page.rotate + rotation) % 360
            interpreter.process_page(page)

        result_contents += outfp.getvalue()
        outfp.close()

    device.close()
    return result_contents


def convert(pdf_in_path, pdf_out_path, pdf_name=None, pages=None):
    """
    如果没有给出 pdf文件名，则将指定 pdf_in_path 目录下所有 pdf文件
        转换成文本文件，并存于指定 pdf_out_path 目录下
    否则将指定 pdf_in_path 目录下的指定名为 pdf_name pdf文件转换为
        txt 文件，并存于指定 pdf_out_path 目录下
    :param pdf_in_path:
    :param pdf_out_path:
    :param pdf_name:
    :param pages: 转换的页数
    :return:
    """
    if not pdf_name:
        pdf_list = os.listdir(pdf_in_path)
        for _ in pdf_list:
            _ = _.replace(".pdf", "")
            # 递归调用
            convert(pdf_in_path, pdf_out_path, _)
    else:
        try:
            with open(pdf_in_path + "/" + pdf_name + ".pdf", "rb") as pdf_f:
                pdf_text = _pdf_to_text(pdf_f, pages)

            if not os.path.exists(pdf_out_path):
                os.makedirs(pdf_out_path)
            with open(pdf_out_path + "/" + pdf_name + ".txt", "w") as txt_f:
                txt_f.write(pdf_text)

        except IOError, msg:
            print msg


def convert_dir(pdf_in_path):
    """
    给出pdf所在的文件的目录，在所给的目录下
    创建 txt_files 文件夹，用以存储所有的文本文件，
    目录结构与原结构相同
    :param pdf_in_path:
    :return:
    """
    year_list = os.listdir(pdf_in_path)
    for year in year_list:

        tmp_dir = pdf_in_path + "/" + year + "/Annual"
        pdf_out_path = pdf_in_path + "/txt_files/" + year + "/Annual"
        if os.path.exists(tmp_dir):
            convert(tmp_dir, pdf_out_path)

        tmp_dir = pdf_in_path + "/" + year + "/Interim"
        pdf_out_path = pdf_in_path + "/txt_files/" + year + "/Interim"
        if os.path.exists(tmp_dir):
            convert(tmp_dir, pdf_out_path)


if __name__ == '__main__':
    # pdf_in_path_1 = "F:/xunlei/CharlesYee/financial_reports/00001"
    # convert_dir(pdf_in_path_1)
    pdf_in_path_2 = "F:/xunlei/CharlesYee/financial_reports/00590"
    convert_dir(pdf_in_path_2)
