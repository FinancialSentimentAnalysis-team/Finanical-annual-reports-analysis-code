
# coding: utf-8

# In[22]:


import os
import csv


def convert_dictionary(file_path):
    count = 1
    s = set()
    for line in open(file_path):
        if count > 16:
            word = line.split()
            if len(word) == 1:
                if '#' in word[0]:
                    s.add(word[0].split('#')[0])
                else:
                    s.add(word[0])
        count += 1
    return sorted(list(s))
    
    
    
    

def save_info_csv(result_path, file_path):
    word_list = convert_dictionary(file_path)
    category = file_path.split('/')[-1][:-4]

    out = open(result_path + category + '.csv', 'w')

    csv_writer = csv.writer(out)
    
    for word in word_list:
        csv_writer.writerow([word])







if __name__ == '__main__':
    root_path = '/usr/yyy/dictionaries/Harvard IV-4/'
    result_path = '/usr/yyy/dictionaries/Harvard IV-4 converted/'
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    for file_name in os.listdir(root_path):
        
        save_info_csv(result_path, root_path + file_name)


    print '-----------------Done-----------------'









# In[ ]:




