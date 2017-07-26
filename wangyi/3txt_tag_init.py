
# coding: utf-8

# In[ ]:





# In[1]:


import re
import os

if __name__ == '__main__':
   
    root_path=    r'/usr/yyy/wk5/txt_tagged/'
    result_path = r'/usr/yyy/wk5/txt_tagged_init/'
    
    if not os.path.exists(result_path):
        os.mkdir(result_path) 
        
    file_list=os.listdir(root_path)
    
    for f in file_list:
        reader=open(root_path+f, 'rU')
        content=reader.read()
        word_tag_pair=re.findall('([A-Za-z]+)_([BCDEFGHIJMNOPRSTUVWXYZ$]+)_([A-Za-z@]+)', content)
        reader.close()
        
        des = open(result_path + f, 'wb')
        for w in word_tag_pair:
            des.write(w[2] + ' ')
        des.close()
        print f +' successfully.'

    print '-----------------Done-----------------'


# In[ ]:




