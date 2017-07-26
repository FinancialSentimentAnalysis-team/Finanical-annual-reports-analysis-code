
# coding: utf-8

# In[52]:


import csv

if __name__ == '__main__':
    dictionary_path = '/usr/yyy/dictionaries/SentiWordNet.txt'
    result_path = '/usr/yyy/dictionaries/'
    csv_file = open(result_path + 'SentiWordNet_filtered.csv','w')
    writer = csv.writer(csv_file)
    for line in open(dictionary_path, 'r'):
        if len(line) > 10:
            line = line.split()
            if line[0] == '#':
                writer.writerow(line[1:])
            else:
                words = []
                if line[2] != '0' or line[3] != '0':
                    for word_index in range(len(line[4:])):
                        if '#' in line[4:][word_index]:
                            words.append(line[4:][word_index])
                        else:
                            writer.writerow(line[:4] + [','.join(words), ' '.join(line[4:][word_index:])])
                            break
    csv_file.close()
    print '------------Done---------------'










# In[ ]:




