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

from pox.openflow.of_json import *

log = core.getLogger()

class MyScheduler (object):
  def __init__ (self, connection):
    self.connection = connection

    # My table
    self.macToPort = {}

    # We want to hear PacketIn messages, so we listen to the connection
    connection.addListeners(self)
    print "stat message is sent to sw_dpid: ", dpid_to_str(self.connection.dpid)
    self.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
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
    packet = event.parsed
    print "Rxed packet: ", packet
    
class my_controller (object):
  """
  Waits for OpenFlow switches to connect and Does ...
  """
  def __init__ (self):
    print 'my_controller is initiated successfully'
    core.openflow.addListeners(self)

  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection,)
    MyScheduler(event.connection)

def _timer_func ():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    connection.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
  log.debug("Sent %i flow/port stats request(s)", len(core.openflow._connections))

def _handle_flowstats_received (event):
  stats = flow_stats_to_list(event.stats)
  print "FlowStatsReceived from ",dpidToStr(event.connection.dpid), ": ",stats
  
def launch ():
  core.registerNew(my_controller)
  #############STATS#################
  from pox.lib.recoco import Timer
  core.openflow.addListenerByName("FlowStatsReceived", _handle_flowstats_received)
  #core.openflow.addListenerByName("PortStatsReceived", _handle_portstats_received) 
    
  # timer set to execute every five seconds
  Timer(5, _timer_func, recurring=True)
