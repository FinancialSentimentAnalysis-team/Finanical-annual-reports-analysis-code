
# coding: utf-8

# In[1]:


import os
import threading
import nltk
from nltk.book import FreqDist
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader
from nltk.stem import WordNetLemmatizer

def load_corpus(corpus_root):
    corpus_reader=PlaintextCorpusReader(corpus_root, '.*')
    file_list=corpus_reader.fileids()
    return corpus_reader, file_list

def get_stem(voc):
    res=[]
    porter=nltk.PorterStemmer()
    for t in voc:
        try:
            res.append(porter.stem(t))
        except Exception:
            print '+++++++++++++++++++'
            print t
    #res=[porter.stem(t) for t in voc]
    return res

def get_ini(voc):
    res=[]
    wn_lem=WordNetLemmatizer()
    for t in voc:
        try:
            res.append(wn_lem.lemmatize(t))
        except Exception:
            print 'Error:+++++++++'
            print t
    print 'haha==============='
    return res

def filter_stopwords(voc):
    stop_w=stopwords.words('english')
    res=[]
    for t in voc:
        try:
            if t.lower() not in stop_w and len(t)>2:
                res.append(t)
            
        except Exception:
            print '=================='
            print t
    #res=[t for t in voc if t not in stop_w]
    return res

def count_words_freq(reader, f):
    word_list=reader.words(f)
    #temp1=get_stem(word_list)
    temp1=get_ini(word_list)
    temp3=filter_stopwords(temp1)
    word_tuple=FreqDist(temp3)
    return word_tuple

def save_wordfreq(word_tuple, filename):
    if os.path.exists(filename):
        os.remove(filename)
    try:
        obj=open(filename, 'a')
        for word, freq in word_tuple.items():
            str='%-40s%-6d\r\n'%(word.encode('utf8'), freq)
            #print str
            #break
            obj.write(str)
        obj.close()
        print 'save %s successfully!' % filename
    except Exception as e:
        print e
        print'Error: save word frequency fail! %s' % filename

def main(file_list, corpus_reader, result_path):    
    for f in file_list:
        ### save words freq
        word_tuple=count_words_freq(corpus_reader, f)
        
        ### save into anthoer txt
        filename=result_path + f
        save_wordfreq(word_tuple, filename)

if __name__=='__main__':
    # Edit Area
    # ===================================================================   
    root_path =   r'/usr/yyy/wk5/txt_tagged_init/'
    result_path = r'/usr/yyy/wk5/txt_freq/'
    # ===================================================================   
    
    if not os.path.exists(result_path):
        os.mkdir(result_path)
        
    corpus_reader, file_list = load_corpus(root_path)
    
    main(file_list, corpus_reader, result_path)
    
    print '------------------Done---------------------'

    


# In[ ]:




