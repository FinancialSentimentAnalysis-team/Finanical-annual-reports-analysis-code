
# coding: utf-8

# In[15]:


import os
import xlrd, xlwt
import time
from datetime import *
from Plotting_Stock_Price import connect, stocks_prices, release_dates, prices, _converted_dates, _fill_up_date, _converted_price, open_prices, _converted_open_price 

def read_excel(file_path):
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
    for col in range(sheet.ncols-1):
        year = sheet.cell_value(0, col+1)
        d[year][category] = sum([int(i) for i in sheet.col_values(col+1)[1:]])

def Label(determinant):
    def Func(open_price, close_price):
        R = (close_price - open_price)/open_price
        if R >= determinant:
            return 1
        elif abs(R) < determinant:
            return 0
        return -1
    return Func

def save_into_excel(stock_name, result_path, data, stock_list, annual_release, interim_release, Stocks_Prices, Function):
    workbook =  xlwt.Workbook()
    Annual = workbook.add_sheet("Annual")
    Interim = workbook.add_sheet("Interim")
    _write_sheet(Annual,  data[0], 'Annual', stock_name, stock_list,  annual_release,  Stocks_Prices, Function)
    _write_sheet(Interim, data[1], 'Inteirm',stock_name, stock_list, interim_release, Stocks_Prices, Function)
    workbook.save(result_path + stock_name +'_McDonald_summary.xls')

def _close_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day):
    result = dict()
    for stock in release_dates:
        d = dict()
        for year in release_dates[stock]:
            d[year] = release_dates[stock][year] + timedelta(days = delta_day)
        result[stock] = d
    return prices(stock_list, result, Stocks_Prices)

def _open_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day):
    result = dict()
    for stock in release_dates:
        d = dict()
        for year in release_dates[stock]:
            d[year] = release_dates[stock][year] + timedelta(days = delta_day)
        result[stock] = d
    return open_prices(stock_list, result, Stocks_Prices)

def _write_sheet(sheet, datum, tag, stock_name, stock_list, release_dates, Stocks_Prices, Function):
    sheet.write(0,0, tag)
    category = ['positive', 'negative', 'model strong', 'model weak', 'litigious', 'uncertainty']
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
            
if __name__ == "__main__":
    root_path = '/usr/yyy/wk3/Count_McDonald/'
    result_path = '/usr/yyy/wk3/Summary_McDonald/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    conn = connect('172.31.238.166', 3306, 'root', 'root', 'stock')
    stock_list = ['00316','00590','01171']
    Stocks_Prices = stocks_prices(conn, stock_list)
    conn.close()
    file_path = '/usr/yyy/wk2/reports release dates/'
    annual_release = release_dates(stock_list, file_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, file_path + 'interim.xlsx', 'interim')
    
    Function = Label(0.005)
    
    for file_name in os.listdir(root_path):
        data = read_excel(root_path + file_name)
        save_into_excel(file_name[:5], result_path, data, stock_list, annual_release, interim_release, Stocks_Prices, Function)
        print file_name[:5] + ' completed \n'

    print '---------------Done-------------------'



# In[ ]:




