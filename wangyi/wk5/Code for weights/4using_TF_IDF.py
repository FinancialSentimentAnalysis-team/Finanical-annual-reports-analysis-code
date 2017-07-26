
# coding: utf-8

# In[1]:


import os
import xlwt
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def get_stock_dir(root_path):
    '''
    functionality: reads a txt file and returns a dict of file names
    
    input: a file path in txt_tagged_init directory
    
    return: a dict
            The keys are stock names. The values are a list of file paths that belong to the stock
    
    '''
    
    result_a = defaultdict(list)
    result_i = defaultdict(list)
    
    for file_name in os.listdir(root_path):
        if "_Annual_" in file_name:
            result_a[file_name[:5]].append(root_path + file_name)
        else:
            result_i[file_name[:5]].append(root_path + file_name)
    
    _sort_dict(result_a)
    _sort_dict(result_i)
    result = _concat_dicts(result_a, result_i)
    return result

def _sort_dict(d):
    '''
    functionality: assuming the values of the dict are lists, sorts the values
    
    input: a dict that has stock names as keys and lists of file paths as values
    
    return: None
    '''
    
    for k in d:
        d[k] = sorted(d[k])

def _concat_dicts(d1, d2):
    '''
    functionality: assuming the values of the dicts are lists, combines these two dicts into one dict
    
    input: a dict representing annual that has stock names as keys and lists of file paths as values
           a dict representing interim that has stock names as keys and lists of file paths as values
    
    return: a combined dict with the same format as the input dicts.
    '''
    
    result = defaultdict(list)
    for k in d1:
        result[k] = d1[k] + d2[k]
    return result

def get_txt_dir(stock_dir):
    '''
    functionality: returns the text string in each file
    
    input: a dict obtained from get_stock_dir(root_path)
    
    return: a dict
            The keys are stock names. The values are lists of text strings; each position of the 
            text string matches the position of the file name in stock_dir[stock_name]
    '''
    
    result = defaultdict(list)
    for stock_name in stock_dir:
        for file_name in stock_dir[stock_name]:
            open_file = open(file_name, 'r')
            content = open_file.readlines()
            open_file.close()
            if len(content) == 0:
                content = ''
            else:
                content = content[0]
            result[stock_name].append(content)
    return result

def get_TFIDF(root_path):
    '''
    functionality: calculates the TF-IDF of the data. The domain is all the files for annual and for interim
    
    input: a file path in txt_tagged_init directory
    
    return: a dict
            The keys are stock names. The values are a list of three element.
                list[0] is a dict for annual
                    In this dict, keys are years and values are sub-dict
                        In this sub-dict, keys are words and values are the weights corresponding to the words
                list[1] is a dict for interim
                    In this dict, keys are years and values are sub-dict
                        In this sub-dict, keys are words and values are the weights corresponding to the words
                list[2] is a list of words

    '''

    stock_dir = get_stock_dir(root_path)
    txt_dir = get_txt_dir(stock_dir)
    # stock_dir: key = stock_name, value = list of file_name    
    # txt_dir  : key = stock_name, value = list of txt_str

    stock_names = sorted(stock_dir.keys())
    
    full_txt_list = [] 
    for stock_name in stock_names:
        for txt_str in txt_dir[stock_name]:
            full_txt_list.append(txt_str)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()        
    tfidf = transformer.fit_transform(vectorizer.fit_transform(full_txt_list))            
    weights = tfidf.toarray() # list of sub-lists, each sub-list is the weight of a word
    words = vectorizer.get_feature_names()            

    txt_freq_dict = dict()
    
    for txt_index in range(len(full_txt_list)):
        if any(weights[txt_index]):
            txt_freq_dict[full_txt_list[txt_index]] = weights[txt_index]
    
    file_freq_dict = dict()
    
    for stock_name in stock_names:
        stock_file_list = stock_dir[stock_name]
        stock_txt_list = txt_dir[stock_name]
        for i in range(len(stock_txt_list)):
            if stock_txt_list[i] in txt_freq_dict.keys():
                file_freq_dict[stock_file_list[i].split('/')[-1]] = txt_freq_dict[stock_txt_list[i]]

    result = dict()
    
    for stock_name in stock_names:
        l = [defaultdict(dict), defaultdict(dict)] # l[0] is annual, l[1] is interim
        l.append(words)
        
        for stock_file in file_freq_dict:
            if stock_name in stock_file:
                stock_info = stock_file.split('_')[:3] # returns [stock_name, year, term]
                _modify_dict(l[0], words, stock_info, file_freq_dict[stock_file], 'Annual')
                _modify_dict(l[1], words, stock_info, file_freq_dict[stock_file], 'Interim')
                
        result[stock_name] = l
    return result

def _modify_dict(result_dict, words, stock_info, freq_list, term):
    '''
    functionality: modifies the result_dict such that the keys will be years and the values will be dicts of words with weights
    
    input: a dict
           a list of words
           a list of information with the format : [stock_name, year, term]
           the term is either 'Annual' or 'Interim'
    
    return: None
    '''
    
    if term == stock_info[2]:
        words_dict = dict()
        for word_index in range(len(words)):
            words_dict[words[word_index]] = freq_list[word_index]
        result_dict[stock_info[1]] = words_dict

def save_into_excel(result_path, data):
    '''
    functionality: saves the data into the destination result path
    
    input: a dict obtained from get_TFIDF(root_path)
    
    return: None
    '''
    
    for stock_name in data:
        result_file_path =  result_path + stock_name + '_words_weights.xls'
        workbook = xlwt.Workbook()
        words = data[stock_name][2]        
        Annual_Sheet  = workbook.add_sheet('Annual')
        Interim_Sheet = workbook.add_sheet('Interim')
        
        _write_sheet(Annual_Sheet,  words, data[stock_name][0])
        _write_sheet(Interim_Sheet, words, data[stock_name][1])
        
        workbook.save(result_file_path)
        print result_file_path, 'saved successfully.'

def _write_sheet(sheet, words, datum):
    '''
    functionality: stores all the information in the data to the sheet
    
    input: the sheet in which you want to write
           a list of words
           a dict with the keys wof years and the values of dicts of words with weights
    
    return: None
    
    '''
    
    col = 0
    for year in sorted(datum):
        sheet.write(0,col,'word')
        sheet.write(0,col+1, year)
        row = 1
        sorted_list = sorted(datum[year].items(), key = (lambda x: x[1]), reverse = True)
        
        for word, weight in sorted_list:
            if weight != 0:
                sheet.write(row, col, word)
                sheet.write(row, col+1, weight)
                row += 1
        col += 2

if __name__ == '__main__':
    root_path = '/usr/yyy/wk5/txt_tagged_init/'
    result_path = '/usr/yyy/wk5/excel_weighted/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    data = get_TFIDF(root_path)
    
    save_into_excel(result_path, data)

    print '-------------Done------------'




# In[ ]:




