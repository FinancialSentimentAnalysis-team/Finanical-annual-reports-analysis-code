
# coding: utf-8

# In[1]:


from Summary import *

if __name__ == '__main__':
    root_path = '/usr/yyy/wk5/Count_Difference/'
    result_path = '/usr/yyy/wk5/Summary_Difference/'
    release_dates_path = '/usr/yyy/wk2/reports release dates/'
    dictionaries_names = ['McDonald', 'Lasswell', 'Harvard']
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    stock_list = [file_name[:5] for file_name in os.listdir(root_path + 'Harvard/')]
    Stocks_Prices = get_Stocks_Prices(stock_list)
    
    annual_release = release_dates(stock_list, release_dates_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, release_dates_path + 'interim.xlsx', 'interim')
    
    for dictionary_name in dictionaries_names:
        root_path_for_this_dictionary = root_path + dictionary_name + '/'
        result_path_for_this_dictionary = result_path + dictionary_name + '/'
        
        if not os.path.exists(result_path_for_this_dictionary):
            os.mkdir(result_path_for_this_dictionary)

        for file_name in os.listdir(root_path_for_this_dictionary):
            root_file_path = root_path_for_this_dictionary + file_name
            result_file_path = result_path_for_this_dictionary + file_name[:5] +'_' + dictionary_name + '_difference_summary.xls'        

            save_into_excel(file_name[:5], root_file_path, result_file_path, stock_list, annual_release, interim_release, Stocks_Prices)       
            print file_name[:5] + ' completed \n'
        
        print 'Summary for ' + dictionary_name + ' is completed.\n\n'

    print '----------Done--------------'


# In[ ]:




