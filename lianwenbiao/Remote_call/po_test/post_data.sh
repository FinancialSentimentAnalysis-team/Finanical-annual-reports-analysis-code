#!/usr/bin


path_from=$1
path_to=$2


/usr/bin/expect << EOF

set timeout -1

spawn scp -r "$path_from"  $4@$5:"$path_to"

expect {
  "(yes/no)?"
  { 
     send "yes\n"
     expect "*asswrod:" { send "123456\n" }
  }  
  "*assword:"
  {
     send "$6\n"
  }
}  

expect "$3"
send "exit\r"
EOF
