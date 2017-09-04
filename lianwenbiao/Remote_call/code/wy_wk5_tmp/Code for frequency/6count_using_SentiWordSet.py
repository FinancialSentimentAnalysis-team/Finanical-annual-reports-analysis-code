
# coding: utf-8

# In[2]:


import os
import xlwt
import csv
from collections import defaultdict

def read_dictionary_for_SentiWordSet(dictionary_path):
    '''
    functionality: reads the SentiWordNet Dictionary
    
    input: the path of the dictioary
    
    return: a tuple of two dicts (you can call them postive_dictionary and negative_dictionary)
            Each dict has words as dict, tuple of (positive score, negative score) as values.

    '''
    
    d = defaultdict(list)
    csv_file = open(dictionary_path, 'r')
    reader = csv.reader(csv_file)
    for line in reader:
        if line[0] != 'POS':
            for word in line[4].split(','):
                d[word[:-2]].append((word.split('#')[0] + '#' + line[0], line[2], line[3]))
    csv_file.close()
    pos_result_dict = dict()
    neg_result_dict = dict()
    for word in d:
        dic = dict()        
        _property = set(word_info[0] for word_info in d[word])
        for word_with_property in _property:
            dic[word_with_property] = [0,0]
        for word_with_property in _property:
            count = 0
            for word_info in d[word]:
                if word_info[0] == word_with_property:
                    count += 1
                    dic[word_with_property][0] += float(word_info[1])
                    dic[word_with_property][1] += float(word_info[2])
            dic[word_with_property][0] /= count
            dic[word_with_property][1] /= count
        for key, value in dic.items():
            if value[0] != 0:
                pos_result_dict[key.strip()] = value
            if value[1] != 0:
                neg_result_dict[key.strip()] = value
    return pos_result_dict, neg_result_dict

def Stocks_info_dict(root_path, pos_dictionary, neg_dictionary):
    '''
    functionality: given a tagged txt file, analyzes the file and stores the information into a dict
    
    input: the path of the tagged txt file
           the positive dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
           the negative dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
    
    return: a dict
            The keys are the names of stocks, the values are a list of two dicts.
            Each sub-dict is either for annual or for interim.
            Each key in a sub-dict is the year, each value in a sub-dict is also a dict. Detail in _analyze_txt_str(txt_str, pos_dictionary, neg_dictionary)

    '''
    
    stock_dict = dict()
    for stock_name in set(file_name[:5] for file_name in os.listdir(root_path)):
        year_dict_a = defaultdict(dict) # make sure every time checks if the year exists
        year_dict_i = defaultdict(dict) # make sure every time checks if the year exists
        
        for file_name in sorted(os.listdir(root_path)):
            if file_name[:5] == stock_name:
                year = file_name[6:10]
                if file_name.split('_')[2] == 'Annual':
                    year_dict_a[year] = _analyze_txt_str(_extract_txt(root_path + file_name), pos_dictionary, neg_dictionary)
                else:
                    year_dict_i[year] = _analyze_txt_str(_extract_txt(root_path + file_name), pos_dictionary, neg_dictionary)
        stock_dict[stock_name] = [year_dict_a, year_dict_i]
    return stock_dict

def _analyze_txt_str(txt_str, pos_dictionary, neg_dictionary):
    '''
    functionality: returns a dict of information
    
    input: a str of txt
           the positive dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
           the negative dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)    
    
    return: a dict
            There are two keys in the dict: 'positive', 'negative'.
            The values are sub-dict.
            Each sub-dict has words as keys and frequencies as values
            
    '''
    
    word_dict = defaultdict(int)
    for word in txt_str.split():
        word_dict[word] += 1
    pos_result_dict = dict()
    neg_result_dict = dict()
    for word in pos_dictionary:
        pos_result_dict[word] = word_dict[word]
    for word in neg_dictionary:
        neg_result_dict[word] = word_dict[word]
    result_dict = dict()
    result_dict['positive'] = pos_result_dict
    result_dict['negative'] = neg_result_dict
    return result_dict

# returns the string of the file
def _extract_txt(file_path):
    '''
    functionality: returns a str of text in the txt file
    
    input: the path of the tagged txt file
    
    return: str of text
            
    '''
    
    o = open(file_path, 'r')
    lines = o.readlines()
    if len(lines) == 0:
        return ''
    result = ''
    for word_property_init in lines[0].split():
        new_word = _alter_word(word_property_init)
        if new_word != '':
            result += new_word + ' '
    o.close()
    return result

def _alter_word(word_property_init):
    '''
    functionality: returns the word in a different format
    
    input: a tagged word
    
    return: a str having the word with its part-of-speech
            
    '''
    
    word_info = word_property_init.split('_')
    _property = word_info[1].upper()
    if _property in ['JJ', 'JJS','JJR']:
        return word_info[2].lower() + '#a'
    elif _property in ['RB', 'RBR', 'RBS']:
        return word_info[2].lower() + '#r'
    elif _property in ['NN', 'NNS', 'NP', 'NPS']:
        return word_info[2].lower() + '#n'
    elif 'V' in _property:
        return word_info[2].lower() + '#v'
    return ''

def save_into_excel(result_path, stock_dict):
    '''
    functionality: save the data into the result_path
    
    input: the destination where you want to store
           the dict obtained from Stocks_info_dict(root_path, pos_dictionary, neg_dictionary)
    
    return: None
            
    '''
    
    for stock_name in stock_dict:
        workbook =  xlwt.Workbook()

        _create_sheets(workbook, stock_dict[stock_name][0],  stock_name, 'Annual')
        _create_sheets(workbook, stock_dict[stock_name][1],  stock_name, 'Interim')

        workbook.save(result_path + stock_name + '_SentiWordSet_count.xls')
        print result_path + stock_name + '_SentiWordSet_count.xls', 'completed\n'

def _create_sheets(workbook, data, stock_name, tag):
    '''
    functionality: creates an annual sheet and an interim sheet
    
    input: the workbook object
           the dict: keys are years, values are sub-dicts.
                     each sub-dict: keys are categories (you can also say determinants), values are sub-sub-dict
                     each sub-sub-dict: keys are words, values are frequencies
           tag is either 'Annual' or 'Interim'
    
    return: None
            
    '''
    
    Positive = workbook.add_sheet('Positive_' + tag)
    Negative = workbook.add_sheet('Negative_' + tag)    
    
    _write_sheets(Positive, data, tag.lower() + ' positive')
    _write_sheets(Negative, data, tag.lower() + ' negative')


def _write_sheets(sheet, data, tag):
    '''
    functionality: stores the data into the sheet
    
    input: the sheet you want to write in
           the dict: keys are years, values are sub-dicts.
                     each sub-dict: keys are categories (you can also say determinants), values are sub-sub-dict
                     each sub-sub-dict: keys are words, values are frequencies
           tag is either 'Annual' or 'Interim'
    
    return: None
            
    '''
    
    sheet.write(0,0, tag)
    determinant = tag.split()[1]
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

if __name__ == "__main__":
    root_path = '/usr/yyy/wk5/txt_tagged/'
    result_path = '/usr/yyy/wk5/Count/SentiWordSet/'
    dictionary_path = '/usr/yyy/dictionaries/SentiWordNet_filtered.csv'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
        
    pos_dictionary, neg_dictionary = read_dictionary_for_SentiWordSet(dictionary_path)
    
    stock_dict = Stocks_info_dict(root_path, pos_dictionary, neg_dictionary)
    
    save_into_excel(result_path, stock_dict)

    print '------------Done-------------'
    


# In[ ]:




