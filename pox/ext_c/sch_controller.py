from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
import time
from pox.openflow.of_json import *

import os, sys, inspect, SocketServer, threading, json

log = core.getLogger()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    data = self.request.recv(1024) #in xml format
    cur_thread = threading.current_thread()
    #response = "{}: {}".format(cur_thread.name, data)
    response = "OK"
    self.request.sendall(response)
    Controller1.pass_rxed_cmd_from_sch(data)
    
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
class SchController (object):
  def __init__ (self):
    #core.addListeners(self) < bu aptal neden calismiyo anlamadim >
    core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", self._handle_FlowStatsReceived)
    core.openflow.addListenerByName("PacketIn", self._handle_PacketIn	)
    
  def _handle_PacketIn (self, event):
    packet = event.parsed
    ip_packet = packet.find('ipv4')
    if ip_packet is None:
      print "packet", packet," isn't IP!"
      return
    print "Rxed packet: ", packet, "from sw_dpid: ", dpidToStr(event.connection.dpid)
    print "Src IP:%s, Dst IP: %s" %(ip_packet.srcip, ip_packet.dstip)
    
    payload = (ip_packet.payload).payload
    print "payload: ", payload
    sch_req_dict = json.loads(payload)
    #change from unicode str to STR
    data_amount = sch_req_dict['data_amount'].encode('ascii','ignore')
    slack_metric = sch_req_dict['slack_metric'].encode('ascii','ignore')
    func_list = sch_req_dict['slack_metric']
    for func in func_list:
      func_list[func] = func_list[func].encode('ascii','ignore')
    print 'data_amount: {}, slack_metric: {}, func_list: {}'.format(data_amount,slack_metric,func_list)
    
  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection)
		    
  def _handle_FlowStatsReceived (self, event):
    stats = flow_stats_to_list(event.stats)
    print "FlowStatsReceived from ",dpidToStr(event.connection.dpid), ": ",stats
  
  def send_stat_req(self, event):
    print "ofp_stats_request is sent to ", dpid_to_str(event.connection.dpid)
    event.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
  
def launch ():
  core.registerNew(SchController)
  
