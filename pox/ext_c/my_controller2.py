"""
Controller will behave as the scheduler.

1st Goal: Get the scheduling request messages 
"""
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
import time

log = core.getLogger()

class MyScheduler (object):
  def __init__ (self, connection):
    self.connection = connection

    # My table
    self.macToPort = {}

    # We want to hear PacketIn messages, so we listen to the connection
    connection.addListeners(self)
    #clear sw table
    #self.clear_sw_table()
	
	#set sw tables
    #self.set_sw_table()

  def clear_sw_table(self):
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    self.connection.send(msg)
    print "Clearing flows from %s." %(dpid_to_str(self.connection.dpid),)
    
  def set_sw_table (self):
    # One thing at a time...
    msg = of.ofp_flow_mod()
    msg.priority = 42
    msg.match.dl_type = 0x800 # Ethertype / length (e.g. 0x0800 = IPv4)
    msg.match.nw_dst = IPAddr("10.0.0.255")
    #msg.match.tp_dst = 9000
    msg.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
    self.connection.send(msg)
  
  def _handle_PacketIn (self, event):
    """
    Handle packet in messages from the switch to implement above algorithm.
    """
    packet = event.parsed
    print "Rxed packet: ", packet
    self.handle_IP_packet(packet)
    
    for con in core.openflow.connections:
      con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

  def handle_IP_packet (self, packet):
    """
    ip = packet.find('ipv4')
    if ip is None:
      print "This packet isn't IP!"
      return
    print "Source IP:", ip.srcip
    """
    udp = packet.find('udp')
    if udp is None:
      print "This packet isn't UDP!"
      return
    print "UDP is found", udp.payload
    
class my_controller2 (object):
  """
  Waits for OpenFlow switches to connect and Does ...
  """
  def __init__ (self):
    print 'my_controller is initiated successfully'
    #log.debug("my_controller is initiated successfully")
    core.openflow.addListeners(self)

  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection,)
    #log.debug("Connection %s" % (event.connection,))
    MyScheduler(event.connection)
    for con in core.openflow.connections:
      con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
      
  # When we get flow stats, print stuff out
  def _handle_FlowStatsReceived (self, event):
    i=0
    for f in event.stats:
      print "stat ", i, ": ", f.match
      i=i+1

def launch ():
  """
  Does ...
  """
  core.registerNew(my_controller2)
  
