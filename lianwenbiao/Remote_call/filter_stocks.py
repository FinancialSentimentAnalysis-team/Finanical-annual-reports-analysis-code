import os

root_path = '/home/luowang/data/financial reports/result_merge/tmp_txt/'
stock_list_file = './282_stock_list.txt'
result_path = '/home/lijunjie/lw/data/282_tmp_txt/'

if not os.path.exists(result_path):
    os.mkdir(result_path)


fp = open(stock_list_file, 'rb')
txt_str = fp.read()


stock_list = []
lines = txt_str.split(' HK Equity\n')

for i in range(len(lines)):
    if len(lines[i]) > 1:
        stock_no_txt = lines[i]
        for l in range(5 - len(stock_no_txt)):
            stock_no_txt = '0' + stock_no_txt

        stock_no = stock_no_txt
        stock_list.append(stock_no)

fp.close()



files1 = os.listdir(root_path + 'Annual/')
files1 = sorted(files1)


stocks1 = set()
for f in files1:
    if f[:5] in stock_list:
        stocks1.add(f[:5])
        cp_cmd = 'cp ' + root_path.replace(' ', '\ ') + 'Annual/' + f.replace(' ', '\ ') + ' ' + result_path
        os.system(cp_cmd)

print len(stocks1)


files2 = os.listdir(root_path + 'Interim/')
files2 = sorted(files2)

stocks2 = set()
for f in files2:
    if f[:5] in stock_list:
        stocks2.add(f[:5])
        cp_cmd = 'cp ' + root_path.replace(' ', '\ ') + 'Interim/' + f.replace(' ', '\ ') + ' ' + result_path
        os.system(cp_cmd)

print len(stocks2)


print 'DONE'
