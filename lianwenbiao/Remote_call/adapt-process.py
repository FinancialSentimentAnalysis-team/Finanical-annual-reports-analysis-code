# -*- coding:utf-8 -*-

import os
import commands
import collections
import sys
import threading
import math
import time


user_name = 'lw'
ip_addr = '172.31.238.166'
pwd = 'lw123'

def single_machine(i, cmd, path_from=None, path_tmp=None, path_to=None):
    os.system('bash ./py-cmd.sh ' + cmd + ' ' + str(i))
    if path_from:
        path_tmp = path_tmp + '/tmp' + str(i)
        if not os.path.exists(path_tmp):
            os.mkdir(path_tmp)
        remote_cmd = '"python /home/lijunjie/post_data.py ' + path_from + '/ ' + path_tmp + ' ' + user_name + ' ' + ip_addr + ' ' + pwd + '"'
        os.system('bash get_data.sh ' + path_from + ' ' + path_tmp + ' ' + str(i) + ' ' + remote_cmd)
        #os.system('mv ' + path_tmp + '/t2.sh ' + path_to) 
        #os.system('rm -r ' + path_tmp)
    end = time.clock()
    print str(i) + ' -- has finished   ' + str(end - start) 

def get_dir_size(path):
    size_info = commands.getstatusoutput('du -s ' + path)
    return int(size_info[1].split('\t')[0])

def dist_subfile(target_path, machine_num):
    stock_num = len(os.listdir(target_path))
    chunk_num = math.ceil(stock_num / float(machine_num))

    return chunk_num

if __name__ == '__main__':
    start = time.clock()
    machine_N = 8
    chunk_num = int(dist_subfile(sys.argv[2], machine_N))
    # cmd = '"' + sys.argv[1][:-1] + ' ' + sys.argv[2] + '\\r' + '"'

    for i in range(machine_N):
        cmd = '"' + sys.argv[1] + ' ' + str(chunk_num) + ' ' + str(i) + '\\r' + '"'
        
        if len(sys.argv) > 3:
            path_from = sys.argv[3]
            path_tmp  = sys.argv[4]
            path_to   = sys.argv[5]
            new_thread = threading.Thread(target=single_machine, args=(i, cmd, path_from, path_tmp, path_to, ))
        else:
            new_thread = threading.Thread(target=single_machine, args=(i, cmd, ))
        new_thread.start()

    while 1:
        if threading.activeCount() <= 1:
            break
        time.sleep(1)
    
    print "All Done"
