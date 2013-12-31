#!/bin/bash

echo $1

VMKEYDIR=./keys/mfa51-key
VMUSRNAME=ubuntu
VMIP=149.165.159.16
VMSCPDIR=~/Dropbox/sim_rel/net_config/mininet_rel/host_rel/net_2p_stwithsingleitr.py

SNAPKEYDIR=./keys/mininet-key
VMSNAP_NAMES=( snap_controller snap_mininet1 snap_mininet2 )
VMSNAP_USRNAMES=( ubuntu ubuntu ubuntu )
VMSNAP_PUBIPS=( 149.165.159.17 149.165.159.18 149.165.159.19 )

FGRELDIR=~/Dropbox/sim_rel/fg_rel

SCPDIRS=( fg_controller fg_mininet1 fg_mininet2 )

if [ $1  = 'ssh' ]; then
  ssh mfa51@india.futuregrid.org
elif [ $1  = 'tr' ]; then
  scp -r misc mfa51@india.futuregrid.org:~/
  #scp -r $MINRELDIR mfa51@india.futuregrid.org:~/misc
elif [ $1  = 'fr' ]; then
  scp -r mfa51@india.futuregrid.org:~/misc .
elif [ $1  = 'scpkeys' ]; then
  scp mfa51@india.futuregrid.org:~/.ssh/mininet* ./keys
  scp mfa51@india.futuregrid.org:~/.ssh/mfa* ./keys
elif [ $1  = 'sshvm' ]; then
  ssh -l $VMUSRNAME -i $VMKEYDIR $VMIP
elif [ $1  = 'tvm' ]; then
  scp -r $VMSCPDIR -i $VMKEYDIR $VMUSRNAME@$VMIP:~/
#######################################################
elif [ $1  = 'sshsnap' ]; then
  ssh -X -l ${VMSNAP_USRNAMES[$2]} -i $SNAPKEYDIR ${VMSNAP_PUBIPS[$2]}
elif [ $1  = 'tsnap' ]; then
  #scp -v -r $FGRELDIR -i $SNAPKEYDIR ${VMSNAP_USRNAMES[$2]}@${VMSNAP_PUBIPS[$2]}:~/
  SCPDIR=${SCPDIRS[$2]}
  if [ $2 = 0 ]; then
    tar czf - $FGRELDIR/$SCPDIR | ssh -v -l ${VMSNAP_USRNAMES[$2]} -i $SNAPKEYDIR ${VMSNAP_PUBIPS[$2]} "tar xzf -; cp -r ~/$FGRELDIR/$SCPDIR ~/; rm -r ~/home; cp ~/$SCPDIR/pox_rel/* ~/pox/ext"
  else
    tar czf - $FGRELDIR/$SCPDIR | ssh -v -l ${VMSNAP_USRNAMES[$2]} -i $SNAPKEYDIR ${VMSNAP_PUBIPS[$2]} "tar xzf -; cp -r ~/$FGRELDIR/$SCPDIR/mininet_rel ~/mininet; rm -r ~/home"
  fi
elif [ $1  = 'scpinstalldirs' ]; then
  #only for snap_controller
  BASEDIR=~/Dropbox/sim_rel
  INSTALLDIRS=( networkx cvxopt )
  for DIR in "${INSTALLDIRS[@]}"; do
    tar czf - $BASEDIR/$DIR | ssh -v -l ${VMSNAP_USRNAMES[$2]} -i $SNAPKEYDIR ${VMSNAP_PUBIPS[$2]} "tar xzf -; cp -r ~/$BASEDIR/$DIR ~/; rm -r ~/home; cp ~/$DIR/pox_rel/* ~/pox/ext"
  done
else
	echo "Argument did not match !"
fi
