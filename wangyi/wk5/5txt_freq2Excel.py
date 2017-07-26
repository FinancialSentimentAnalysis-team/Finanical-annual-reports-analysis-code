
# coding: utf-8

# In[3]:


import os
import xlwt
import re

def classify_file(path):
    file_dict={}
    file_list=os.listdir(path)
    for f in file_list:
        temp=f.split('_')
        if temp[0] not in file_dict.keys():
            file_dict[temp[0]]={}
        if temp[1] not in file_dict[temp[0]].keys():
            file_dict[temp[0]][temp[1]]={}
        if temp[2] not in file_dict.keys():
            file_dict[temp[0]][temp[1]][temp[2]]=[]
        file_dict[temp[0]][temp[1]][temp[2]].append(f)
        
    return file_dict

def read_txt(file_name):
    data=[]
    f=open(file_name, 'r')
    lines=f.readlines()
    for line in lines:
        t = re.findall('([A-Za-z]+)\s+([0-9]+)', line)
        if t != []:
            data.append(t[0])
    return data

def save_data_into_excel(flag, sheet_name, file_data, file_name, root_path):
    col=0
    for y in sorted(file_data.keys()):
        try:
            file_path = root_path + file_data[y][flag][0]
        except:
            continue
        row=0
        sheet_name.write(row,col,'word')
        sheet_name.write(row,col + 1,y)
        data=read_txt(file_path)
        print root_path + file_data[y][flag][0]
        for e in data:
            row += 1
            sheet_name.write(row,col, e[0])
            sheet_name.write(row,col+1, e[1])
        col +=2

if __name__ == '__main__':
    root_path = '/usr/yyy/wk5/txt_freq/'
    result_path = '/usr/yyy/wk5/excel_freq/'

    if not os.path.exists(result_path):
        os.mkdir(result_path)
        
    file_dict= classify_file(root_path)
    stock_list=file_dict.keys()

    for s in stock_list:
        wbk = xlwt.Workbook()
        sheet_annual = wbk.add_sheet('Annual')
        sheet_interim = wbk.add_sheet('Interim')

        file_name = result_path + s + '_word_frequency.xls'

        save_data_into_excel('Annual', sheet_annual, file_dict[s], file_name, root_path)
        save_data_into_excel('Interim', sheet_interim, file_dict[s], file_name, root_path)

        wbk.save(file_name)

    print '-----------------Done------------------'


# In[ ]:




