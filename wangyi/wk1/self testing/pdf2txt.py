
# coding: utf-8

# In[5]:



 
from pdfminer.pdfparser import PDFParser 
from pdfminer.pdfdocument import PDFDocument 
from pdfminer.pdfpage import PDFTextExtractionNotAllowed, PDFPage
from pdfminer.pdfinterp import PDFResourceManager,  PDFPageInterpreter
from pdfminer.layout import LTTextBoxHorizontal,  LAParams
from pdfminer.converter import TextConverter, PDFPageAggregator
import os

def pdfTotxt1(pdf_path, txt_path):
    '''
    if os.path.exists(txt_path):
        return
    '''
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
        
    else:
        rsrcmgr=PDFResourceManager()
        laparams=LAParams()
        
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout=device.get_result()
            
            for x in layout:
                if(isinstance(x, LTTextBoxHorizontal)):
                    with open(txt_path,'a') as f:
                        f.write(x.get_text().encode('utf-8')+'\n')
                    f.close()
                    
        print ('create %s successully' % pdf_path)
    fp.close()
    return

def pdfTotxt2(pdf_path, txt_path) :
    '''
    if os.path.exists(txt_path):
        return
    '''
    try:
        outfile = txt_path
        outfp = file(outfile,'a')
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
        PDFResourceManager.debug = debug
        PDFPageInterpreter.debug = debug

        rsrcmgr = PDFResourceManager(caching=caching)        
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams, imagewriter=imagewriter)
        
        for fname in args:
            fp = file(fname,'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            
            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=False):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
            fp.close()

        device.close()
        outfp.close()
        print ('create %s successfully:'% pdf_path)
    except:
        print 'Error!!!:', pdf_path
        return


if __name__=='__main__':    # used for only testing.
    pdf_path='/home/luowang/financial_reports_data/attach/00001/2002/Annual/Report of the Chairman and the Managing Director.pdf'
    txt_path='/usr/yyy/self testing/b.txt'
    pdfTotxt2(pdf_path, txt_path)    # the result is a mere raw txt file


# In[ ]:




