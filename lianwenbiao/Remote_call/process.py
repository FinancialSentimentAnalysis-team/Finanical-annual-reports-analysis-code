# -*- coding:utf-8 -*-

import os
import commands
import collections
import sys
import threading


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
    print str(i) + ' -- has finished'

def get_dir_size(path):
    size_info = commands.getstatusoutput('du -s ' + path)
    return int(size_info[1].split('\t')[0])

def dist_subfile(target_path, machine_num):
    t = get_dir_size(target_path)

    r_file_list = []
    f_list = []
    for f_item in os.listdir(target_path): # 获取目标目录的下一层子文件(夹)
        f_list.append( ( f_item, get_dir_size(target_path + '/' + f_item.replace(' ', '\ ')) ) ) 
    f_list = sorted(f_list, key=lambda tup:tup[1], reverse=1)  # 按文件大小排列


    Q = collections.deque()
    for f in f_list:
        Q.append(f)

    # 对于每个机器，其处理的子文件为 f_l，该子文件大小之和为 f_l_s
    # 分配的算法为 1) 将文件由大到小排列  2) 尽可能塞大文件到f_l  3) 尽可能塞小文件到f_l
    # 每次对一台机器分配后，都重新评估chunk_size，即  余下文件大小/余下机器数
    for i in range(machine_num-1):
        f_l_s = 0
        f_l = []
        chunk_size = t / (machine_num - i)

        for j in range(len(Q)):
            if ( (f_l_s + Q[0][-1] - chunk_size) < (chunk_size - f_l_s) ) or len(f_l) == 0:
                f_l_s += Q[0][-1]
                f_l.append(Q[0][0])
                Q.popleft()
            else:
                break
        for j in range(len(Q)):
            if ( (f_l_s + Q[-1][-1] - chunk_size) < (chunk_size - f_l_s) ):
                f_l_s += Q[-1][-1]
                f_l.append(Q[-1][0])
                Q.pop()
            else:
                r_file_list.append(f_l)
                t -= f_l_s
                break

    f_l_s = 0
    f_l = []
    for i in range(len(Q)):
        f_l_s += Q[i][-1]
        f_l.append(Q[i][0])
    r_file_list.append(f_l)

    return r_file_list

if __name__ == '__main__':
    machine_N = 9
    dist_f_list = dist_subfile(sys.argv[2], machine_N)
    # cmd = '"' + sys.argv[1][:-1] + ' ' + sys.argv[2] + '\\r' + '"'
    for i in range(machine_N):
        if len(dist_f_list[i]) == 0:
            continue
        cmd = '"' + sys.argv[1]
        for j in range(len(dist_f_list[i])):
            cmd = cmd[:] + ' ' + sys.argv[2] + '/' + dist_f_list[i][j]
        cmd = cmd[:] + '\\r' + '"'

        # print i, cmd
        
        if len(sys.argv) > 3:
            path_from = sys.argv[3]
            path_tmp  = sys.argv[4]
            path_to   = sys.argv[5]
            new_thread = threading.Thread(target=single_machine, args=(i, cmd, path_from, path_tmp, path_to, ))
        else:
            new_thread = threading.Thread(target=single_machine, args=(i, cmd, ))
        new_thread.start()
