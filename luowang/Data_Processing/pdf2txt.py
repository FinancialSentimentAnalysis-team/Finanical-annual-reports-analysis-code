# -*- coding: utf-8 -*-  
 
from pdfminer.pdfparser import PDFParser    ### ´ÓÒ»¸öÎÄ¼þÖÐ»ñÈ¡Êý¾Ý
from pdfminer.pdfdocument import PDFDocument    ### ±£´æ»ñÈ¡µÄÊý¾Ý£¬ºÍPDFParser ÊÇ»¥Ïà¹ØÁªµÄ
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter   ### ´¦ÀíÒ³ÃæÄÚÈÝ
#from pdfminer.pdfdevice import PDFDevice
#from pdfminer.layout import *
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import TextConverter
import os

def pdfTotxt1(pdf_path, txt_path):
    '''
    function: get the text according to the structure of pdf page
    pdf_path: the source pdf path 
    txt_path: the target txt file path
    '''
    
    ### check whether the source pdf file is exist ##########
    if not os.path.exists(pdf_path):
        return
     
    ### check whether the target txt path is exist ##########
    if not os.path.exists(txt_path):
        os.path.mkdir(txt_path)
        
    
   
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)  
    document = PDFDocument(parser)
    if not document.is_extractable:     ### check whether the pdf is protected and not be allowed to extract 
        raise PDFTextExtractionNotAllowed
    else:
        
        rsrcmgr=PDFResourceManager()
        laparams=LAParams()
        # device=PDFDevice(rsrcmgr)
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout=device.get_result()
            for x in layout:
                #print type(x)
                if(isinstance(x, LTTextBoxHorizontal)):
                    #content += x.get_text().encode('utf-8')+'\n'
                    with open(txt_path,'a') as f:
                        f.write(x.get_text().encode('utf-8')+'\n')
                    f.close()
        print ('create %s successully' % pdf_path)
    fp.close()
    return
    #return content
        
    

def pdfTotxt2(pdf_path, txt_path) :
    '''
    function: it is a violent method to translate pdf into txt when the pdf file is not allowed to be extracted
    pdf_path: the source pdf path 
    txt_path: the target txt file path
    '''
  
    ### check whether the source pdf file is exist ##########
    if not os.path.exists(pdf_path):
        return
     
    ### check whether the target txt path is exist ##########
    if not os.path.exists(txt_path):
        os.path.mkdir(txt_path)
      
    content =''
    try:
        outfile = txt_path
        args =[pdf_path]

        debug = 0
        pagenos = set()
        password = ''
        maxpages = 0
        rotation = 0
        codec = 'utf-8'   

        caching = True
        imagewriter = None
        laparams = LAParams()
        #
        PDFResourceManager.debug = debug
        PDFPageInterpreter.debug = debug

        rsrcmgr = PDFResourceManager(caching=caching)
        outfp = file(outfile,'a')
       
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams, imagewriter=imagewriter)
        for fname in args:
            fp = file(fname,'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            
            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=False) :
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
            fp.close()
        device.close()
        outfp.close()
        print 'create successful:', pdf_path
    except Exception:
        print 'Error!!!:', pdf_path
        return

if __name__=='__main__':
    pdf_path='/home/luowang/financial_reports_data/attach/00001/2002/Annual/Report of the Chairman and the Managing Director.pdf'
    txt_path='/home/a.txt'
    pdfTotxt(pdf_path, txt_path)
