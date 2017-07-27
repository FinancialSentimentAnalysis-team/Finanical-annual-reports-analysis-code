
# coding: utf-8

# In[1]:


from Summary import *
import csv

def read_dictionary_for_SentiWordNet(dictionary_path):
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

def read_excel_for_SentiWordNet(file_path, pos_dictionary, neg_dictionary):
    '''
    functionality: reads an excel file in Count
    
    input: the path of the file
           the positive dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
           the negative dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
           
    return: a list of two dicts
            list[0] is for annual, which is a dict having year as keys and sub-dict as values
            list[1] is for interim, which is a dict having year as keys and sub-dict as values
            Each sub-dict has 'positive' and 'megative' as years and the sum(each word's weight * its frequency) as value
            
    '''
    
    workbook = xlrd.open_workbook(file_path)
    result = list()
    result.append(dict()) # dict of year: info, for annual
    result.append(dict()) # dict of year: info, for interim
    year = 2002
    for i in range(15):
        result[0][str(year+i)] = dict() # for each category
        result[1][str(year+i)] = dict() # for each category
    
    for sheet_name in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheet_name)
        info = sheet.cell_value(0,0).split()
        
        if info[0] == 'annual':
            _modify_dict_for_SentiWordNet(result[0], ' '.join(info[1:]), sheet, pos_dictionary, neg_dictionary)
        else:
            _modify_dict_for_SentiWordNet(result[1], ' '.join(info[1:]), sheet, pos_dictionary, neg_dictionary)
    return result

def _modify_dict_for_SentiWordNet(d, category, sheet, pos_dictionary, neg_dictionary):
    '''
    functionality: modify the dicts described in read_excel_for_SentiWordNet(file_path, pos_dictionary, neg_dictionary)
    
    input: the dict for annual or the dict for interim
           one single cateogry (or you can call it determinant)
           the sheet in which you want to write
           the positive dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
           the negative dictionary obtained from read_dictionary_for_SentiWordNet(dictionary_path)
           
    return: None
    '''
   
    for col in range(sheet.ncols-1):
        s = 0
        for row in range(sheet.nrows-1):
            if category == 'positive':
                weight = pos_dictionary[sheet.cell_value(row+1, 0)][0]
            else:
                weight = neg_dictionary[sheet.cell_value(row+1, 0)][1]
            s += int(sheet.cell_value(row+1, col+1)) * weight
        year = sheet.cell_value(0, col+1)
        if year != '2017':
            d[year][category] = s

def save_into_excel_for_SentiWordNet(stock_name, result_path, data, stock_list, annual_release, interim_release, Stocks_Prices):
    '''
    functionality: save the information into an excel file
    
    input: the name of a stock, for example: '00371'
           the destination directory path
           object returned by read_excel_for_SentiWordNet(file_path, pos_dictionary, neg_dictionary)
           the list of stocks you are interested in
           the annual reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)
           the interim reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)  
           
    return: None
     
    '''
    
    workbook =  xlwt.Workbook()
    Annual = workbook.add_sheet("Annual")
    Interim = workbook.add_sheet("Interim")
    _write_sheet_for_SentiWordNet(Annual,  data[0], 'Annual', stock_name, stock_list,  annual_release,  Stocks_Prices)
    _write_sheet_for_SentiWordNet(Interim, data[1], 'Inteirm',stock_name, stock_list, interim_release, Stocks_Prices)
    workbook.save(result_path + stock_name +'_SentiWordSet_summary.xls')

