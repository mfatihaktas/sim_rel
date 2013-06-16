"""
Controller behaving as the scheduler.

1st Goal: Fill the sw tables for resource scheduling purposes
	first simple scheduling scenario:
		t11(::03) - t13(::05) - t43(::14)
		session port: 5000
"""
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
import time
from pox.openflow.of_json import *

import os, sys, inspect, SocketServer, threading

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"ext")))
if cmd_subfolder not in sys.path:
 	sys.path.insert(0, cmd_subfolder)
 	
from ruleparser import RuleParser

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

class Controller1 (object):
  rule_parser = RuleParser("ext/scheduling.xml")
  def __init__ (self):
    self.dict_ = Controller1.rule_parser.rule_dict_for_session('1')
    self.dict_I = Controller1.rule_parser.rule_dict_for_session_I('1')
    # for listening scheduler
    self.HOST, self.PORT = '192.168.56.1', 9999 #socket.gethostbyname(socket.gethostname())
    self.server = ThreadedTCPServer((self.HOST, self.PORT), ThreadedTCPRequestHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    # Exit the server thread when the main thread terminates
    self.server_thread.daemon = True
    self.server_thread.start()
    print "To listen Scheduler, Server loop running in thread:", self.server_thread.name
     
    #core.addListeners(self) < bu aptal neden calismiyo anlamadim >
    core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", self._handle_FlowStatsReceived)
    core.openflow.addListenerByName("PacketIn", self._handle_PacketIn	)
  
  @staticmethod
  def pass_rxed_cmd_from_sch(xml_path_rule):
    Controller1.rule_parser.modify_by_cmd(xml_path_rule)
  
  def _handle_PacketIn (self, event):
    packet = event.parsed
    self.handle_data_packet(event, packet)    

  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection)
    if _install_initial_flow:
      self.install_initial_scheduling_flows(event)

    if _no_flood_by_default:
		  con = event.connection
		  print "Disabling flooding for %i ports" %(len(con.ports))
		  for p in con.ports.itervalues():
		    if p.port_no >= of.OFPP_MAX: continue
		    pm = of.ofp_port_mod(port_no=p.port_no,
		                        hw_addr=p.hw_addr,
		                        config = of.OFPPC_NO_FLOOD,
		                        mask = of.OFPPC_NO_FLOOD)
		    con.send(pm)
		    
  def _handle_FlowStatsReceived (self, event):
    stats = flow_stats_to_list(event.stats)
    print "FlowStatsReceived from ",dpidToStr(event.connection.dpid), ": ",stats
  
  def install_initial_scheduling_flows(self, event):
    dpid = str(event.connection.dpid)
    
    self.install_drop_casually(event) #this is default for every switch from the start
    try:
      hw = Controller1.rule_parser.hm_from_dpid[dpid]
    except (KeyError, RuntimeError, TypeError, NameError):
      print "\n ---> No entry in hm_from_dpid for dpid: ", dpid, "\n"
      return
      
    l_dict = None
    counter = 0
    while (counter <= hw):
      l_dict = self.dict_I[dpid, counter]
      typ = l_dict['typ']
      rule_dict = l_dict['rule_dict']
      wc_dict = l_dict['wc_dict']
      duration = [1000, 0]

      if typ == 'forward':
        self.send_ofmod_forward('conn_up', event, wc_dict['src_ip'], wc_dict['dst_ip'], int(rule_dict['fport']), duration)
        self.send_stat_req(event)
      elif typ == 'modify_forward':
        self.send_ofmod_modify_forward('conn_up', event, wc_dict['src_ip'], wc_dict['dst_ip'],
  	    rule_dict['new_dst_ip'], rule_dict['new_dst_mac'], int(rule_dict['fport']), duration)
        self.send_stat_req(event)

      counter = counter + 1

  def install_drop_casually (self, event):
    fm = of.ofp_flow_mod()
    fm.priority = 0x0001 # Pretty low
    fm.match.dl_type = ethernet.IP_TYPE#ARP_TYPE
    #fm.match.dl_dst = EthAddr("ff:ff:ff:ff:ff:ff")
    fm.idle_timeout = 1000
    fm.hard_timeout = 0
    #fm.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    event.connection.send(fm)
    print "install_drop_casually is done for ", event.connection
    #self.send_stat_req(event)
  
  def send_stat_req(self, event):
    print "ofp_stats_request is sent to ", dpid_to_str(event.connection.dpid)
    event.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    
  def clear_sw_table(self, event):
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    event.connection.send(msg)
    print "Clearing flows from %s." %(dpid_to_str(event.connection.dpid),)
    
  def handle_data_packet (self, event, packet):
    ip = packet.find('ipv4')
    if ip is None:
      print "packet", packet," isn't IP!"
      return
    print "Rxed packet: ", packet, "from sw_dpid: ", dpidToStr(event.connection.dpid)
    print "Src IP:%s, Dst IP: %s" %(ip.srcip, ip.dstip)
    try:
    	dict_ = self.dict_[(str(event.connection.dpid), ip.srcip.toStr())]
    except (KeyError, RuntimeError, TypeError, NameError):
    	print "\n ---> No rule for dpid: ", str(event.connection.dpid), "src_ip: ", ip.srcip.toStr(), "\n"
    	return
    typ = dict_['typ']
    rule_dict = dict_['rule_dict']
    wc_dict = dict_['wc_dict']
    duration = [1000, 0]
    if typ == 'forward':
    	self.send_ofmod_forward('packet_in', event, wc_dict['src_ip'], 
      wc_dict['dst_ip'], int(rule_dict['fport']), duration)
    	#self.send_stat_req(event)
    elif 	typ == 'modify_forward':
    	self.send_ofmod_modify_forward('packet_in', event, wc_dict['src_ip'], wc_dict['dst_ip'],
    	rule_dict['new_dst_ip'], rule_dict['new_dst_mac'], int(rule_dict['fport']), duration)
    	#self.send_stat_req(event)  
    
  def send_ofmod_forward (self, _called_from, event, nw_src, nw_dst, o_port, duration):
    msg = of.ofp_flow_mod()
    #msg.match = of.ofp_match.from_packet(packet)
    msg.priority = 0x7000
    #msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.UDP_PROTOCOL, nw_dst=IPAddr(nw_dst))
    msg.match.dl_type = 0x800 # Ethertype / length (e.g. 0x0800 = IPv4)
    msg.match.nw_src = IPAddr(nw_src)
    msg.match.nw_dst = IPAddr(nw_dst)
    msg.match.nw_proto = 17 #UDP
    msg.match.tp_dst = 5000
    msg.idle_timeout = duration[0]
    msg.hard_timeout = duration[1]
    #print "event.ofp.buffer_id: ", event.ofp.buffer_id
    if _called_from == 'packet_in':
	    msg.buffer_id = event.ofp.buffer_id
    msg.actions.append(of.ofp_action_output(port = o_port))
    event.connection.send(msg)
    print "\nFrom dpid: ", event.connection.dpid, "send_ofmod_forward ", "src_ip: ", nw_src
    print " dst_ip: ",nw_dst,"fport: ",o_port," is sent\n"
  
  def send_ofmod_modify_forward (self, _called_from, event, nw_src, nw_dst, new_dst, new_dl_dst,o_port, duration):
    msg = of.ofp_flow_mod()
    msg.priority = 0x7000
    msg.match.dl_type = 0x800 # Ethertype / length (e.g. 0x0800 = IPv4)
    msg.match.nw_src = IPAddr(nw_src)
    msg.match.nw_dst = IPAddr(nw_dst)
    msg.match.nw_proto = 17 #UDP
    msg.match.tp_dst = 5000
    msg.idle_timeout = duration[0]
    msg.hard_timeout = duration[1]
    if _called_from == 'packet_in':
	    msg.buffer_id = event.ofp.buffer_id
    msg.actions.append(of.ofp_action_nw_addr(nw_addr = IPAddr(new_dst), type=7))
    msg.actions.append(of.ofp_action_dl_addr(dl_addr = EthAddr(new_dl_dst), type=5))
    msg.actions.append(of.ofp_action_output(port = o_port))
    event.connection.send(msg)
    print "\nFrom dpid: ", event.connection.dpid, "send_ofmod_modify_forward", "src_ip: ",nw_src,
    print " dst_ip: ",nw_dst,"new_dst_ip: ",new_dst, "new_dst_mac", new_dl_dst, "fport: ", o_port, " is sent\n"
  
  # Method for just sending a packet to any port (broadcast by default)
  def send_packet (self, event, dst_port = of.OFPP_ALL):
    msg = of.ofp_packet_out(in_port=event.ofp.in_port)
    if event.ofp.buffer_id != -1 and event.ofp.buffer_id is not None:
      # We got a buffer ID from the switch; use that
      msg.buffer_id = event.ofp.buffer_id
    else:
      # No buffer ID from switch -- we got the raw data
      if event.ofp.data:
        # No raw_data specified -- nothing to send!
        return
      msg.data = event.ofp.data
    msg.actions.append(of.ofp_action_output(port = dst_port))
    event.connection.send(msg)
    print "send_packet; sw_dpid:%s and dst_port:%s" %(dpid_to_str(event.connection.dpid), dst_port)

_no_flood_by_default = None
_install_initial_flow = None

def launch (initial_install=True, no_flood=True):
  global _install_initial_flow, _no_flood_by_default
  
  _install_initial_flow = str_to_bool(initial_install)
  _no_flood_by_default = str_to_bool(no_flood)
  
  
  core.registerNew(Controller1)
  
  """
  udp = packet.find('udp')
  if udp is None:
    print "This packet isn't UDP!"
    return
  print "UDP is found", udp.payload
  """	
  
  """
  fm = of.ofp_flow_mod()
  fm.priority = 0x7000 # Pretty high
  fm.match.dl_type = ethernet.ARP_TYPE#IP_TYPE
  fm.match.dl_dst = EthAddr("ff:ff:ff:ff:ff:ff")
  fm.idle_timeout = 1000
  fm.hard_timeout = 0
  fm.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
  event.connection.send(fm)
  print "_install_flow is done for ", event.connection
  self.send_stat_req(event)  
  """

