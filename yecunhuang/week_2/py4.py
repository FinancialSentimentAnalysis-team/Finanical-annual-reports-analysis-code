# encoding:utf-8

"""
File: py4.py
Author:  Charles Yee
Date: 2017/7/20
Version: python 2.7.13
Desc:
"""
import xlrd
import xlwt


def save_data_to_excel(sheet_name, file_path):
    with open(file_path + "week_2\\files\\Board_of_Directors"
                          "_back_treetagger_step3.txt") as txt_f:
        row = 0
        for line in txt_f:
            data = line.strip().split()
            sheet_name.write(row, 0, data[0])
            sheet_name.write(row, 1, data[1])
            row += 1


if __name__ == '__main__':
    file_path = "E:\codes\pycharm\\nlp\\financial_reports_processing\\"

    wk_book = xlwt.Workbook()
    sheet_annual = wk_book.add_sheet("Annual")
    sheet_interim = wk_book.add_sheet("Interim")

    save_data_to_excel(sheet_annual, file_path)

    wk_book.save(file_path + "financial_reports\\Board_of_Directors.xls")
