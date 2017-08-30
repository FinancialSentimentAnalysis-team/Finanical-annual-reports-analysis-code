import MySQLdb
import xlrd
import xlsxwriter
import os
from collections import defaultdict
from datetime import *
import time

# Returns a connect object given host, port, user, password, and the name of the database
def connect(host, port, user, pwd, db):
    '''
    functionality: for opening the database that has the information of stocks prices
    
    input: host name,     type of str
           port,          type of int
           user,          type of str
           password,      type of str
           database name, type of str
           
    return: a connect object
    
    '''
    return MySQLdb.connect(host = host,port = port,user=user,passwd=pwd,db=db)

# returns a dict(key: stock) of subdicts(key : date object, value:  tuple of stock prices info)
# Checked
def stocks_prices(conn, stock_list):
    '''
    functionality: provides all the prices (open prices, close prices and other information) 
                   for the stocks you are interested in
    
    input: a connect object
           the list of stocks you are interested in

    return: a dict
            The keys are stock names, the values are sub-dicts
            Each sub-dict has date objects as keys and prices information as values
            
    '''
    
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
    '''
    functionality: provides all the prices (open prices, close prices and other information) 
                   for the stocks you are interested in
    
    input: the list of stocks you are interested in
           the file that has all the reports release dates
           flag is either 'annual' or 'interim'

    return: a dict
            The keys are stock names, the values are sub-dicts.
            Each sub-dict has year as keys and date objects as values
            
    '''
    
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
                    Date = _fill_up_date(sheet, r, c, sheet.ncols)
                Date = str(Date[0]).split('/')
                d[year] = _converted_dates(date(int(year), int(Date[1]), int(Date[0])))
            stock_release_dates[stock] = d
    return stock_release_dates

# Checked
def prices(stock_list, stock_release_dates, Stocks_Prices):
    '''
    functionality: provides all the close prices for the stocks you are interested in
    
    input: the list of stocks you are interested in
           the stock reports release information, detail in release_dates(stock_list, file_path, flag)
           the stocks prices, detail in stocks_prices(conn, stock_list)

    return: a dict
            The keys are stock names, the values are sub-dicts.
            Each sub-dict has year as keys and price as values
            
    '''
    
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
    '''
    functionality: provides a date object that is one weekday after the given date.
                   If the given date is on weekend, the function will return the next monday
    
    input: a date object

    return: a date object
            
    '''
    
    if Date.isoweekday() == 5:
        delta = timedelta(days = 3)
    elif Date.isoweekday() == 6:
        delta = timedelta(days = 2)
    else:
        delta = timedelta(days = 1)
    return Date + delta

# Checked
def _fill_up_date(sheet, row, col, ncols):
    '''
    functionality: This function is used only when the release date for a certain year is not on the sheet.
                   It will find the next years or previous years' month and day to fill up the missing date.
    
    input: the sheet that has all the date release information
          row number
          col number
          total col number

    return: a str of date information
            
    '''
        
    return _fill_up_date_forward(sheet, row, col, ncols)

def _fill_up_date_forward(sheet, row, col, ncols):
    '''
    functionality: It will recursively find the next years' month and day to fill up the missing date.
                   If it reaches the end of the column, it will call _fill_up_date_backward(sheet, row, col)
    
    input: the sheet that has all the date release information
          row number
          col number
          total col number

    return: a str of date information
            
    '''
    
    if col < ncols - 1:
        next_year_date = sheet.cell(row, col + 1).value
        if type(next_year_date) == float:
            next_year_date = ''
        Date = next_year_date.strip().replace('<br>', ' ')
        if Date == '':
            return _fill_up_date_forward(sheet, row, col + 1, ncols)
        return Date.split()
    return _fill_up_date_backward(sheet, row, col)

def _fill_up_date_backward(sheet, row, col):
    '''
    functionality: It will recursively find the previous years' month and day to fill up the missing date.
    
    input: the sheet that has all the date release information
           row number
           col number

    return: a str of date information
            
    '''

    previous_year_date = sheet.cell(row, col - 1).value
    if type(previous_year_date) == float:
        previous_year_date = ''
    Date = previous_year_date.strip().replace('<br>', ' ')
    if Date == '':
        return _fill_up_date_backward(sheet, row, col - 1)
    return Date.split()

# Checked
def _converted_price(Date, stock, Stocks_Prices):
    '''
    functionality: Provides the close price of the given date for the stock.
                   If the date is not valid, returns the close price for the next date.
    
    input: a date object
           the name of the stock
           the stocks prices, detail in stocks_prices(conn, stock_list)

    return: the close price, type of float
            or 
            '#N/A',          representing date out of range
            
    '''
        
    data = Stocks_Prices[stock][Date]
    if Date > date(2017, 5, 20):
        return '#N/A'
    if data == tuple():
        return _converted_price(_converted_dates(Date), stock, Stocks_Prices)
    return float(data[-2])

def open_prices(stock_list, stock_release_dates, Stocks_Prices):
    '''
    functionality: provides all the open prices for the stocks you are interested in
    
    input: the list of stocks you are interested in
           the stock reports release information, detail in release_dates(stock_list, file_path, flag)
           the stocks prices, detail in stocks_prices(conn, stock_list)

    return: a dict
            The keys are stock names, the values are sub-dicts.
            Each sub-dict has year as keys and price as values.
            
    '''
    
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
    '''
    functionality: Provides the open price of the given date for the stock.
                   If the date is not valid, returns the open price for the next date.
    
    input: a date object
           the name of the stock
           the stocks prices, detail in stocks_prices(conn, stock_list)

    return: the open price, type of float
            or 
            '#N/A',         representing date out of range
            
    '''
        
    data = Stocks_Prices[stock][Date]
    if Date > date(2017, 5, 20):
        return '#N/A'
    if data == tuple():
        return _converted_open_price(_converted_dates(Date), stock, Stocks_Prices)
    return float(data[-5])
    

