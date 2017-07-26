
# coding: utf-8

# In[ ]:


import xlrd
import xlsxwriter

import os
from collections import defaultdict

# returns a lsit of positive words and a list of negative words
def read_dictionary(file_path):
    pos_words = []
    neg_words = []
    data = xlrd.open_workbook(file_path)
    sheet = data.sheet_by_name("LoughranMcDonald_MasterDictiona")
    title = sheet.row_values(0)   
    for i in range(sheet.ncols):
        if title[i] == 'Word':
            words = sheet.col_values(i)[1:]
        elif title[i] == 'Positive':
            pos = [int(i) for i in sheet.col_values(i)[1:]]
        elif title[i] == 'Negative':
            neg = [int(i) for i in sheet.col_values(i)[1:]]   
    for i in range(sheet.nrows - 1):
        if pos[i] != 0:
            pos_words.append(words[i])
        if neg[i] != 0:
            neg_words.append(words[i])
    return pos_words, neg_words
        
def read_excel(file_path):
    data = xlrd.open_workbook(file_path)
    sheet_annual = data.sheet_by_name("Annual")
    sheet_interim = data.sheet_by_name("Interim")
    return sheet_annual, sheet_interim
    
def analyze_sheet(pos_words, neg_words, sheet):
    pos_list = []
    neg_list = []  
    for i in range(sheet.ncols):
        if sheet.cell(0,i).value == 'word':
            pos = defaultdict(int)
            neg = defaultdict(int)
            for word_index in range(sheet.nrows - 1):
                word = sheet.col_values(i)[word_index+1].upper()
                if word != '':
                    if word in pos_words:
                        pos[word] += int(sheet.col_values(i+1)[word_index+1])
                    if word in neg_words:
                        neg[word] += int(sheet.col_values(i+1)[word_index+1])
            pos_list.append((sheet.row_values(0)[i+1],pos))
            neg_list.append((sheet.row_values(0)[i+1],neg))
    return pos_list, neg_list
                      
def save_into_excel(result_path, stock, annual_pos, annual_neg, interim_pos, interim_neg):
    workbook = xlsxwriter.Workbook(result_path + '/' + stock + '_summary.xls')
    Positive_Annual = workbook.add_worksheet("Positive_Annual")
    Negative_Annual = workbook.add_worksheet("Negative_Annual")
    Positive_Interim = workbook.add_worksheet("Positive_Interim")
    Negative_Interim = workbook.add_worksheet("Negative_Interim")
    Summary = workbook.add_worksheet('Summary')
    _write_sheet(Positive_Annual, annual_pos, 'positive')
    _write_sheet(Negative_Annual, annual_neg, 'negative')
    _write_sheet(Positive_Interim, interim_pos, 'positive')
    _write_sheet(Negative_Interim, interim_neg, 'negative')
    _write_summary(workbook, Summary, annual_pos, annual_neg, interim_pos, interim_neg)

def _word_set(data):
    s = set()
    for year_data in data:
        for word in year_data[1]:
            s.add(word)
    return s

def _write_sheet(sheet, data, flag):
    sheet.write(0,0, flag)
    col = 1
    for year_data in data:
        sheet.write(0, col, year_data[0])
        col += 1
    word_set = _word_set(data)
    row = 1
    col = 1
    for word in word_set:
        sheet.write(row, 0, word)
        for year_data in data:
            sheet.write(row, col, year_data[1][word])
            col += 1       
        row += 1
        col = 1

def _year_list(annual, interim):
    s = set()
    for year_data in annual:
        s.add(year_data[0])
    for year_data in interim:
        s.add(year_data[0])
    return sorted(list(s))

def _count_freq(data, year):
    result = 0
    for year_data in data:
        if year_data[0] == year:
            for freq in year_data[1].values():
                result += freq
            break
    return result
    
def _draw_plot1(workbook, sheet, cat, name1, val1, name2, val2, title, des):
    chart = workbook.add_chart({'type':'column'})
    chart.add_series({'name':name1, 'categories':cat, 'values':val1,})
    chart.add_series({'name':name2, 'categories':cat, 'values':val2,})
    chart.set_title({'name': title})
    chart.set_style(10)
    chart.set_size({'x_scale': 2.13, 'y_scale': 1.5})
    sheet.insert_chart(des, chart)
    
def _draw_plot2(workbook, sheet, cat, name, val, title, des):
    chart = workbook.add_chart({'type':'column'})
    chart.add_series({'name':name, 'categories':cat, 'values':val,})
    chart.set_title({'name': title})
    chart.set_style(10)
    chart.set_size({'x_scale': 2.13, 'y_scale': 1.5})
    sheet.insert_chart(des, chart)

if __name__ == "__main__":
    def _write_summary(workbook, sheet, annual_pos, annual_neg, interim_pos, interim_neg):
        year_list = _year_list(annual_pos, interim_pos)
        col = 1 
        for year in year_list:
            sheet.write(0, col, year)
            col += 1
        sheet.write(1,0, 'Positive(Annual)')
        sheet.write(2,0, 'Negative(Annual)')
        sheet.write(3,0, 'Positive-Negative(Annual)')
        sheet.write(49,0, 'Positive(Interim)')
        sheet.write(50,0, 'Negative(Interim)')
        sheet.write(51,0, 'Positive-Negative(Interim)') 
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
            sheet.write(row + 48, col, interim_pos_freq)
            sheet.write(row + 49, col, interim_neg_freq)
            sheet.write(row + 50, col, interim_pos_freq - interim_neg_freq)
            col += 1
        _draw_plot1(workbook, sheet, '=Summary!$B$1:$P$1', "=Summary!$A$2", '=Summary!$B$2:$P$2',  '=Summary!$A$3', '=Summary!$B$3:$P$3',  'Annual Report Plot', 'A5' )  
        _draw_plot1(workbook, sheet, '=Summary!$B$1:$P$1', "=Summary!$A$50",'=Summary!$B$50:$P$50','=Summary!$A$51','=Summary!$B$51:$P$51','Interim Report Plot','A53')
        _draw_plot2(workbook, sheet, '=Summary!$B$1:$P$1', '=Summary!$A$4', '=Summary!$B$4:$P$4', 'Annual','A27')
        _draw_plot2(workbook, sheet, '=Summary!$B$1:$P$1', '=Summary!$A$52','=Summary!$B$52:$P$52','Interim','A75')

    root_path = "/usr/yyy/self testing/excel_freq/"
    result_path = "/usr/yyy/wk2/excel_summary/"
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
        save_into_excel(result_path, file_name[:5], annual_pos, annual_neg, interim_pos, interim_neg)
        print file_name + ' save successfully.'

    print '-------------------Done-----------------------'

