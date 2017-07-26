
# coding: utf-8

# In[1]:


import re
import os
import threading

def main(file_root, result_root):
    for e_txt in os.listdir(file_root):
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
    # the file_path should contain txt files
    file_path   = r'/usr/yyy/wk5/demo_68_txt/'
    result_path = r'/usr/yyy/wk5/txt_filtered/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    main(file_path, result_path)
    
    print '---------------------------Done---------------------------'
    
    

    
    
    
    


# In[ ]:




