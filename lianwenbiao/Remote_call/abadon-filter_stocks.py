import os
import sys

import xlrd
import xlwt


def read_excel(file_path):
    data = xlrd.open_workbook(file_path)
    sheet = data.sheet_by_name('Discretionary')

    stock_list = []

    for i in range(550):
        if i > 510:
            print sheet.cell(i, 2).value
        # stock_no = sheet.cell(i, 0).value.split()[0]
        # stock_list.append(stock_no)
  
    print stock_list
    '''
    for i in range(sheet.ncols)
        _l.append(sheet.cell(0, i).value)
    return _l

path_from = sys.argv[1]
path_to   = sys.argv[2]

target_list = []


files = os.listdir(path_from)
for f in files:
    if f in target_list:
        cmd = "cp -r " + path_from + f + ' ' + path_to
        os.system(cmd)
'''
read_excel('./HK_282stocks2003.xlsx')
