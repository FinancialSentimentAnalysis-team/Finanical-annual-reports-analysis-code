
# coding: utf-8

# In[4]:


from Count import *

if __name__ == '__main__':
    root_path = '/usr/yyy/self testing/excel_freq/'
    result_path = '/usr/yyy/wk4/Count_Harvard/'
    dictionary_path = '/usr/yyy/dictionaries/Harvard IV-4 converted/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    dictionary = read_dictionary(dictionary_path)   

    for file_name in os.listdir(root_path):
        sheet_annual, sheet_interim = read_excel(root_path + file_name)
        result_file_path = result_path +file_name[:5]+ '_Harvard_count.xls'
        save_into_excel(file_name[:5], dictionary, sheet_annual, sheet_interim, result_file_path)

        print file_name[:5] + ' saved successfully.'
        
        
        
        break
    print '-----------Done------------'


# In[ ]:




