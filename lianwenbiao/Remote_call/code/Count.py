import os
import csv
import xlrd
import xlwt
from collections import defaultdict


def read_dictionary(dictionary_path):
    '''
    functionality: reads a dictionary that has the same format as McDonald Dictionary
    
    input: the path of the dictioary
    
    return: a dict 
            The keys are the determinants (such as positive, negative ...) 
            and the values are a list of words that satisfy the determinant.
       
    '''
    
    result = dict()
    for file_name in os.listdir(dictionary_path):
        csv_reader = csv.reader(open(dictionary_path + file_name))
        result[file_name[:-4]] = [row[0] for row in csv_reader]
    return result

def read_excel(file_path):
    '''
    functionality: reads an excel file in excel_freq
    
    input: the path of the file
    
    return: a tuple of the annual sheet and the interim sheet in the file
     
    '''
    
    data = xlrd.open_workbook(file_path)
    sheet_annual = data.sheet_by_name("Annual")
    sheet_interim = data.sheet_by_name("Interim")
    return sheet_annual, sheet_interim

"A list of tuples, which is ('year', defaultdict(int)), which is word:int "
def analyze_sheet(dictionary, sheet):
    '''
    functionality: reads an excel file and stores the frequency for each word that is in the determinant
    
    input: the dictionary that is obtained from read_ditionary(dictionary_path),
           annual sheet or interim sheet obtained from read_excel(file_path).
    
    return: a list of lists.
            Each sub-list is for a determinant for that dictionary
            Each sub-list is a ('year', dict), tuple[0] is the 'year', tuple[1] is a dict.
            Each dict has words as keys and frequencies for those words as values.
            
            For example,
                info = analyze(dictionary, sheet_annual)
                print info[0][0][0]           --------> the year
                print info[0][0][1]['happy']  --------> the frequency of happy in that year
     
    '''
    
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

def save_into_excel(stock, dictionary1, dictionary2, dictionary3, sheet_annual, sheet_interim, result_file_path):
    '''
    functionality: save the information into an excel file
    
    input: the name of a stock, for example: '00371'
           the dictionary that is obtained from read_ditionary(dictionary_path)
           annual sheet obtained from read_excel(file_path)[0]
           interim sheet obtained from read_excel(file_path)[1]
           the destination path for storing the excel file
    
    return: None
     
    '''
    workbook = xlwt.Workbook()
 
    keys = sorted(dictionary1.keys())
    list_a = analyze_sheet(dictionary1, sheet_annual)
    list_i = analyze_sheet(dictionary1, sheet_interim)

    for determinant_index in range(len(keys)):
        Annual_Sheet  = workbook.add_sheet('Harvard_' + keys[determinant_index] + '_Annual')
        Interim_Sheet = workbook.add_sheet('Harvard_' + keys[determinant_index] + '_Interim')
        _write_sheet(Annual_Sheet,  list_a[determinant_index], 'annual '  + keys[determinant_index].lower())
        _write_sheet(Interim_Sheet, list_i[determinant_index], 'interim ' + keys[determinant_index].lower())


    keys = sorted(dictionary2.keys())
    list_a = analyze_sheet(dictionary2, sheet_annual)
    list_i = analyze_sheet(dictionary2, sheet_interim)

    for determinant_index in range(len(keys)):
        Annual_Sheet  = workbook.add_sheet('Lasswell_' + keys[determinant_index] + '_Annual')
        Interim_Sheet = workbook.add_sheet('Lasswell_' + keys[determinant_index] + '_Interim')
        _write_sheet(Annual_Sheet,  list_a[determinant_index], 'annual '  + keys[determinant_index].lower())
        _write_sheet(Interim_Sheet, list_i[determinant_index], 'interim ' + keys[determinant_index].lower())


    keys = sorted(dictionary3.keys())
    list_a = analyze_sheet(dictionary3, sheet_annual)
    list_i = analyze_sheet(dictionary3, sheet_interim)

    for determinant_index in range(len(keys)):
        Annual_Sheet  = workbook.add_sheet('McDonald_' + keys[determinant_index] + '_Annual')
        Interim_Sheet = workbook.add_sheet('McDonald_' + keys[determinant_index] + '_Interim')
        _write_sheet(Annual_Sheet,  list_a[determinant_index], 'annual '  + keys[determinant_index].lower())
        _write_sheet(Interim_Sheet, list_i[determinant_index], 'interim ' + keys[determinant_index].lower())


    workbook.save(result_file_path)


def _write_sheet(sheet, data, flag):
    '''
    functionality: stores all the information in the data to the sheet
    
    input: the sheet in which you want to write
           the data in the form of ('year', dict). details in analyze_sheet(dictionary, sheet)
           flag is either 'annual' or 'interim'
    
    return: None
    
    '''
    
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

def _word_set(data):
    '''
    functionality: getting a word set
    
    input: the data in the form of ('year', dict). details in analyze_sheet(dictionary, sheet)
    
    return: a set of words
     
    '''
    
    s = set()
    for year_data in data:
        for word in year_data[1]:
            s.add(word)
    return s
