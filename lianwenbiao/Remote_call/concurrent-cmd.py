# -*- coding:utf-8 -*-

import os
import sys
import threading


def single_machine(i, cmd, path_from=None, path_tmp=None, path_to=None):
    os.system('bash ./py-cmd.sh ' + cmd + ' ' + str(i))
    print str(i) + ' -- has finished   '


if __name__ == '__main__':
    machine_N = 8
    cmd = raw_input()
    cmd = '"' + cmd + '\\r' + '"'

    for i in range(machine_N):
        print i, cmd
        
        new_thread = threading.Thread(target=single_machine, args=(i, cmd, ))
        new_thread.start()

    while 1:
        if threading.activeCount() <= 1:
            break
        time.sleep(1)
    
    print "All Done"
