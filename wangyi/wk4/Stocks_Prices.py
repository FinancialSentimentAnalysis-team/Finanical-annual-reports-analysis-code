
# coding: utf-8

# In[ ]:


import MySQLdb
import xlrd
import xlsxwriter
import os
from collections import defaultdict
from datetime import *
import time

# Returns a connect object given host, port, user, password, and the name of the database
def connect(host, port, user, pwd, db):
    return MySQLdb.connect(host = host,port = port,user=user,passwd=pwd,db=db)

# returns a dict(key: stock) of subdicts(key : date object, value:  tuple of stock prices info)
# Checked
def stocks_prices(conn, stock_list):
    stock_price = dict()
    cur = conn.cursor()
    cur.execute('select * from stock_price')
    data = cur.fetchall()
    for stock in stock_list:
        d = defaultdict(tuple)
        for stock_info in data:
            if ('00000' + stock_info[0].split()[0].strip())[-5:] == stock:
                Date = str(stock_info[1]).split('-')
                D = date(int(Date[0]), int(Date[1]), int(Date[2]))
                d[D] = stock_info[2:]
        stock_price[stock] = d
    cur.close()
    return stock_price

# Checked
def release_dates(stock_list, file_path, flag):
    data = xlrd.open_workbook(file_path)
    sheet = data.sheet_by_name(flag)
    stock_release_dates = dict()
    
    for r in range(sheet.nrows):
        stock = ('00000'+str(sheet.cell(r, 0).value))[-7:-2]
        
        if stock in stock_list:
            d = dict()
            for c in range(1, sheet.ncols, 1):
                year = str(sheet.cell(0,c).value)[:-2]
                value = sheet.cell(r,c).value
                
                if type(value) == unicode and '<br>' in value:
                    Date = value.split('<br>')
                elif type(value) == float:
                    Date = []
                else:
                    Date = value.split()

                if year == '':
                    year = '2017'
                if Date == []:
                    if year == '2017':
                        continue
                    Date = _fill_up_date(sheet, r, c)
                Date = str(Date[0]).split('/')
                d[year] = _converted_dates(date(int(year), int(Date[1]), int(Date[0])))
            stock_release_dates[stock] = d
    return stock_release_dates

# Checked
def prices(stock_list, stock_release_dates, Stocks_Prices):
    result = dict()
    for stock in stock_list:
        d = dict()
        year = 2000
        i = 0
        for Date in sorted(stock_release_dates[stock].values()):
            d[str(year+i)] = _converted_price(Date, stock, Stocks_Prices)
            i+=1
        result[stock] = d
    return result

# Returns a date object which is one valid day after the given date object
# Checked
def _converted_dates(Date):
    if Date.isoweekday() == 5:
        delta = timedelta(days = 3)
    elif Date.isoweekday() == 6:
        delta = timedelta(days = 2)
    else:
        delta = timedelta(days = 1)
    return Date + delta

# Checked
def _fill_up_date(sheet, row, col):
    try:
        Date = sheet.cell(row, col+1).value.strip()
        col+=1
    except:
        Date = sheet.cell(row, col-1).value.strip()
        col-=1
    if Date == '':
        return _fill_up_date(sheet, row, col)
    return Date.split()

# Checked
def _converted_price(Date, stock, Stocks_Prices):
    data = Stocks_Prices[stock][Date]
    if Date > date(2017, 5, 20):
        return '#N/A'
    if data == tuple():
        return _converted_price(_converted_dates(Date), stock, Stocks_Prices)
    return float(data[-2])

def open_prices(stock_list, stock_release_dates, Stocks_Prices):
    result = dict()
    for stock in stock_list:
        d = dict()
        year = 2000
        i = 0
        for Date in sorted(stock_release_dates[stock].values()):
            d[str(year+i)] = _converted_open_price(Date, stock, Stocks_Prices)
            i+=1
        result[stock] = d
    return result

def _converted_open_price(Date, stock, Stocks_Prices):
    data = Stocks_Prices[stock][Date]
    if Date > date(2017, 5, 20):
        return '#N/A'
    if data == tuple():
        return _converted_open_price(_converted_dates(Date), stock, Stocks_Prices)
    return float(data[-5])
    

