
# coding: utf-8

# In[1]:


import os
import xlrd, xlwt
import time
from datetime import *
import csv
from collections import defaultdict

from Plotting_Stock_Price import connect, stocks_prices, release_dates, prices, _converted_dates, _fill_up_date, _converted_price, open_prices, _converted_open_price 
from Summary_McDonald import  Label, _close_prices_after_release, _open_prices_after_release


def read_dictionary(dictionary_path):
    d = defaultdict(list)
    csv_file = open(dictionary_path, 'r')
    reader = csv.reader(csv_file)
    for line in reader:
        if line[0] != 'POS':
            for word in line[4].split(','):
                d[word[:-2]].append((word.split('#')[0] + '#' + line[0], line[2], line[3]))
    csv_file.close()
    pos_result_dict = dict()
    neg_result_dict = dict()
    for word in d:
        dic = dict()        
        _property = set(word_info[0] for word_info in d[word])
        for word_with_property in _property:
            dic[word_with_property] = [0,0]
        for word_with_property in _property:
            count = 0
            for word_info in d[word]:
                if word_info[0] == word_with_property:
                    count += 1
                    dic[word_with_property][0] += float(word_info[1])
                    dic[word_with_property][1] += float(word_info[2])
            dic[word_with_property][0] /= count
            dic[word_with_property][1] /= count
        for key, value in dic.items():
            if value[0] != 0:
                pos_result_dict[key.strip()] = value
            if value[1] != 0:
                neg_result_dict[key.strip()] = value
    return pos_result_dict, neg_result_dict

def read_excel(file_path, pos_dictionary, neg_dictionary):
    workbook = xlrd.open_workbook(file_path)
    result = list()
    result.append(dict()) # dict of year: info, for annual
    result.append(dict()) # dict of year: info, for interim
    year = 2002
    for i in range(15):
        result[0][str(year+i)] = dict() # for each category
        result[1][str(year+i)] = dict() # for each category
    
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        info = sheet.cell_value(0,0).split()
        
        if info[0] == 'annual':
            _modify_dict(result[0], ' '.join(info[1:]), sheet, pos_dictionary, neg_dictionary)
        else:
            _modify_dict(result[1], ' '.join(info[1:]), sheet, pos_dictionary, neg_dictionary)
    return result

def _modify_dict(d, category, sheet, pos_dictionary, neg_dictionary):
    for col in range(sheet.ncols-1):
        s = 0
        for row in range(sheet.nrows-1):
            if category == 'positive':
                weight = pos_dictionary[sheet.cell_value(row+1, 0)][0]
            else:
                weight = neg_dictionary[sheet.cell_value(row+1, 0)][1]
            s += int(sheet.cell_value(row+1, col+1)) * weight
        d[sheet.cell_value(0, col+1)][category] = s

def save_into_excel(stock_name, result_path, data, stock_list, annual_release, interim_release, Stocks_Prices, Function):
    workbook =  xlwt.Workbook()
    Annual = workbook.add_sheet("Annual")
    Interim = workbook.add_sheet("Interim")
    _write_sheet(Annual,  data[0], 'Annual', stock_name, stock_list,  annual_release,  Stocks_Prices, Function)
    _write_sheet(Interim, data[1], 'Inteirm',stock_name, stock_list, interim_release, Stocks_Prices, Function)
    workbook.save(result_path + stock_name +'_SentiWordSet_summary.xls')

def _write_sheet(sheet, datum, tag, stock_name, stock_list, release_dates, Stocks_Prices, Function):
    sheet.write(0,0, tag)
    category = ['positive', 'negative']
    delta_days = [0,7,30,90,180]
    col = 1
    for c in category:
        sheet.col(col).width = 256*15
        sheet.write(0, col, c)
        col += 1
    for i in range(1,6,1):
        sheet.col(col).width = 256*15
        sheet.write(0, col, 'Label_'+str(i))
        col += 1
        
    row = 1
    for year in sorted(datum):
        sheet.write(row,0,year)
        col = 1
        for c in category:
            if len(datum[year]) == 0:
                sheet.write(row, col, 0)
            else:
                sheet.write(row, col, datum[year][c])
            col += 1
        row += 1
        
    for delta_day in delta_days:
        close_prices = _close_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day)[stock_name]
        open_prices  =  _open_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day)[stock_name]
        row = 1
        for year in range(2002, 2017):
            open_price = open_prices[str(year)]
            close_price = close_prices[str(year)]
            if open_price == '#N/A' or close_price == '#N/A':
                sheet.write(row, col, '#N/A')
            else:
                sheet.write(row, col, Function(open_price, close_price))
            row += 1
        col += 1


if __name__ == '__main__':
    root_path =   '/usr/yyy/wk3/Count_SentiWordSet/'
    result_path = '/usr/yyy/wk3/Summary_SentiWordSet/'
    dictionary_path = '/usr/yyy/dictionaries/SentiWordNet_filtered.csv'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
        
    conn = connect('172.31.238.166', 3306, 'root', 'root', 'stock')
    stock_list = [file_name[:5] for file_name in os.listdir(root_path)]
    Stocks_Prices = stocks_prices(conn, stock_list)
    conn.close()
    
    release_dates_path = '/usr/yyy/wk2/reports release dates/'
    annual_release = release_dates(stock_list, release_dates_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, release_dates_path + 'interim.xlsx', 'interim')
    
    Function = Label(0.005)
    
    pos_dictionary, neg_dictionary = read_dictionary(dictionary_path)
    
    for file_name in os.listdir(root_path):
        data = read_excel(root_path + file_name, pos_dictionary, neg_dictionary)
        
        save_into_excel(file_name[:5], result_path, data, stock_list, annual_release, interim_release, Stocks_Prices, Function)
        
        print file_name[:5] + ' completed\n'

    print '---------------Done------------------'




# In[ ]:




