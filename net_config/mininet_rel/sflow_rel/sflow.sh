#!/bin/bash
if [ $1 = 'ca' ]
then
	sudo ovs-vsctl -- \
	--id=@sflow create sFlow agent=eth1 target=\"192.168.56.1:6343\" 	header=128 sampling=64 polling=10 -- \
	-- set bridge s11 sflow=@sflow \
	-- set bridge s1 sflow=@sflow \
	-- set bridge s2 sflow=@sflow \
	-- set bridge s12 sflow=@sflow
elif [ $1 = 'ra' ]
then
	sudo ovs-vsctl -- clear Bridge s11 sflow
	sudo ovs-vsctl -- clear Bridge s1 sflow
	sudo ovs-vsctl -- clear Bridge s2 sflow
	sudo ovs-vsctl -- clear Bridge s12 sflow
elif [ $1 = 'lbr' ]
then
	sudo ovs-vsctl list br
else
	echo "Argument did not match !"
fi