def _write_sheet_for_SentiWordNet(sheet, datum, tag, stock_name, stock_list, release_dates, Stocks_Prices):
    '''
    functionality: stores the datum into the sheet
    
    input: the sheet you want to write in
           data[0] or data[1] from read_excel_for_SentiWordNet(file_path, pos_dictionary, neg_dictionary)
           tag is either 'Annual' or 'Interim'
           the name of the stock
           the list of stocks you are interested in
           the stock reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           
    return: None
    
    '''
   
    sheet.write(0,0, tag)
    category = ['positive', 'negative']
    delta_days = [1,7,30,90,180]
    col = 1
    for c in category:
        sheet.col(col).width = 256*15
        sheet.write(0, col, c)
        col += 1
    for i in range(1,6,1):
        sheet.col(col).width = 256*15
        sheet.write(0, col, 'Label_'+str(i))
        col += 1
        
    row = 1
    for year in sorted(datum):
        sheet.write(row,0,year)
        col = 1
        for c in category:
            if len(datum[year]) == 0:
                sheet.write(row, col, 0)
            else:
                sheet.write(row, col, datum[year][c])
            col += 1
        row += 1

    close_prices_current = _close_prices_after_release(stock_list, release_dates, Stocks_Prices, 0)[stock_name]
    
    for delta_day in delta_days:
        close_prices_future  =  _close_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day)[stock_name]
        row = 1
        for year in range(2002, 2017):
            close_price_c = close_prices_current[str(year)]
            close_price_f = close_prices_future[str(year)]
            if close_price_c == '#N/A' or close_price_f == '#N/A':
                sheet.write(row, col, '#N/A')
            else:
                sheet.write(row, col, Func(close_price_c, close_price_f))
            row += 1
        col += 1

def _close_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day):
    '''
    functionality: provides the close prices for all the stocks you interested in
    
    input: the list of stocks you are interested in
           the stock reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)        
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           delta_day is an int, representing how many days after the report release day
           
    return: a dict, detail in Srocks_Prices.prices(stock_list, stock_release_dates, Stocks_Prices)
    
    '''

    result = dict()
    for stock in release_dates:
        d = dict()
        for year in release_dates[stock]:
            d[year] = release_dates[stock][year] + timedelta(days = delta_day)
        result[stock] = d
    return prices(stock_list, result, Stocks_Prices)

def _open_prices_after_release(stock_list, release_dates, Stocks_Prices, delta_day):
    '''
    functionality: provides the open prices for all the stocks you interested in
    
    input: the list of stocks you are interested in
           the stock reports release information, detail in Stocks_Prices.release_dates(stock_list, file_path, flag)        
           the stocks prices, detail in Stocks_Prices.stocks_prices(conn, stock_list)
           delta_day is an int, representing how many days after the report release day
           
    return: a dict, detail in Srocks_Prices.open_prices(stock_list, stock_release_dates, Stocks_Prices)
    
    '''

    result = dict()
    for stock in release_dates:
        d = dict()
        for year in release_dates[stock]:
            d[year] = release_dates[stock][year] + timedelta(days = delta_day)
        result[stock] = d
    return open_prices(stock_list, result, Stocks_Prices)


if __name__ == '__main__':
    # Edit Area
    # ===================================================================   
    root_path = '/usr/yyy/wk5/Count/SentiWordSet/'
    result_path = '/usr/yyy/wk5/Summary/SentiWordSet/'
    release_dates_path = '/usr/yyy/wk2/reports release dates/'
    dictionary_path = '/usr/yyy/dictionaries/SentiWordNet_filtered.csv'
    # ===================================================================   
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    stock_list = [file_name[:5] for file_name in os.listdir(root_path)]
    Stocks_Prices = get_Stocks_Prices(stock_list)    
    
    annual_release = release_dates(stock_list, release_dates_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, release_dates_path + 'interim.xlsx', 'interim')
    
    pos_dictionary, neg_dictionary = read_dictionary_for_SentiWordNet(dictionary_path)
    
    for file_name in os.listdir(root_path):
        data = read_excel_for_SentiWordNet(root_path + file_name, pos_dictionary, neg_dictionary)
        
        save_into_excel_for_SentiWordNet(file_name[:5], result_path, data, stock_list, annual_release, interim_release, Stocks_Prices)
        
        print file_name[:5] + ' completed\n'

    print '---------------Done------------------'




# In[ ]:




