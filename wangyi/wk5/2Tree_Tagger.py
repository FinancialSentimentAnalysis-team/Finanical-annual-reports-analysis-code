
# coding: utf-8

# In[1]:


import os
import treetaggerwrapper

if __name__ == '__main__':
    root_path   = r'/usr/yyy/wk5/txt_filtered/'
    result_path = r'/usr/yyy/wk5/txt_tagged/'

    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    tagger = treetaggerwrapper.TreeTagger(TAGDIR = '/usr/yyy/')

    for file_name in os.listdir(root_path):
        
        root_file_path = root_path + file_name

        result_file_path = result_path + file_name[:-4] + '.TAGGED.txt'
        
        result_file = open(result_file_path, 'w')
        
        txt_list = ' '.join(['_'.join(i.split('\t')) for i in tagger.tag_file(root_file_path)])
        
        result_file.write(txt_list)
        
        result_file.close()
        print file_name + ' tagged successfully.'

    print '-----------Done------------'



# In[ ]:




