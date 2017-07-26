
# coding: utf-8

# In[50]:


import csv
from collections import defaultdict

# 0: property
# 2: positive
# 3: negative
# 4: words

def read_dictionary(dictionary_path):
    d = defaultdict(list)
    csv_file = open(dictionary_path, 'r')
    reader = csv.reader(csv_file)
    for line in reader:
        if line[0] != 'POS':
            for word in line[4].split(','):
                d[word[:-2]].append((word.split('#')[0] + '#' + line[0], line[2], line[3]))
    csv_file.close()
    pos_result_dict = dict()
    neg_result_dict = dict()
    for word in d:
        dic = dict()        
        _property = set(word_info[0] for word_info in d[word])
        for word_with_property in _property:
            dic[word_with_property] = [0,0]
        for word_with_property in _property:
            count = 0
            for word_info in d[word]:
                if word_info[0] == word_with_property:
                    count += 1
                    dic[word_with_property][0] += float(word_info[1])
                    dic[word_with_property][1] += float(word_info[2])
            dic[word_with_property][0] /= count
            dic[word_with_property][1] /= count
        for key, value in dic.items():
            if value[0] != 0:
                pos_result_dict[key.strip()] = value
            if value[1] != 0:
                neg_result_dict[key.strip()] = value
    return pos_result_dict, neg_result_dict


if __name__ == '__main__':
    dictionary_path = '/usr/yyy/dictionaries/SentiWordNet_filtered.csv'
    
    dictionary = read_dictionary(dictionary_path)
    
    s = set()
    
    for word in sorted(dictionary):
        s.add(word.split('#')[1])
    print s
    
    #for word, info in sorted(dictionary.items()):
    #    print word, info

    
    print '------------Done--------------'
    
    


# In[ ]:




