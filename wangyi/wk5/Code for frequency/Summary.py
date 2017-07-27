import os
import xlrd, xlwt
import time
from datetime import *
from Stocks_Prices import *
from collections import defaultdict

def read_excel(file_path):
    '''
    functionality: reads an excel file that counts the words using McDonald-like Dictionary
    
    input: the path where the excel file is
    
    return: a list of two dicts, list[0] is for annual, list[1] is for interim
            Each dict above has years as keys, and sub-dict as values
            Each sub-dict is has categories (or you can call them determinants) as keys, and the total count of words for that category
    
    '''
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
            _modify_dict(result[0], ' '.join(info[1:]), sheet)
        else:
            _modify_dict(result[1], ' '.join(info[1:]), sheet)
    return result

def _modify_dict(d, category, sheet):
    '''
    functionality: modify the dicts described in read_excel(file_path)
    
    input: the dict for annual or the dict for interim
           one single cateogry (or you can call it determinant)
           the sheet in which you want to write
           
    return: None
    
    '''
   
    for col in range(sheet.ncols-1):
        year = sheet.cell_value(0, col+1)
        if year != '2017':
            d[year][category] = sum([float(i) for i in sheet.col_values(col+1)[1:]])

def Func(current_close_price, future_close_price):
    if future_close_price > current_close_price:
        return 1
    elif future_close_price < current_close_price:
        return -1
    return 0

def save_into_excel(stock_name, root_file_path, result_file_path, stock_list, annual_release, interim_release, Stocks_Prices):
    '''
    functionality: save the data into the result_file_path
    
    input: the name of the stock
           the excel file that has counts information
           the destination where you want to store
           the list of stocks you are interested in
           the annual reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)
           the interim reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           
    return: None
    
    '''
   
    data = read_excel(root_file_path)
    workbook =  xlwt.Workbook()
    Annual = workbook.add_sheet("Annual")
    Interim = workbook.add_sheet("Interim")
    _write_sheet(Annual,  data[0], 'Annual', stock_name, stock_list,  annual_release,  Stocks_Prices)
    _write_sheet(Interim, data[1], 'Inteirm',stock_name, stock_list, interim_release, Stocks_Prices)
    workbook.save(result_file_path)

def _write_sheet(sheet, datum, tag, stock_name, stock_list, release_dates, Stocks_Prices):
    '''
    functionality: stores the datum into the sheet
    
    input: the sheet you want to write in
           data[0] or data[1] from read_excel(file_path)
           tag is either 'Annual' or 'Interim'
           the name of the stock
           the list of stocks you are interested in
           the stock reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           
    return: None
    
    '''
   
    sheet.write(0,0, tag)
    category = set()
    for year in sorted(datum):
        for c in datum[year]:
            category.add(c)
    delta_days = [1,7,30,90,180]
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
    close_prices_current = _close_prices_after_release(stock_list, release_dates, Stocks_Prices, 0)[stock_name]
    
    for delta_day in delta_days:
        close_prices_future  =  _close_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day)[stock_name]
        row = 1
        for year in range(2002, 2017):
            close_price_c = close_prices_current[str(year)]
            close_price_f = close_prices_future[str(year)]
            if close_price_c == '#N/A' or close_price_f == '#N/A':
                sheet.write(row, col, '#N/A')
            else:
                sheet.write(row, col, Func(close_price_c, close_price_f))
            row += 1
        col += 1

def _close_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day):
    '''
    functionality: provides the close prices for all the stocks you are interested in
    
    input: the list of stocks you are interested in
           the stock reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)        
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           delta_day is an int, representing how many days after the report release day
           
    return: a dict, detail in Srocks_Prices.prices(stock_list, stock_release_dates, Stocks_Prices)
    
    '''

    result = dict()
    for stock in release_dates:
        d = dict()
        for year in release_dates[stock]:
            d[year] = release_dates[stock][year] + timedelta(days = delta_day)
        result[stock] = d
    return prices(stock_list, result, Stocks_Prices)

def _open_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day):
    '''
    functionality: provides the open prices for all the stocks you are interested in
    
    input: the list of stocks you are interested in
           the stock reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)        
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           delta_day is an int, representing how many days after the report release day
           
    return: a dict, detail in Srocks_Prices.open_prices(stock_list, stock_release_dates, Stocks_Prices)
    
    '''

    result = dict()
    for stock in release_dates:
        d = dict()
        for year in release_dates[stock]:
            d[year] = release_dates[stock][year] + timedelta(days = delta_day)
        result[stock] = d
    return open_prices(stock_list, result, Stocks_Prices)

def get_Stocks_Prices(stock_list):
    '''
    functionality: assuming the information of stocks prices store in a constant place,
                   you can easily access the database that has the information of stocks prices
    
    input: the list of stocks you are interested in

    return: the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
    
    '''

    conn = connect('172.31.238.166', 3306, 'root', 'root', 'stock')
    Stocks_Prices = stocks_prices(conn, stock_list)
    conn.close()
    return Stocks_Prices
