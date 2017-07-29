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


path_from=$1
path_to=$2
echo $3

    # expect "(yes/no)?"
    # { send "yes\r" }

for((i=0;i<8;i++))
do
    /usr/bin/expect << EOF

    set timeout -1

    spawn scp -r "$path_from"  lijunjie@${machine_list[i]}:"$path_to"


    expect "password"
    send "123456\r"

    expect "$3"
    send "exit\r"
EOF
done
