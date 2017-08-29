# -*- coding: utf-8 -*-

import os
import re


def _is_invalid_line(line_txt):
    """
    function:check the current sentence is invalid
    line_txt:the line content which is in string format
    """
    ##1. The blank line
    if line_txt == '':
        return True

    tmp = re.sub(r"[^A-Za-z0-9]", '', line_txt)
    
    #2. if the length of a sentence except only contain digit, punctuation or special character is lower than 3, it should be a invalid sentence
    if tmp.isdigit() or len(tmp) <= 3:
        return True

    #3. handle like (cid:180)
    if re.search("(cid\d*)+", tmp):
        return True
        
    # what out: all blank spaces have been replaced
    ## 4. H K 2 0 1 4
    if re.search("HK\d+", tmp) and len(line_txt.split()) == 1:
        return True
        
    ## 5. Million Million Million ... or Hong Kong Hong Kong ... 
    if len(set(tmp.split()))<3:
        return True

    return False


def _is_title(line_txt):
    """
    function: check whether the current line is title or directory
    line_txt: the target line content in string format
    """
    
    conj_words = ['or', 'and', 'at', 'in', 'by', 'with', 'of']
    
    # initial the variable
    words = line_txt.split()
    is_title = True

    # all words' Capital letter of a title except conj should be capitalized 
    for word in words:
        if word not in conj_words and not word[0].isupper():
            is_title = False

    return is_title


def deal_with_sentence(line_txt):
    """
    function: deal with single line 
    line_txt: the target line in string format
    """
    ## check whether the line is valid
    if _is_invalid_line(line_txt):
        return
        
    ## filter all special characters
    ## leave alpha, digit, '.' and ','
    ## but '?)"'may be a line end sign ?
    line_content = re.sub(r"[^A-Za-z0-9,.’]", ' ', line_txt) \
        .decode("utf-8", 'ignore').strip()

    # check whether the line is a title
    if _is_title(line_content):
        line_content += '\n'
    else:
        # check whether the line is a complete sentence
        if line_content[-1] == '.':
            line_content += '\n'
        
        else:   # if the line is not a compete sentence, it should be a part of behine content, so add a blank space
            line_content += ' '
    return line_content


def _filter_invalid_title(txt_f):
    """
    function: delete all invalid title, and leave the final title if there are serval same titles
    txt_f: the target txt content's object
    """
    ## initial the variable
    result_content = ""
    last_title = ""

    while True:
        line = txt_f.readline()
        if _is_invalid_line(line):
            continue
        elif _is_title(line):
            last_title = "\n"+line + "\n"
        else:
            result_content += last_title
            result_content += line
            last_title = ''
    return result_content


def split_chunk(txt_path, txt_name):
    """
    function: split the txt contnet into many chuncks
    txt_path: the target txt path
    txt_name: the target txt name
    """
    
    result_content = ''  ## the final result content
    chunk_content = ''

    with open(txt_path + "/" + txt_name + ".txt", "rb") as txt_f:
        while True:
            line = txt_f.readline()
            
            if _is_invalid_line(line.strip()): ## if the sentence is invalid, it is a end sign of chunk, and the chunk should be writen in result content 
                if chunk_content != '':
                    result_content += chunk_content
                    
                    result_content += '\n'  ### use '\n' to separate chunks 
                    chunk_content = ''   ## start a new chunk
                
            else:   ### add the sentence into the chunk if it is valid
                line = deal_with_sentence(line)
                chunk_content += line

    paths = "/".join(txt_path.split('/')[:5]) + "/filter_files/" \
            + "/".join(txt_path.split('/')[-2:])
    if not os.path.exists(paths):
        os.makedirs(paths)

    with open(paths + "/" + txt_name + "_back.txt", "w") as txt_f:
        txt_f.write(result_content.encode("utf-8"))

    ### filter invalid titles
    with open(paths + "/" + txt_name + "_back.txt", "r") as txt_f:
        result_content = _filter_invalid_title(txt_f)

    if os.path.exists(paths + "/" + txt_name + "_back2.txt"):
        os.remove(paths + "/" + txt_name + "_back2.txt")

    with open(paths + "/" + txt_name + "_back.txt", "w") as txt_f:
        txt_f.write(result_content)


def process(stock_no, period):
    """
    function: the main process procedure
    stock_no: the number of a stock
    period: 'Annual' or 'Interim'
    """
    txt_path = "F:/xunlei/CharlesYee/financial_reports" \
               "/" + stock_no + "/txt_files/"

    year_list = os.listdir(txt_path)

    for year in year_list:
        # cannot accumulation
        # txt_path = txt_path + year + "/" + period
        txt_path_in = txt_path + year + "/" + period

        # deal with 'Annual' or 'Interim' file absent
        if not os.path.exists(txt_path_in):
            continue

        file_list = os.listdir(txt_path_in)
        for txt_name in file_list:
            txt_name = txt_name.replace(".txt", "")
            split_chunk(txt_path_in, txt_name)


if __name__ == '__main__':
    # process("00590", "Annual")
    process("00590", "Interim")

    process("00001", "Annual")
    process("00001", "Interim")
    print "finished!"
