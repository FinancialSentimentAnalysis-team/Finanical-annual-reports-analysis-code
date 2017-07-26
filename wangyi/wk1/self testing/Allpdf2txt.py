
# coding: utf-8

# In[1]:


from pdf2txt import pdfTotxt1, pdfTotxt2    # Two convertion functions, 1 is normal convertion, 2 is brutal convertion
import xlrd
import os
from nltk.corpus import PlaintextCorpusReader   
from nltk.book import FreqDist
import threading

                # list of str of stock number
                # root directory for stocks
                # destination directory for storing converted .txt files
def handleStock(stock_dir, dir, root_txt_path):
    for stock in stock_dir:
        years_dir=os.listdir(dir + stock)
        for y in years_dir:
            type_dir=os.listdir(dir + stock + '/' + y)
            
            for t in type_dir:
                report_dir = os.listdir(dir + stock + '/' + y + '/' + t)
                root_txt = root_txt_path + stock + '_' + y + '_' + t + '_Chairman Statement.txt'
                if os.path.exists(root_txt):
                    continue
                for r in report_dir:
                    try:
                        pdfTotxt1(dir+stock+'/'+y+'/'+t+'/'+r, root_txt)
                    except:
                        pdfTotxt2(dir+stock+'/'+y+'/'+t+'/'+r, root_txt)

if __name__=='__main__':
    root_pdf_path='/home/luowang/financial_reports_data/attach/'
    root_txt_path = '/usr/yyy/self testing/txt_file/'
    stock_list = ['00590','00316','01171']

    if not os.path.exists(root_txt_path):
        os.mkdir(root_txt_path)

    handleStock(stock_list, root_pdf_path, root_txt_path)
    
    print "----------------------DONE----------------------"


# In[ ]:





# In[ ]:




