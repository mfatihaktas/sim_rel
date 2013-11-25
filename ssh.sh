if [ $1 = 's' ]
then
	ssh -X mfa51@spring.rutgers.edu
elif [ $1 = 'lsvm' ]
then
        VBoxManage showvminfo  mininet-2
else
        echo "Argument did not match !"
fi
