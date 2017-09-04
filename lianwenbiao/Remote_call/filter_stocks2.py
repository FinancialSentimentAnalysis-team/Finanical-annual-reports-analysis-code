import os

root_path = '/home/luowang/data/financial reports/result_merge/filter_files/'
stock_list_file = './282_stock_list.txt'
result_path = '/home/lijunjie/lw/data/282_filter_files/'

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



files = os.listdir(root_path)
files = sorted(files)


stocks = set()
for f in files:
    if f[:5] in stock_list:
        stocks.add(f[:5])
        cp_cmd = 'cp ' + root_path.replace(' ', '\ ') + f.replace(' ', '\ ') + ' ' + result_path
        os.system(cp_cmd)

print len(stocks)

