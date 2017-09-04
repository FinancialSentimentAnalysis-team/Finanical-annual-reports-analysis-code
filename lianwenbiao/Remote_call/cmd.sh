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


read cmd
cmd='"'$cmd'\r''"'
echo $cmd

for((i=0;i<8;i++))
do
    /usr/bin/expect << EOF

    spawn ssh lijunjie@${machine_list[i]}

    expect "password: "
    send "123456\r"
    expect "$ " { send $cmd }
    expect "$ "
    send "exit\r"
EOF
done
