if [ $1 = 'svm' ]
then
	VBoxManage modifyvm mininet-2 --vrde on
        VBoxManage startvm "mininet-2" --type headless
elif [ $1 = 'lsvm' ]
then
        VBoxManage showvminfo  mininet-2
elif [ $1 = 'cvm' ]
then
        VBoxManage controlvm mininet-2 poweroff
elif [ $1 = 'srdp' ]
then
	rdesktop -a 16 -N 127.0.0.1:3389
else
        echo "Argument did not match !"
fi

