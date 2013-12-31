#!/bin/bash

echo $1

N01IP=10.0.0.201
N02IP=10.0.0.202
CCIP=10.0.0.101

if [ $1  = 'init' ]; then
  module load novaclient
  source ~/.futuregrid/openstack_havana/novarc
elif [ $1  = 'lsf' ]; then
  nova flavor-list
elif [ $1  = 'lsi' ]; then
  nova image-list
elif [ $1  = 'bdi' ]; then
  nova boot --flavor $FLV \
            --image $VMIMG \
            --key_name $KEY $VMNAME
elif [ $1  = 'lsvm' ]; then
  nova list
elif [ $1  = 'rmvm' ]; then
  nova delete $VMNAME
elif [ $1  = 'sshtvm' ]; then
  ssh -l $VMUSERNAME -i ~/.ssh/$KEY $PIVVMIP
elif [ $1  = 'setup-extacc' ]; then
  nova floating-ip-create
  nova add-floating-ip $VMNAME $PUBVMIP
  nova floating-ip-list
else
	echo "Argument did not match !"
fi
