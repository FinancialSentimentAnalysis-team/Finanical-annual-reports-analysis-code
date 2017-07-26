
# coding: utf-8

# In[24]:


import re
import os
import threading

def main(txt_list):
    result_root = '/usr/yyy/self testing/txt_filted/'
    file_root =   '/usr/yyy/self testing/txt_file/'
    for e_txt in txt_list:
        try:        
            f=open(file_root+e_txt, 'rU')
            content=f.read()
            f.close()          
            
            content=re.sub(r'[^A-Za-z]', ' ', content)
            content=re.sub(r'\s{2,}', ' ', content)
            content=content.strip().lower()
            
            f1=open(result_root + e_txt, 'wb')            
            f1.write(content)
            f1.close()           
        except Exception as e:
            print e
            print 'handle file: %s error!' % e_txt

if __name__=='__main__':
    result_path = '/usr/yyy/self testing/txt_filted/'
    file_path=  '/usr/yyy/self testing/txt_file/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    txt_list=os.listdir(file_path)
    
    main(txt_list)
    
    print '---------------------------Done---------------------------'
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


# In[ ]:




