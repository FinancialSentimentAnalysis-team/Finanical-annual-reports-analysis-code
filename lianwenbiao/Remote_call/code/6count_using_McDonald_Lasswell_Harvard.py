
# coding: utf-8

# In[ ]:


from Count import *

if __name__ == '__main__':
    # Edit Area
    # ===================================================================   
    root_path = '/usr/yyy/wk5/excel_freq/'
    result_path = '/usr/yyy/wk5/Count/'
    Harvard_dictionary = '/usr/yyy/dictionaries/Harvard IV-4 converted/'    
    Lasswell_dictionary = '/usr/yyy/dictionaries/Lasswell dictionary converted/'
    McDonald_dictionary = '/usr/yyy/dictionaries/McDonald sentiment dictionary/'
    # ===================================================================   
    
    dictionaries = [('Harvard', Harvard_dictionary), ('Lasswell', Lasswell_dictionary), ('McDonald', McDonald_dictionary)]

    if not os.path.exists(result_path):
        os.mkdir(result_path)


    result_path = result_path + 'Har_Las_McD/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
            

    dictionary1 = read_dictionary(Harvard_dictionary)   
    dictionary2 = read_dictionary(Lasswell_dictionary)
    dictionary3 = read_dictionary(McDonald_dictionary)

    for file_name in os.listdir(root_path):
        sheet_annual, sheet_interim = read_excel(root_path + file_name)
        result_file_path = result_path + file_name[:5] + '_count.xls'
        save_into_excel(file_name[:5], dictionary1, dictionary2, dictionary3, sheet_annual, sheet_interim, result_file_path)
        print file_name[:5] + ' saved successfully.'
            
    print 'Dictionary ' + dictionary_name + ' Done\n\n\n'

    print '-----------Done------------'


# In[ ]:




