import os
import csv
import xlrd
import xlwt
from collections import defaultdict

def read_dictionary(dictionary_path):
    result = dict()
    for file_name in os.listdir(dictionary_path):
        csv_reader = csv.reader(open(dictionary_path + file_name))
        result[file_name[:-4]] = [row[0] for row in csv_reader]
    return result

def read_excel(file_path):
    data = xlrd.open_workbook(file_path)
    sheet_annual = data.sheet_by_name("Annual")
    sheet_interim = data.sheet_by_name("Interim")
    return sheet_annual, sheet_interim

"A list of tuples, which is ('year', defaultdict(int)), which is word:int "
def analyze_sheet(dictionary, sheet):
    keys = sorted(dictionary.keys())
    l = []
    for k in range(len(keys)):
        l.append([])
    for i in range(sheet.ncols):
        if sheet.cell(0,i).value == 'word':  
            _l = []
            for k in range(len(keys)):
                _l.append(  defaultdict(float)  )
            for word_index in range(sheet.nrows - 1):
                word = sheet.col_values(i)[word_index+1].upper()
                if word != '':         
                    for determinant_index in range(len(keys)):
                        if word in dictionary[keys[determinant_index]]:
                            _l[determinant_index][word] += float(sheet.col_values(i+1)[word_index+1])
            for determinant_index in range(len(keys)):
                l[determinant_index].append((sheet.row_values(0)[i+1], _l[determinant_index]))
    return l

def save_into_excel(stock, dictionary, sheet_annual, sheet_interim, result_file_path):
    workbook = xlwt.Workbook()
 
    keys = sorted(dictionary.keys())
    list_a = analyze_sheet(dictionary, sheet_annual)
    list_i = analyze_sheet(dictionary, sheet_interim)

    for determinant_index in range(len(keys)):
        Annual_Sheet  = workbook.add_sheet(keys[determinant_index] + '_Annual')
        Interim_Sheet = workbook.add_sheet(keys[determinant_index] + '_Interim')
        _write_sheet(Annual_Sheet,  list_a[determinant_index], 'annual '  + keys[determinant_index].lower())
        _write_sheet(Interim_Sheet, list_i[determinant_index], 'interim ' + keys[determinant_index].lower())

    workbook.save(result_file_path)

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

