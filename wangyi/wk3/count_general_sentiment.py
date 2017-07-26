
# coding: utf-8

# In[ ]:


import os
import xlwt
from collections import defaultdict

def read_dictionary(dictionary_path):
    result = dict()
    for file_name in os.listdir(dictionary_path):
        result[file_name[:-4]] = [line[:-3].upper() for line in open(dictionary_path + file_name)]        
    return result

def Stocks_info_dict(root_path, dictionary):
    stock_dict = dict()
    for stock_name in set(file_name[:5] for file_name in os.listdir(root_path)):
        year_dict_a = defaultdict(dict) # make sure every time checks if the year exists
        year_dict_i = defaultdict(dict) # make sure every time checks if the year exists
        
        for file_name in sorted(os.listdir(root_path)):
            if file_name[:5] == stock_name:
                year = file_name[6:10]
                if file_name.split('_')[2] == 'Annual':
                    year_dict_a[year] = _analyze_txt_str(_extract_txt(root_path + file_name), dictionary)
                else:
                    year_dict_i[year] = _analyze_txt_str(_extract_txt(root_path + file_name), dictionary)
        stock_dict[stock_name] = [year_dict_a, year_dict_i]
    return stock_dict

# returns the string of the file
def _extract_txt(file_path):
    lines = open(file_path, 'r').readlines()
    if len(lines) == 0:
        return ''
    return lines[0].upper()

def _analyze_txt_str(txt_str, dictionary):
    result_dict = dict()
    for determinant in dictionary:
        d = dict()
        for phrase in dictionary[determinant]:
            d[phrase] = txt_str.count(phrase)
        result_dict[determinant] = d
    return result_dict

def save_into_excel(result_path, stock_dict):
    for stock_name in stock_dict:
        workbook =  xlwt.Workbook()

        _create_sheets(workbook, stock_dict[stock_name][0],  stock_name, 'Annual')
        _create_sheets(workbook, stock_dict[stock_name][1],  stock_name, 'Interim')

        workbook.save(result_path + stock_name + '_General_Sentiment_count.xls')
        print result_path + stock_name + '_General_Sentiment_count.xls', 'completed\n'

def _create_sheets(workbook, data, stock_name, tag):
    Positive_Evaluation = workbook.add_sheet('Positive_Evaluation_' + tag)
    Negative_Evaluation = workbook.add_sheet('Negative_Evaluation_' + tag)
    Positive_Emotion    = workbook.add_sheet('Positive_Emotion_'    + tag)
    Negative_Emotion    = workbook.add_sheet('Negative_Emotion_'    + tag)    
    
    _write_sheets(Positive_Evaluation, data, tag.lower() + ' positive evaluation')
    _write_sheets(Negative_Evaluation, data, tag.lower() + ' negative evaluation')
    _write_sheets(Positive_Emotion,    data, tag.lower() + ' positive emotion')
    _write_sheets(Negative_Emotion,    data, tag.lower() + ' negative emotion')

def _write_sheets(sheet, data, tag):
    sheet.write(0,0, tag)
    determinant = ' '.join([word.capitalize() for word in tag.split()[1:]])
    phrases = set()
    col = 1
    for year in sorted(data):
        sheet.write(0,col, year)
        for phrase in data[year][determinant]:
            try:
                phrases.add(unicode(phrase, 'utf-8'))
            except:
                pass
        col += 1
    phrases = sorted(phrases)

    row = 1
    for phrase in phrases:
        sheet.write(row, 0, phrase)
        col = 1
        for year in sorted(data):
            sheet.write(row, col, data[year][determinant][phrase])
            col += 1        
        row += 1

if __name__ =='__main__':
    root_path = '/usr/yyy/self testing/txt_tagged_init/'
    result_path = '/usr/yyy/wk3/Count_General_Sentiment/'
    dictionary_path = '/usr/yyy/dictionaries/general sentiment dictionary/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    dictionary = read_dictionary(dictionary_path)
    stock_dict = Stocks_info_dict(root_path, dictionary)
    save_into_excel(result_path, stock_dict)

    print '-----------Done------------'


# In[ ]:




