#!/bin/bash
echo $1 $2
if [ $1 = 'run' ]
then
	sudo -u flowvisor flowvisor

elif [ $1 = 'run-d' ]
then 
	sudo -u flowvisor flowvisor -d DEBUG -l
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
	fvctl -f fvpasswd_file add-slice --password=1  allslice tcp:192.168.56.1:9011 mfa
	#fvctl -f fvpasswd_file add-slice myslice2 tcp:192.168.56.1:8002 mfa
	fvctl -f fvpasswd_file add-slice --password=1 cnt1slice tcp:192.168.56.1:9001 mfa
	fvctl -f fvpasswd_file add-slice --password=1 arpslice tcp:192.168.56.1:9010 mfa
	#fvctl-xml --passwd-file=fvpasswd_file --url=https://localhost:8081 createSlice cnt1slice tcp:192.168.56.1:9001 mfa
elif [ $1 = 'rs' ]
then
	fvctl -f fvpasswd_file remove-slice allslice
	#fvctl -f fvpasswd_file remove-slice myslice2
	fvctl -f fvpasswd_file remove-slice cnt1slice
	fvctl -f fvpasswd_file remove-slice arpslice
elif [ $1 = 'af' ]
then
	fvctl -f fvpasswd_file add-flowspace allflowspace all 1 any allslice=6 #,myslice2=0
	#fvctl -f fvpasswd_file add-flowspace myflowspace2 all 10 tp_dst=1000 myslice2=6 #,myslice2=0
	#fvctl -f fvpasswd_file add-flowspace cnt1flowspace all 20 any cnt1slice=6 #,myslice2=0
	fvctl -f fvpasswd_file add-flowspace cnt1flowspace all 10 tp_dst=5000 cnt1slice=7 #,myslice2=0

	fvctl -f fvpasswd_file add-flowspace arpflowspace all 3 dl_type=0x806 arpslice=7 #,myslice2=0
	
	#fvctl-xml --url=https://localhost:8081 addFlowSpace cnt1flowspace all 10 tp_dst=5000  Slice:cnt1slice=7
 	#fvctl-xml --url=https://localhost:8081 --passwd-file=fvpasswd_file addFlowSpace all 11 tp_dst=5000 Slice:cnt1slice=7
	#fvctl -f fvpasswd_file add-flowspace myflowspace2 00:00:00:00:00:02 3 any myslice2=7 #nw_dst=10.0.0.255/32 myslice2=7
	#fvctl -f fvpasswd_file add-flowspace myflowspace2 00:00:00:00:00:01 3 tp_src=4000  myslice2=7
	#fvctl -f fvpasswd_file add-flowspace myflowspace2 00:00:00:00:00:03 3 any myslice2=7 #nw_dst=10.0.0.255/32 myslice2=7
	#fvctl -f fvpasswd_file add-flowspace myflowspace2 00:00:00:00:00:01 3 any myslice2=7 #nw_dst=10.0.0.255/32 myslice2=7
	#fvctl -f fvpasswd_file add-flowspace myflowspace2 00:00:00:00:00:02 3 tp_src=4000 myslice2=7
else
	echo "Argument did not match !"
fi
