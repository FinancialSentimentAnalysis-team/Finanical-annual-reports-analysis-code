from pdf2txt import pdfTotxt1, pdfTotxt2
import os
import sys


def handleStock(stock_dir, dir, root_txt_path, chunk_num, chunk_no):
    print chunk_num
    chunk_num  = int(chunk_num)
    chunk_no = int(chunk_no)


    for stock in stock_dir[chunk_num * chunk_no : chunk_num * (chunk_no+1)]:
        years_dir=os.listdir(dir+stock)
        for y in years_dir:
            type_dir=os.listdir(dir+stock+'/'+y)
            for t in type_dir:
                report_dir=os.listdir(dir+stock+'/'+y+'/'+t)
                root_txt=root_txt_path+stock+'_'+y+'_'+t+'_Chairman Statement.txt'
                if os.path.exists(root_txt):
                    continue
                for r in report_dir:
                    try:
                        pdfTotxt1(dir+stock+'/'+y+'/'+t+'/'+r, root_txt)
                    except:
                        pdfTotxt2(dir+stock+'/'+y+'/'+t+'/'+r, root_txt)

if __name__=='__main__':
    target_path= sys.argv[1]
    chunk_num  = sys.argv[2]
    machine_no = sys.argv[3]   

    root_txt_path='/home/lijunjie/lw/data/tmp_txt/'
    if not os.path.exists(root_txt_path):
        os.mkdir(root_txt_path)
    
    # root_pdf_path='/home/lijunjie/lw/data/HKEX/'
    root_pdf_path = target_path
    if os.path.exists(root_pdf_path):
        stock_dir=os.listdir(root_pdf_path)
        handleStock(stock_dir, root_pdf_path, root_txt_path, chunk_num, machine_no)

    print "DONE"
    
