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

cmd='"'$1'"'


/usr/bin/expect << EOF

spawn ssh lijunjie@${machine_list[$2]}

set timeout -1

expect "password: "
send "123456\r"

expect "lijunjie" { send "su\r" }
expect "Password:" { send "gust\r" }

expect "root" { send $cmd }
expect "DONE"
send "exit\r"
EOF
