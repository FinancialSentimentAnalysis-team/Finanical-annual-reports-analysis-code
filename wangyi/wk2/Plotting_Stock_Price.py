
# coding: utf-8

# In[1]:


import MySQLdb
import xlrd
import xlsxwriter
import os
from collections import defaultdict
from datetime import *
import time
from Python_Plotting import read_dictionary, read_excel, analyze_sheet, _word_set, _write_sheet, _year_list, _count_freq, _draw_plot1

def save_into_excel(workbook, stock, annual_pos, annual_neg, interim_pos, interim_neg, annual_prices, interim_prices):
    Positive_Annual = workbook.add_worksheet("Positive_Annual")
    Negative_Annual = workbook.add_worksheet("Negative_Annual")
    Positive_Interim = workbook.add_worksheet("Positive_Interim")
    Negative_Interim = workbook.add_worksheet("Negative_Interim")
    Summary = workbook.add_worksheet('Summary')
    _write_sheet(Positive_Annual, annual_pos, 'positive')
    _write_sheet(Negative_Annual, annual_neg, 'negative')
    _write_sheet(Positive_Interim, interim_pos, 'positive')
    _write_sheet(Negative_Interim, interim_neg, 'negative')
    _write_summary(workbook, Summary, stock, annual_pos, annual_neg, interim_pos, interim_neg, annual_prices, interim_prices)

def _write_summary(workbook, sheet, stock, annual_pos, annual_neg, interim_pos, interim_neg, annual_prices, interim_prices):
    year_list = _year_list(annual_pos, interim_pos)
    col = 1 
    for year in year_list:
        sheet.write(0, col, year)
        col += 1
    sheet.write(1,0, 'Positive(Annual)')
    sheet.write(2,0, 'Negative(Annual)')
    sheet.write(3,0, 'Positive-Negative(Annual)')
    sheet.write(4,0, 'Price(Annual)')
    sheet.write(50,0, 'Positive(Interim)')
    sheet.write(51,0, 'Negative(Interim)')
    sheet.write(52,0, 'Positive-Negative(Interim)')
    sheet.write(53,0, 'Price(Interim)') 
    row = 1
    col = 1
    for year in year_list:
        annual_pos_freq  = _count_freq(annual_pos, year)
        annual_neg_freq  = _count_freq(annual_neg, year)
        interim_pos_freq = _count_freq(interim_pos, year)
        interim_neg_freq = _count_freq(interim_neg, year)

        sheet.write(row,      col, annual_pos_freq)
        sheet.write(row + 1,  col, annual_neg_freq)
        sheet.write(row + 2,  col, annual_pos_freq - annual_neg_freq)
        sheet.write(row + 3,  col, annual_prices[stock][year])
        sheet.write(row + 49, col, interim_pos_freq)
        sheet.write(row + 50, col, interim_neg_freq)
        sheet.write(row + 51, col, interim_pos_freq - interim_neg_freq)
        sheet.write(row + 52, col, interim_prices[stock][year])
        col += 1

    _draw_plot1(workbook, sheet, '=Summary!$B$1:$P$1', "=Summary!$A$2", '=Summary!$B$2:$P$2',  '=Summary!$A$3', '=Summary!$B$3:$P$3',  'Annual Report Plot', 'A6' )  
    _draw_plot1(workbook, sheet, '=Summary!$B$1:$P$1', "=Summary!$A$51",'=Summary!$B$51:$P$51','=Summary!$A$52','=Summary!$B$52:$P$52','Interim Report Plot','A55')
    _draw_plot2(workbook, sheet, '=Summary!$B$1:$P$1', '=Summary!$A$4', '=Summary!$B$4:$P$4',  '=Summary!$A$5', '=Summary!$B$5:$P$5',  'Positive-Negative and Price(Annual)', 'A28')
    _draw_plot2(workbook, sheet, '=Summary!$B$1:$P$1', '=Summary!$A$53','=Summary!$B$53:$P$53','=Summary!$A$54','=Summary!$B$54:$P$54','Positive-Negative and Price(Interim)','A77')

def _draw_plot2(workbook, sheet, cat, name1, val1, name2, val2, title, des):
    # Create a chart and a line chart
    chart = workbook.add_chart({'type':'column'})
    line_chart = workbook.add_chart({'type':'line'})

    # Insert data
    chart.add_series({'name':name1, 'categories':cat, 'values':val1,})
    line_chart.add_series({'name':name2, 'categories':cat, 'values':val2, 'y2_axis': True,})
    
    chart.set_title({'name': title})
    chart.set_x_axis({'name':"Year"})
    chart.set_y_axis({'name':'Frequency'})
    chart.set_style(10)
    chart.set_size({'x_scale': 2.13, 'y_scale': 1.5})
    
    line_chart.set_y2_axis({'name':'Price'})
    chart.combine(line_chart)
    sheet.insert_chart(des, chart)

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
                Date = sheet.cell(r,c).value.split() 
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
    if data == tuple():
        return _converted_price(_converted_dates(Date), stock, Stocks_Prices)
    return float(data[-2])

if __name__ == "__main__":
    conn = connect('172.31.238.166', 3306, 'root', 'root', 'stock')
    stock_list = ['00316','00590','01171']
    Stocks_Prices = stocks_prices(conn, stock_list)
    conn.close()
    file_path = '/usr/yyy/wk2/reports release dates/'
    annual_release = release_dates(stock_list, file_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, file_path + 'interim.xlsx', 'interim')
    annual_prices =  prices(stock_list, annual_release,  Stocks_Prices)
    interim_prices = prices(stock_list, interim_release, Stocks_Prices)
    
    root_path = "/usr/yyy/self testing/excel_freq/"
    result_path = "/usr/yyy/wk2/excel_summary_with_price/"
    dictionary_path = "/usr/yyy/self testing/Dictionary.xlsx" 
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    excel_list = os.listdir(root_path)
    for file_name in excel_list:
        file_path = root_path + file_name
        pos_words, neg_words = read_dictionary(dictionary_path)
        sheet_annual, sheet_interim = read_excel(file_path)
        annual_pos,  annual_neg  = analyze_sheet(pos_words, neg_words, sheet_annual)
        interim_pos, interim_neg = analyze_sheet(pos_words, neg_words, sheet_interim)
        workbook = xlsxwriter.Workbook(result_path + '/' + file_name[:5] + '_summary.xlsx')
        save_into_excel(workbook, file_name[:5], annual_pos, annual_neg, interim_pos, interim_neg, annual_prices, interim_prices)
        print file_name[:5] + ' saved successfully.'

    print '----------------Done------------'


# In[ ]:





# In[ ]:




