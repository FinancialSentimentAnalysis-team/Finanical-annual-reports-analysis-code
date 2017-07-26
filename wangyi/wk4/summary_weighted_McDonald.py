
# coding: utf-8

# In[1]:


from Summary import *

if __name__ == '__main__':
    root_path = '/usr/yyy/wk4/Count_Weighted_McDonald/'
    result_path = '/usr/yyy/wk4/Summary_Weighted_McDonald/'
    release_dates_path = '/usr/yyy/wk2/reports release dates/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    stock_list = [file_name[:5] for file_name in os.listdir(root_path)]
    Stocks_Prices = get_Stocks_Prices(stock_list)

    annual_release = release_dates(stock_list, release_dates_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, release_dates_path + 'interim.xlsx', 'interim')
    
    Function = Label(0.005)
    
    for file_name in os.listdir(root_path):
        root_file_path = root_path + file_name
        result_file_path = result_path + file_name[:5] +'_McDonald_weighted_summary.xls'
        
        save_into_excel(file_name[:5], root_file_path, result_file_path, stock_list, annual_release, interim_release, Stocks_Prices, Function)
        print file_name[:5] + ' completed \n' 

    print '---------------Done-----------------'


# In[ ]:




