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
cmd=$4'\n'
echo $cmd


/usr/bin/expect << EOF

spawn ssh lijunjie@${machine_list[$3]}

expect {
  "(yes/no)?"
  { 
     send "yes\n"
     expect "*asswrod:" { send "123456\n" }
  }  
  "*assword:"
  {
     send "123456\n"
  }
}  

expect "lijunjie@"  { send "$cmd" }

expect "finish work"
send "exit\r"
EOF
