
# coding: utf-8

# In[36]:


import os
import xlwt
from collections import defaultdict

def save_to_sheet(result_path, workbook, data, flag, year_set):
    workbook.write(0,0,'Stocks')
    col = 1
    year_list = sorted(list(year_set))
    for year in year_list:
        workbook.write(0, col, year)
        col += 1
    row, col = 1, 1
    for stock in sorted(data):
        workbook.write(row, 0, stock)
        for year in year_list:
            workbook.write(row, col, data[stock][year])
            col += 1
        col = 1
        row += 1

if __name__ == '__main__':
    root_path = '/home/luowang/financial_reports_data/attach/'
    result_path = '/usr/yyy/wk2/Report Completeness/'
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    stocks_annual  = {}
    stocks_interim = {}
    year_set = set()
    
    for stock in os.listdir(root_path):
        stocks_annual[stock] = defaultdict(int)
        stocks_interim[stock] = defaultdict(int)

        for year in os.listdir(root_path + stock + '/'):
            year_set.add(year)
            
            for term in os.listdir(root_path+stock+'/'+year+'/'):
                
                for root, dirs, files in os.walk(root_path+stock+'/'+year+'/'+term+'/'):
                    if term == 'Annual' and len(files) != 0:
                        stocks_annual[stock][year] = 1
                    elif term == 'Interim' and len(files)!= 0:
                        stocks_interim[stock][year] = 1
    
    workbook = xlwt.Workbook()
    annual = workbook.add_sheet('Annual')
    interim = workbook.add_sheet("Interim")
    
    save_to_sheet(result_path, annual,  stocks_annual, "Annual",  year_set)
    save_to_sheet(result_path, interim, stocks_annual, "Interim", year_set)
    workbook.save(result_path  + 'Stocks Completeness.xls')    
    print '---------------Done--------------'


# In[ ]:




