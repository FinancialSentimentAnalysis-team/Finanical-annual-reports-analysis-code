from pdf2txt import pdfTotxt1, pdfTotxt2
import os


def AllPdftoTxt(stock_dir, dir, root_txt_path):
    '''
    function: translate all pdf file to txt file in stock_dir directory
    stock_dir:the stock number list
    dir: the root directory of all reports
    root_txt_path: the target directory where the result txt file will be saved
    '''
    
    for stock in stock_dir:
        years_dir=os.listdir(dir+stock)
        for y in years_dir:
            type_dir=os.listdir(dir+stock+'/'+y)
            for t in type_dir:
                report_dir=os.listdir(dir+stock+'/'+y+'/'+t)
                if os.path.exists(root_txt):
                    continue
                for r in report_dir:
                    pdf_path=dir+stock+'/'+y+'/'+t+'/'+r
                    txt_path=root_txt_path+stock+'/'+y+'/'+t+'/'+r+'.txt'
                    try:
                        pdfTotxt1(pdf_path, txt_path)
                    except:
                        pdfTotxt2(pdf_path, txt_path)
                        
def MergeFile(root_txt_dir, target_txt_path):
    '''
    function: merge all txt file into one file in root_txt_dir directory
    root_txt_dir: the source directory where save many txt files
    target_txt_path: the target txt file path which will save all txt file
    '''
    
    file_list=os.listdir(root_txt_dir)
    with open(target_txt_path,'a') as f:
        for t in file_list:
            with open(root_txt_dir+t, 'r') as f1:
                content=f1.read()
                f.write(content.strip()+'\n')
            f1.close()
    f.close()

if __name__=='__main__':
    
    root_txt_path='/home/luowang/data/financial reports/demo_68_txt/'
    if not os.path.exists(root_txt_path):
        os.mkdir(root_txt_path)
    
    root_pdf_path='/home/luowang/data/financial reports/demo_68_test/'
    
    #### translate pdf file into txt file 
    if os.path.exists(root_pdf_path):
        stock_dir=os.listdir(root_pdf_path)
        AllPdftoTxt(stock_dir, root_pdf_path, root_txt_path)
    
    ### merge all txt files into one file 
    target_txt_dir='/home/luowang/data/financial reports/demo_68_txt/txt/'
    if not os.path.exists(target_txt_dir):
        os.mkdir(target_txt_dir)
        
    for stock in os.listdir(root_txt_path):
        for year in os.listdir(root_txt_path+stock):
            for type in os.listdir(root_txt_path+stock+'/'+y):
                temp_root_dir=root_txt_path+stock+'/'+y+'/'+type
                target_txt_path=target_txt_dir+stock+'_'+year+'_'+type+'_chairman_statement.txt'
                MergeFile(temp_root_dir, target_txt_path)
        
