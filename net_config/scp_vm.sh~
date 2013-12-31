VM=$2 #mininet, n01, n02 ...

if [ $1 = 'fvm' ]
then
	scp -r mininet@$VM:~/mininet/mininet_rel .
elif [ $1 = 'tvm' ]
then
	scp -r mininet_rel mininet@$VM:~/mininet
else
	echo "Argument did not match !"
fi
