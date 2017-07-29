import os
import sys

path_from = sys.argv[1]
path = path_from
#'/home/luowang/financial_reports_data/attach'

if os.path.isdir(path):
    files = os.listdir(path)
    # 获取传输文件中的最后一个文件
    while os.path.isdir(path + '/' + files[-1]):
        path = path[:] + '/' + files[-1]
        files = os.listdir(path)


    print files[-1]

    # 获取最后一个文件的大小
    last_file_size = os.path.getsize(path + '/' + files[-1])
    if last_file_size > 9999: # 最后会以KB还是字节的形式显示，这里其实假定了要传输的文件不会超过 9999KB -> 9MB
        last_file_size = str(round(last_file_size / float(1024)))[:-2] + 'KB'
    else:
        last_file_size = str(last_file_size) + '  '

    print last_file_size

    # 作为终止标志的字符串，格式不用太细究
    expect_str = '{:<54}'.format(files[-1]) + '100%' + '{:>7}'.format(last_file_size)
    # expect_str = '{:<54}'.format('INTERIM REPORT 2010.pdf') + '100%' + '{:>7}'.format('288KB')

    os.system('bash post_data.sh ' + '"' + sys.argv[1] + '" "' + sys.argv[2] + '" "' + expect_str.replace(' ', '\ ') + '"') 

else:
    os.system('bash post_data.sh ' + '"' + sys.argv[1] + '" "' + sys.argv[2] + '" "100%"')

print 'finish work'
