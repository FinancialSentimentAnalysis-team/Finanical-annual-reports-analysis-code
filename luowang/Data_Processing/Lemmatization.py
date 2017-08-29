# -*- coding: utf-8 -*-
from treetaggerwrapper import TreeTagger
from nltk.corpus import PlaintextCorpusReader
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.book import FreqDist

def load_corpus(c_root, file_name=None):
    """
    function: load ourself corpus
    c_root: the root path of our corpus' files
    file_name: the file name
    """
    
    c_reader = PlaintextCorpusReader(c_root, ".txt")  ### our corpus only contain txt file
    f_list = c_reader.fileids() ### get all file name list of our corpus
    return c_reader, f_list
    
def get_lem(word_list):
    """
    function: translate all words in word_list into their lemmatization
    word_list: the target word list which must be in unicode !!!
    """
    ret = []
    tagger = TreeTagger(TAGDIR=".\\tools\\tree-tagger-windows-3.2\TreeTagger")
    for word in word_list:
        # for digit, tagger will use '@card@' to identify
        if word.isdigit():
            ret.append(word)
        else:
            tags = tagger.tag_text(word.lower())
            for tag in tags:
                ret.append(tag.split()[2])
    return ret

def filter_stop_words(word_list):
    """
    function: filter all stop words according to stopword list of nltk corpus
    word_list: the target word_list
    """
    
    ret = []
    for word in word_list:
        if word.lower() not in stopwords.words('english') and len(word) > 2:   ### filter those are not in stopword list and their length less than 2
            ret.append(word)
    return ret


def count_word_freq(c_reader, f):
    """
    function: count all words frequency of f in c_reader corpus
    c_reader: the corpus object which save the taregt f file
    f: the target file
    """
    
    words = c_reader.words(f)

    # lemmatization
    tree_words = get_lem(words)
    
    # filter stop words
    filter_words = filter_stop_words(tree_words)
    
    # count word frequency
    w_freq = FreqDist(filter_words)

    return w_freq



if __name__ == '__main__':
    corpus_root = "E:\codes\pycharm\\nlp\\financial_reports_processing\week_2\\files\\"
    corpus_reader, file_list = load_corpus(corpus_root)
    for f in file_list:
        word_freq = count_word_freq(corpus_reader, f)
        
