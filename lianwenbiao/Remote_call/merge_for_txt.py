import os
import math

user_name = 'root'
ip_addr = '172.31.238.165'
pwd = 'gust'


def get_data_to_tmp(path_from, path_tmp, i):
    path_tmp_i = path_tmp + 'tmp' + str(i) + '/'
    if not os.path.exists(path_tmp_i.replace('\\', '')):
        os.mkdir(path_tmp_i.replace('\\', ''))    

    remote_cmd = '"python /home/lijunjie/post_data.py ' + path_from + ' ' + path_tmp_i.replace(' ', '\\\ ') + ' ' + user_name + ' ' + ip_addr + ' ' + pwd + '"'
    os.system('bash get_data.sh ' + path_from + ' ' + path_tmp + ' ' + str(i) + ' ' + remote_cmd)
    print str(i) + ' -- has finished'

def merge_in_local(path_tmp, path_to):
    path_tmp_i = path_tmp + 'tmp' + str(i) + '/tmp_txt/'
    # files = os.listdir(path_tmp_i.replace('\ ', ' '))

    '''    
    chunk_num = 1
    file_num_in_chunk = len(files)
    while file_num_in_chunk > 1500:
        chunk_num = chunk_num * 2
        file_num_in_chunk = int(math.ceil(file_num_in_chunk/2)) 

      
    
    file_num_in_res_path = 0
    res_path = path_to + suffix + '/'
    if os.path.exists(res_path):
        os.mkdir(res_path)

    for chunk_i in range(chunk_num):
        cmd = 'cp -r '
        for chunk_j in range(chunk_i * file_num_in_chunk, (chunk_i+1) * file_num_in_chunk):
            cmd = cmd + path_tmp_i + files[chunk_j].replace(' ', '\ ') + ' '
        
        cmd = cmd + path_to
        os.system('cp ' + path_tmp + 'tmp' + str(i) + '/* ' + path_to) 
    '''

    os.system('cp -r ' + path_tmp_i + '*_Annual_* ' + path_to + 'Annual/')
    os.system('cp -r ' + path_tmp_i + '*_Interim_* ' + path_to + 'Interim/')

    print str(i) + ' merge -- has finished'


if __name__ == '__main__':
    machine_N = 8

    path_from = '/home/lijunjie/lw/data/tmp_txt/'
    path_tmp = '/home/luowang/data/financial\ reports/Remote_call/Remote_call/tmp/'
    path_to = '/home/luowang/data/financial\ reports/Remote_call/Remote_call/result/'


    file_num_in_res_path = 0
    res_folder_No = 0
   
    if not os.path.exists(path_to.replace('\\', '') + 'Annual/'):
        os.mkdir(path_to.replace('\\', '') + 'Annual/')
    if not os.path.exists(path_to.replace('\\', '') + 'Interim/'):
        os.mkdir(path_to.replace('\\', '') + 'Interim/')


    for i in range(machine_N):
        # get_data_to_tmp(path_from, path_tmp, i) 
     
        path_tmp_i = path_tmp + 'tmp' + str(i) + '/tmp_txt/'
        files = os.listdir(path_tmp_i.replace('\ ', ' '))
       
        ''' 
        if file_num_in_res_path + len(files) > 10000:
            print i, file_num_in_res_path, len(files)
            res_folder_No += 1
            res_path = path_to + suffix + str(res_folder_No) + '/'
            file_num_in_res_path = 0
            if not os.path.exists(res_path.replace('\\', '')):
                os.mkdir(res_path.replace('\\', ''))
        file_num_in_res_path += len(files)
        '''

        merge_in_local(path_tmp, path_to)
