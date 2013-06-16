#!/bin/bash
echo $1
if [ $1 = 'cli' ]
then
	echo "Aha"
elif [ $1 = 'sch2' ]
then
	./pox.py openflow.of_01 --port=8002 my_controller #misc.arp_responder --10.0.0.255=11:00:00:00:00:01 --10.0.0.254=11:00:00:00:00:02
elif [ $1 = 'cnt1' ]
then
	./pox.py openflow.of_01 --port=9001 controller1 --initial_install=True --no_flood=False  #misc.arp_responder #--10.0.0.255=11:00:00:00:00:01
elif [ $1 = 'sch' ]
then
	./pox.py openflow.of_01 --port=9010 sch_controller
elif [ $1 = 'span' ]
then
	./pox.py openflow.of_01 --port=9011 openflow.discovery openflow.spanning_tree --no-flood --hold-down
else
	echo "Argument did not match !"
fi
