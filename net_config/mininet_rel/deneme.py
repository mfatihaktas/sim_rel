#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel, info, error
from mininet.net import Mininet
from mininet.link import Intf
from mininet.topolib import TreeTopo
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.util import quietRun

class SimpleTopo( Topo ):
    def __init__( self ):
        "Create custom topo."
        Topo.__init__( self )
        # Add hosts and switches
        p = self.addHost( 'p' )
        c = self.addHost( 'c' )

        s1 = self.addSwitch( 's1' )
	
	 #link opts
        local_linkopts = dict(bw=10, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
        # Add links
        self.addLink( p,s1, **local_linkopts )
        self.addLink( s1,c, **local_linkopts )

if __name__ == '__main__':
    setLogLevel( 'info' )

    info( '*** Creating network\n' )
    net = Mininet( topo=SimpleTopo(), link=TCLink, controller=RemoteController)
    cont=net.addController('r0', controller=RemoteController, ip='192.168.56.1',port=7000)
    cont.start()
    #c0 = Controller( 'c0' )
    #c0.stop()
    c0 = net.getNodeByName('c0')
    p, c = net.getNodeByName('p', 'c')
    
    p.setIP(ip='10.0.0.2', prefixLen=32)
    c.setIP(ip='10.0.0.1', prefixLen=32)
    
    p.setMAC(mac='00:00:00:01:00:02')
    c.setMAC(mac='00:00:00:01:00:01')
    
    p.setDefaultRoute(intf='p-eth0')
    c.setDefaultRoute(intf='c-eth0')
    
    #arp thing
    p.setARP(ip='10.0.0.1', mac='00:00:00:01:00:01')
    c.setARP(ip='10.0.0.2', mac='00:00:00:01:00:02')

    net.start()
    CLI( net )
    net.stop()
