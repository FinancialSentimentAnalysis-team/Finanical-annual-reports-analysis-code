#!/usr/bin

machine_list=(
'172.31.238.127'
'172.31.238.128'
'172.31.238.130'
'172.31.238.131'
'172.31.238.133'
'172.31.238.134'
'172.31.238.135'
'172.31.238.136'
)


for((i=0;i<8;i++))
do
    /usr/bin/expect << EOF


    spawn ssh lijunjie@${machine_list[i]}

    expect "password: "
    send "123456\r"
    expect "$ " { send "su\r" }
    expect "Password:" { send "gust\r" }
    expect "root" { send "python /home/lijunjie/lw/code/a.py\r" }
    expect "Downloader" { send "d\r" }
    expect "Identifier" { send "book\r" }
    expect "Downloader" { send "d\r" }
    expect "Identifier" { send "all-corpora\r" } 
    expect "Downloader" { send "q\r" }
    expect "root"
    send "exit\r"
EOF
done
