if [ $1 = 'fvm' ]
then
	scp -r mininet@mininet:~/mininet/mininet_rel . 
elif [ $1 = 'tvm' ]
then
	scp -r mininet_rel mininet@mininet:~/mininet
elif [ $1 = 'tvmo' ]
then
	scp -r mininet_rel openflow@openflow:~/mininet
else
	echo "Argument did not match !"
fi