#!/bin/bash

MFADEV="lo"
MFADIR="/home/mehmet/Dropbox/sim_rel/net_config/mininet_rel/host_rel/tc_rel/htb_rel/lo_"
#

MINDEV="p-eth0"
MINDIR="/home/mininet/mininet/mininet_rel/host_rel/tc_rel/htb_rel"

if [ $2  = 'p' ]; then
  DIR=$MINDIR
  DEV=$MINDEV
  OPT="not_add_root"
  echo "confing p"
else
  DIR=$MFADIR
  DEV=$MFADEV
  OPT="add_root"
  echo "confing mfa"
fi

if [ $1  = 'conf' ]; then
    sudo ./htb.init.sh start invalidate $DEV $DIR $OPT
elif [ $1  = 'dconf' ]; then
    #sudo tc filter del dev $DEV parent 1: protocol ip prio 100 u32
    #sudo tc class del dev $DEV parent 1:2 classid 1:10
    #sudo tc class del dev $DEV parent 1:2 classid 1:20
    #sudo tc class del dev $DEV parent 1: classid 1:2
    
    sudo tc qdisc del dev $DEV root
elif [ $1  = 'show' ]; then
  #sudo ./htb.init.sh stats
  
  echo "> qdiscs:"
  tc -s -p qdisc show dev $DEV
  echo "> classes:"
  tc -s -p class show dev $DEV
  echo "> filters:"
  tc -s -p filter show dev $DEV
elif [ $1  = 'root' ]; then
  sudo ./htb.init.sh start invalidate $DEV $DIR $OPT
  sudo ./htb.init.sh minstop ... $DEV $DIR
  #sudo tc class del dev $DEV parent 1:1 classid 1:2
else
  echo "1st arg did not match !"
fi
