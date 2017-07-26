
# coding: utf-8

# In[1]:


from Plotting_Stock_Price import *

# Delete the num amount of data
def alter_data(data, num):
    for i in range(len(data)):
        detected = sorted(data[i][1].items(), key = lambda tuple_a: tuple_a[1], reverse = True)[:num]
        for word, freq in detected:
            data[i][1][word] = 0


if __name__ == "__main__":
    print '--------------Start Connecting-----------'
    conn = connect('172.31.238.166', 3306, 'root', 'root', 'stock')
    stock_list = ['00316','00590','01171']
    Stocks_Prices = stocks_prices(conn, stock_list)
    conn.close()
    file_path = '/usr/yyy/wk2/reports release dates/'
    annual_release = release_dates(stock_list, file_path + 'annual.xlsx','annual')
    interim_release = release_dates(stock_list, file_path + 'interim.xlsx', 'interim')
    annual_prices =  prices(stock_list, annual_release,  Stocks_Prices)
    interim_prices = prices(stock_list, interim_release, Stocks_Prices)

    root_path = "/usr/yyy/self testing/excel_freq/"
    result_path = "/usr/yyy/wk2/excel_summary_with_price_reweighted/"
    dictionary_path = "/usr/yyy/self testing/Dictionary.xlsx"
    delete_range = range(3,8)
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    pos_words, neg_words = read_dictionary(dictionary_path)
    for file_name in os.listdir(root_path):
        for num in delete_range:
            file_path = root_path + file_name
            sheet_annual, sheet_interim = read_excel(file_path)
            annual_pos,  annual_neg  = analyze_sheet(pos_words, neg_words, sheet_annual)
            interim_pos, interim_neg = analyze_sheet(pos_words, neg_words, sheet_interim)
            alter_data(annual_pos, num)
            alter_data(annual_neg, num)
            alter_data(interim_pos, num)
            alter_data(interim_neg, num)
            
            workbook = xlsxwriter.Workbook(result_path + '/' + file_name[:5] + '_delete_' + str(num) + '_summary.xlsx')
            
            save_into_excel(workbook, file_name[:5], annual_pos, annual_neg, interim_pos, interim_neg, annual_prices, interim_prices)
            
            print file_name[:5] +'_delete_' + str(num) + ' saved successfully.'

    print '------------------Done----------------'


# In[ ]:




