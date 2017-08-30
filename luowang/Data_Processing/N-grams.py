# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:58:04 2017

@author: Administrator
"""
import os
#import re
import csv
import nltk
import string
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader
from nltk.collocations import TrigramCollocationFinder
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import QuadgramCollocationFinder

def load_corpus(corpus_root):
    """
    function: load our corpus
    corpus_root: the root path of our corpus
    """
    corpus_reader=PlaintextCorpusReader(corpus_root, '.*')
    file_list=corpus_reader.fileids()
    return corpus_reader, file_list

def filter_punctuation(finder):
    """
    function: filter all  Collocations which contains punctuation
    finder: the object of N-Collocations
    """
    finder.apply_word_filter(lambda w: len(w)==1 or w in string.punctuation)
    return finder

def filter_digit(finder):
    """
    function: filter all  Collocations which contains digit
    finder:the object of N-Collocations
    """
    finder.apply_word_filter(lambda w: len(w)==1 or w in string.digits)
    return finder

def filter_Preposition(finder):
    """
    function: filter all  Collocations which contains Preposition
    finder:the object of N-Collocations
    """
    Prep_list=['at', 'of', 'for', 'in', 'on', 'with',  'out','to', 'from', 'after', 'behind', 'before', 'ago']
    finder.apply_word_filter(lambda w: len(w)==1 or w in Prep_list)
    return finder

def filter_BeVerb(finder):
    """
    function: filter all  Collocations which contains BeVerb
    finder:the object of N-Collocations
    """
    Bev_list=['am', 'is', 'are', 'be', 'been', 'was', 'were']
    finder.apply_word_filter(lambda w: len(w)==1 or w in Bev_list)
    return finder

def filter_Article(finder):
    """
    function: filter all  Collocations which contains Article
    finder:the object of N-Collocations
    """
    Art_list=['the', 'a', 'an']
    finder.apply_word_filter(lambda w: len(w)==1 or w in Art_list)
    return finder

def filter_Pronoun(finder):
    """
    function: filter all  Collocations which contains Pronoun
    finder:the object of N-Collocations
    """
    Pron_list=['I', 'i', 'my', 'myself', 'you', 'your', 'yours', 'yourselves', 'he', 'she', 'him', 'her', 'his', 'himself', 'herself', 'them', 'they', 'their', 'themselves']
    finder.apply_word_filter(lambda w: len(w)==1 or w in Pron_list)
    return finder

def filter_stop_words(data):
    """
    function: filter all  Collocations which consist of stop words or same words
    finder:the object of N-Collocations
    """
    stopword=stopwords.words('english')
    flag=1
    
    ### filter eg:cid cid cid 
    if len(set(data)) == 1: 
        flag=0
        
    ### filter eg: you are (a)
    if len([e for e in data if e not in stopword]) ==0:
        flag=0
        
    return flag
    
def Bigrams_freq(tokens):
    """
    function: count bigrams' frequency
    tokens: the target word list
    """
    finder = BigramCollocationFinder.from_words(tokens)
    finder=filter_punctuation(finder)
    finder=filter_digit(finder)
    finder=filter_Preposition(finder)
    finder=filter_BeVerb(finder)
    finder=filter_Article(finder)
    finder=filter_Pronoun(finder)
    Bi_collocations=sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    for e in Bi_collocations:
            Bi_dict[e[0]] +=e[1]
    return Bi_dict

def Trigrams_freq(tokens):
    """
    function: count trigrams' frequency
    tokens: the target word list
    """
    finder = TrigramCollocationFinder.from_words(tokens)
    finder=filter_punctuation(finder)
    finder=filter_digit(finder)
    finder=filter_Preposition(finder)
    finder=filter_BeVerb(finder)
    finder=filter_Pronoun(finder)
    Tri_collocations=sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    for e in Tri_collocations:
            Tri_dict[e[0]] +=e[1]
    return Tri_dict

def N_grams_freq(tokens, n):
    """
    function: count ngrams' frequency
    tokens: the target word list
    """
    finder = QuadgramCollocationFinder.from_words(tokens, window_size=n)
    finder=filter_punctuation(finder)
    finder=filter_digit(finder)
    finder=filter_Preposition(finder)
    finder=filter_BeVerb(finder)
    n_collocations=sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    for e in n_collocations:
            n_dict[e[0]] +=e[1]
    return n_dict

def save_into_csv(data, result_path):
    """
    function: save the data (bigrams-frequency , trigrams-frequency or n-grams-frequency) into a csv
    data: the target data
    result_path: the result csv path
    """
    
    print 'start to handld %s' % result_path
    with open( result_path, 'wb') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(['collocations', 'frequency'])
        for key, value in data.items():
            if filter_stop_words(key):
                writer.writerow(['_'.join(key), value])
    f.close()
    print 'create %s successfully' % result_path
       
def save_data(tokens, n, result_path):
    """
    function: get n-grams and their frequency and save them into csv according  to different n
    tokens: word list
    n: point the n-grams, when n=2, it is bigrams; when n=3, it is trigrams...
    result_path: the result csv path
    """
    
    if n=2:
        collocations_dict=Bigrams_freq(tokens)
        save_into_csv(collocations, result_path)
    elif n=3:
        collocations_dict=Trigrams_freq(tokens)
        save_into_csv(collocations, result_path)
    elif n>3:
        collocations_dict=N_grams_freq(tokens, n)
        save_into_csv(collocations, result_path)

def main(corpus_root, result_path_bi_root, result_path_tri_root):
    """
    function: the main code procedure
    corpus_root: the corpus root path
    result_path_bi_root: the bigrams result csv path
    result_path_tri_root: the trigrams result csv path
    """
    
    corpus_reader, file_list=load_corpus(corpus_root)
    
    if not os.path.exists(result_path_bi_root):
        os.mkdir(result_path_bi)
        
    if not os.path.exists(result_path_tri_root):
        os.mkdir(result_path_tri)
        
    file_list=os.listdir(corpus_root)
   
    for f in file_list:
        tokens=corpus_reader.words(f)
        save_data(tokens, 2, result_path_bi_root+f+'.csv')
        save_data(tokens, 3, result_path_tri_root+f+'.csv')
        
      
if __name__ == '__main__':
    corpus_root='D:/my project/financial annual reports/demo/result/simple_reports/00316/'
    result_path_bi_root='D:/my project/financial annual reports/demo/result/excel/'
    result_path_tri_root='D:/my project/financial annual reports/demo/result/excel/'
    main(corpus_root, result_path_bi_root, result_path_tri_root)



