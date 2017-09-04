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
  
    set timeout 5

    expect "password: "
    send "123456\r"
    expect "$ " { send "su\r" }
    expect "Password:" { send "gust\r" }
    expect "root" { send "pip uninstall sklearn\r" }
    expect "Proceed" { send "Y\r" }
    expect "$ "  
    send "exit\r"
EOF
done
