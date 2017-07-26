
# coding: utf-8

# In[13]:


import os
import xlwt
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def get_stock_dir(root_path):
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
    for k in d:
        d[k] = sorted(d[k])

def _concat_dicts(d1, d2):
    result = defaultdict(list)
    for k in d1:
        result[k] = d1[k] + d2[k]
    return result

def get_txt_dir(stock_dir):
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

def get_TFIDF(stock_dir, txt_dir):
    result = dict()
    
    for stock_name in txt_dir:
        
        l = [defaultdict(dict), defaultdict(dict)] # l[0] is annual, l[1] is interim
        
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(txt_dir[stock_name]))
        weights = tfidf.toarray()
        words = vectorizer.get_feature_names()
        l.append(words)
        
        for file_index in range(len(weights)):
            if not any(weights[file_index]):
                continue
            
            year = stock_dir[stock_name][file_index].split('_')[-3]
            file_dict = dict()

            for word_index in range(len(words)):
                file_dict[words[word_index]] = weights[file_index][word_index]
            
            if '_Annual_' in stock_dir[stock_name][file_index]:
                l[0][year] = file_dict
            else:
                l[1][year] = file_dict              
        result[stock_name] = l
    return result

def save_into_excel(result_path, data):
    for stock_name in data:
        result_file_path =  result_path + stock_name + '_words_weights.xls'
        workbook = xlwt.Workbook()
        words = data[stock_name][2]        
        Annual_Sheet  = workbook.add_sheet('Annual')
        Interim_Sheet = workbook.add_sheet('Interim')
        
        _write_sheet(workbook, Annual_Sheet,  words, data[stock_name][0])
        _write_sheet(workbook, Interim_Sheet, words, data[stock_name][1])
        
        workbook.save(result_file_path)
        print result_file_path, 'saved successfully.'

def _write_sheet(workbook, sheet, words, datum):
    col = 0
    for year in sorted(datum):
        sheet.write(0,col,'word')
        sheet.write(0,col+1, year)
        row = 1
        nd = sorted(datum[year].items(), key = (lambda x: x[1]), reverse = True)
        
        for word, weight in nd:
            if weight != 0:
                sheet.write(row, col, word)
                sheet.write(row, col+1, weight)
                row += 1
        col += 2




if __name__ == '__main__':
    root_path = '/usr/yyy/self testing/txt_tagged_init/'
    result_path = '/usr/yyy/self testing/txt_wighted/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    stock_dir = get_stock_dir(root_path)
    txt_dir = get_txt_dir(stock_dir)
    data = get_TFIDF(stock_dir, txt_dir)
    
    save_into_excel(result_path, data)

    

    print '-------------Done------------'




# In[ ]:




