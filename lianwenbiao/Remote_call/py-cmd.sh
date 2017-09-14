#!/usr/bin

machine_list=(
'111.12.12.11'
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
