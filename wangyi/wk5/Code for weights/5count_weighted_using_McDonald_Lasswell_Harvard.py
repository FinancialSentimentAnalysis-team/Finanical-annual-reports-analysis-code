
# coding: utf-8

# In[ ]:


from Count import *

if __name__ == '__main__':
    # Edit Area
    # ===================================================================   
    root_path = '/usr/yyy/wk5/excel_weighted/'
    result_path = '/usr/yyy/wk5/Count_Weighted/'
    Harvard_dictionary = '/usr/yyy/dictionaries/Harvard IV-4 converted/'    
    Lasswell_dictionary = '/usr/yyy/dictionaries/Lasswell dictionary converted/'
    McDonald_dictionary = '/usr/yyy/dictionaries/McDonald sentiment dictionary/'
    # ===================================================================  
    
    dictionaries = [('Harvard', Harvard_dictionary), ('Lasswell', Lasswell_dictionary), ('McDonald', McDonald_dictionary)]

    if not os.path.exists(result_path):
        os.mkdir(result_path)

    for dictionary_name, dictionary_path in dictionaries:
        result_path_for_this_dictionary = result_path + dictionary_name + '/'
        
        if not os.path.exists(result_path_for_this_dictionary):
            os.mkdir(result_path_for_this_dictionary)
            
        dictionary = read_dictionary(dictionary_path)   

        for file_name in os.listdir(root_path):
            sheet_annual, sheet_interim = read_excel(root_path + file_name)
            result_file_path = result_path_for_this_dictionary + file_name[:5] + '_' + dictionary_name + '_weighted_count.xls'
            save_into_excel(file_name[:5], dictionary, sheet_annual, sheet_interim, result_file_path)
            print file_name[:5] + ' saved successfully.'
            
        print 'Dictionary ' + dictionary_name + ' Done\n\n\n'

    print '-----------Done------------'


# In[ ]:




