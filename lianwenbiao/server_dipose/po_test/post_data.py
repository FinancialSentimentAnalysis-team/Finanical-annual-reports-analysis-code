import os
import sys

path_from = sys.argv[1]
path = path_from
#'/home/luowang/financial_reports_data/attach'

username = sys.argv[3]
userip   = sys.argv[4]
password = sys.argv[5]

if os.path.isdir(path):
    files = os.listdir(path)
    while os.path.isdir(path + '/' + files[-1]):
        path = path[:] + '/' + files[-1]
        files = os.listdir(path)

    print files[-1]
    last_file_size = os.path.getsize(path + '/' + files[-1])
    if last_file_size > 9999: 
        last_file_size = str(round(last_file_size / float(1024)))[:-2] + 'KB'
    else:
        last_file_size = str(last_file_size) + '  '
    print last_file_size

    expect_str = '{:<46}'.format(files[-1]) + '100%' + '{:>7}'.format(last_file_size)
    # expect_str = '{:<54}'.format('INTERIM REPORT 2010.pdf') + '100%' + '{:>7}'.format('288KB')

    os.system('bash post_data.sh ' + '"' + sys.argv[1] + '" "' + sys.argv[2] + '" "' + expect_str.replace(' ', '\ ') + '" "' + username + '" "' + userip + '" "' + password + '"') 

else:
    os.system('bash post_data.sh ' + '"' + sys.argv[1] + '" "' + sys.argv[2] + '" "100%" "' + username + '" "' + userip + '" "' + password + '"')

print 'finish work'
