
# coding: utf-8

# In[3]:


import xlrd
import xlwt
import os

def read_excel(path):
    '''
    functionality: reads the file and extracts the data
    
    input: the file path in excel_freq
    
    return: a tuple of two list
            tuple[0] is for annual. It is a list of sub-lists, each sub-list is a list of words
            tuple[1] is for annual. It is a list of sub-lists, each sub-list is a list of words

    '''
    
    wbk=xlrd.open_workbook(path)
    sheet_annual=wbk.sheet_by_name('Annual')
    sheet_interim=wbk.sheet_by_name('Interim')
    
    ncols_annual=sheet_annual.ncols
    data_annual=[]
    for col in range(ncols_annual):
        data_annual.append(sheet_annual.col_values(col))
        
    ncols_interim=sheet_interim.ncols
    data_interim=[]
    for col in range(ncols_interim):
        data_interim.append(sheet_interim.col_values(col))
        
    return data_annual, data_interim

def save_into_sheet(data, year, term, wbk):
    '''
    functionality: save the data into a sheet in the workbook
    
    input: the data obtained from countDiff1(data)
           a list of years
           the term is either 'Annual' or 'Interim'
           the workbook where you want the sheet to be created
    
    return: None
            
    '''
    
    sheet=wbk.add_sheet(term)
    col=0
    for i in range(1,len(data), 2):
        row=0
        sheet.write(row, col, 'word')
        sheet.write(row, col+1, year[col/2])
        for j in range(len(data[i-1])):
            row +=1
            sheet.write(row, col, data[i-1][j])
            sheet.write(row, col+1, data[i][j])
        col +=2

def countDiff1(data):
    '''
    functionality: calculates the difference of words frequencies in two consecutive years.
    
    input: the data obtained from read_excel(path)
    
    return:  a list of sub-lists, each sub-list is a list of words or a list of numbers
             a list of years
            
    '''
    
    res_data=[]
    year=[data[i][0] for i in range(1,len(data),2) ]
    res_data.append(data[0][1:])
    res_data.append(data[1][1:])
    for i in range(2, len(data), 2):
        res_data.append(data[i][1:])
        res_data.append([0]*len(data[i][1:]))
        for j in range(1, len(data[i][1:])):
            if data[i][j] in data[i-2]:
                for h in range(len(data[i-2])):
                    if data[i-2][h]==data[i][j]:
                        if len(data[i][j]) >0 :
                            res_data[i+1][j-1]=str(int(data[i+1][j])-int(data[i-1][h]))
                        else:
                            res_data[i+1][j-1]=0
            else:
                res_data[i+1][j-1]='-'+data[i+1][j]
    return res_data, year

if __name__=='__main__':
    root_path =   '/usr/yyy/wk5/excel_freq/'
    result_path = '/usr/yyy/wk5/excel_diff/'

    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    excel_list=os.listdir(root_path)
    for excel_name in excel_list:
        #wbk=xlwt.Workbook()
        stock = excel_name[:5]
        file_name = root_path + excel_name
        data_annual, data_interim = read_excel(file_name)

        res_data, year = countDiff1(data_annual)
        #save_into_sheet(res_data, year, 'Annual', wbk)
    
        #res_data, year = countDiff1(data_interim)
        #save_into_sheet(res_data, year, 'Interim', wbk)
        
        #wbk.save(result_path + stock + '_Diff.xls')
        print stock, 'saved successfully.'

    print '-----------------Done------------------'


# In[ ]:




