echo $1

N02_IP=10.0.0.102
N01_IP=10.0.0.101
SW=s2
GRE_PORT=3

if [ $1  = 'init' ]; then
  sudo mn --custom ~/mininet/custom/topo-2sw-2host.py --topo mytopo
elif [ $1 = 'dp' ]; then
  sudo ovs-ofctl dump-ports-desc $SW
elif [ $1 = 'af' ]; then
  #flow btw n01-n02
  sudo ovs-ofctl add-flow $SW "in_port=$GRE_PORT ip idle_timeout=0 actions=output:1"
  sudo ovs-ofctl add-flow $SW "in_port=1 ip idle_timeout=0 actions=output:$GRE_PORT"

  #sudo ovs-ofctl add-flow $SW "in_port=$GRE_PORT ip idle_timeout=0 actions=output:2"
  #sudo ovs-ofctl add-flow $SW "in_port=2 ip idle_timeout=0 actions=output:$GRE_PORT"
  #flow btw n01 hosts
  #sudo ovs-ofctl add-flow $SW "in_port=1 ip idle_timeout=0 actions=output:2"
  #sudo ovs-ofctl add-flow $SW "in_port=2 ip idle_timeout=0 actions=output:1"
elif [ $1  = 'df' ]
then
  sudo ovs-ofctl dump-flows $SW
elif [ $1  = 'rf' ]
then
  sudo ovs-ofctl del-flows $SW "ip"
elif [ $1  = 'ct' ]
then
  sudo ovs-ofctl del-flows $SW
elif [ $1 = 'show' ]; then
  sudo ovs-vsctl show
elif [ $1  = 'gre' ]; then
  sudo ovs-vsctl add-port s2 s2-gre1 -- set interface s2-gre1 type=gre options:remote_ip=$N01_IP
else
  echo "Argument did not match !"
fi

