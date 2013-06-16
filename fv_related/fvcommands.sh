#!/bin/bash
echo $1 $2
if [ $1 = 'run' ]
then
	sudo -u mehmet flowvisor

elif [ $1 = 'run-d' ]
then 
	sudo -u flowvisor flowvisor -d DEBUG -l
elif [ $1 = 'ls' ]
then
	./fvctl.py -f fvpasswd_file list-slices
elif [ $1 = 'ld' ] #to learn the "dpids" of the openflow sws connected 
then
	./fvctl.py -f fvpasswd_file list-datapaths
elif [ $1 = 'ldi' ] #to print the datapath infos for "the specific case i am working on"
then
#Note: dpid s are assigned by FV according to the numbers assigned in Mininet to the sws
	./fvctl.py -f fvpasswd_file list-datapath-info 00:00:00:00:00:00:00:0c #dpid s -> 8-byte
elif [ $1 = 'lf' ]
then
	#./fvctl.py -f fvpasswd_file list-flowspace myflowspace1
	#./fvctl.py -f fvpasswd_file list-flowspace myflowspace2
	./fvctl.py -f fvpasswd_file list-flowspace cnt1flowspace
elif [ $1 = 'rf' ]
then
	if [ $2 = '1' ]
	then
		./fvctl.py -f fvpasswd_file remove-flowspace myflowspace1
	elif [ $2 = '2' ]
	then
		./fvctl.py -f fvpasswd_file remove-flowspace myflowspace2
	else
		echo "naahhh"
	fi
elif [ $1 = 'rfa' ]
then
	./fvctl.py -f fvpasswd_file remove-flowspace myflowspace1
	#./fvctl.py -f fvpasswd_file remove-flowspace myflowspace2
	#./fvctl.py -f fvpasswd_file remove-flowspace myflowspace1
	
elif [ $1 = 'as' ] #to add the slices "sliced" by different controllers
then
	./fvctl.py -f fvpasswd_file add-slice --password=1  allslice tcp:192.168.56.1:9011 mfa
	./fvctl.py -f fvpasswd_file add-slice --password=1 cnt1slice tcp:192.168.56.1:9001 mfa
	./fvctl.py -f fvpasswd_file add-slice --password=1 sch_cntslice tcp:192.168.56.1:9010 mfa
	#./fvctl.py -f fvpasswd_file add-slice --password=1 arpslice tcp:192.168.56.1:9010 mfa
elif [ $1 = 'rs' ]
then
	./fvctl.py -f fvpasswd_file remove-slice allslice
	./fvctl.py -f fvpasswd_file remove-slice cnt1slice
	./fvctl.py -f fvpasswd_file remove-slice sch_cntslice
	#./fvctl.py -f fvpasswd_file remove-slice arpslice
elif [ $1 = 'af' ]
then
	./fvctl.py -f fvpasswd_file add-flowspace allflowspace all 1 any allslice=6 #,myslice2=0
	./fvctl.py -f fvpasswd_file add-flowspace cnt1flowspace all 10 tp_dst=5000 cnt1slice=7 #,myslice2=0
	./fvctl.py -f fvpasswd_file add-flowspace sch_cntflowspace all 10 tp_dst=6000 sch_cntslice=7 #,myslice2=0
	#./fvctl.py -f fvpasswd_file add-flowspace arpflowspace all 3 dl_type=0x806 arpslice=7 #,myslice2=0
else
	echo "Argument did not match !"
fi
