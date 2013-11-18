#!/bin/bash
echo $1 $2
if [ $1 = 'run' ]
then
	sudo -u flowvisor flowvisor

elif [ $1 = 'run-d' ]
then 
	sudo -u flowvisor flowvisor -d DEBUG
elif [ $1 = 'run-l' ]
then
	sudo -u flowvisor flowvisor -l
elif [ $1 = 'ls' ]
then
	fvctl -f fvpasswd_file list-slices
elif [ $1 = 'ld' ] #to learn the "dpids" of the openflow sws connected 
then
	fvctl -f fvpasswd_file list-datapaths
elif [ $1 = 'ldi' ] #to print the datapath infos for "the specific case i am working on"
then
#Note: dpid s are assigned by FV according to the numbers assigned in Mininet to the sws
	fvctl -f fvpasswd_file list-datapath-info 00:00:00:00:00:00:00:0b #dpid s -> 8-byte
elif [ $1 = 'lf' ]
then
	#fvctl -f fvpasswd_file list-flowspace myflowspace1
	#fvctl -f fvpasswd_file list-flowspace myflowspace2
	fvctl -f fvpasswd_file list-flowspace cnt1flowspace
elif [ $1 = 'rf' ]
then
	if [ $2 = '1' ]
	then
		fvctl -f fvpasswd_file remove-flowspace myflowspace1
	elif [ $2 = '2' ]
	then
		fvctl -f fvpasswd_file remove-flowspace myflowspace2
	else
		echo "naahhh"
	fi
elif [ $1 = 'rfa' ]
then
	fvctl -f fvpasswd_file remove-flowspace myflowspace1
	#fvctl -f fvpasswd_file remove-flowspace myflowspace2
	#fvctl -f fvpasswd_file remove-flowspace myflowspace1
	
elif [ $1 = 'as' ] #to add the slices "sliced" by different controllers
then
	#fvctl -f fvpasswd_file add-slice --password=1  allslice tcp:192.168.56.1:9011 mfa
	fvctl -f fvpasswd_file add-slice --password=1 acterslice tcp:192.168.56.1:9001 mfa
	fvctl -f fvpasswd_file add-slice --password=1 scherslice tcp:192.168.56.1:9010 mfa
	fvctl -f fvpasswd_file add-slice --password=1 arpslice tcp:192.168.56.1:9111 mfa
elif [ $1 = 'rs' ]
then
	#fvctl -f fvpasswd_file remove-slice allslice
	fvctl -f fvpasswd_file remove-slice acterslice
	fvctl -f fvpasswd_file remove-slice scherslice
	fvctl -f fvpasswd_file remove-slice arpslice
elif [ $1 = 'af' ]
then
	#fvctl -f fvpasswd_file add-flowspace allflowspace all 1 any allslice=6 #,myslice2=0
	fvctl -f fvpasswd_file add-flowspace acterflowspace all 10 any acterslice=7 #,myslice2=0, tp_dst=6000
	fvctl -f fvpasswd_file add-flowspace scherflowspace all 10 tp_dst=7000 scherslice=7 #,myslice2=0
	fvctl -f fvpasswd_file add-flowspace arpflowspace all 100 dl_type=0x806 arpslice=7 #,myslice2=0
else
	echo "Argument did not match !"
fi
