"""
Realizing Sching decisions.
"""
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
import time
from pox.openflow.of_json import *

import os, sys, inspect, SocketServer, threading, json

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"ext")))
if cmd_subfolder not in sys.path:
   sys.path.insert(0, cmd_subfolder)
   
from ruleparser import RuleParser

log = core.getLogger()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    data = self.request.recv(1024*10) #xml_path_rule
    cur_thread = threading.current_thread()
    print "--------------------------------"
    print "Cont1 rxed cur_thread:{}, data:{}".format(cur_thread.name, data)
    print "--------------------------------"
    #response = "{}: {}".format(cur_thread.name, data)
    response = "OK"
    self.request.sendall(response)
    process_rxed_cmd_from_sch(data)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip, port))
  try:
    sock.sendall(message)
    print "client: sent to_ip: {}, to_port: {}, message: {}".format(ip,port,message)
    response = sock.recv(1024)
    print "Received: {}".format(response)
  finally:
    sock.close()
      
#Right now this dict is filled up by HAND
#TODO: Do this autonomically
info_dict = {'gw_dpid_list': [11,12],
             'listen_sch_from_ip': '192.168.56.1',
             'listen_sch_from_port': 7999,
             'schcont_listening_from_ip': '192.168.56.1',
             'schcont_listening_from_port': 7998,
             'scher_virtual_ip': '10.0.0.255',
             'scher_virtual_mac': '00:00:00:00:00:00',
             'p_ip': '10.0.0.1',
             'p_mac': '00:00:00:01:00:02',
             'session_ids': [],
             'sching_tp_dst': 7000,
             'p_gw_dpid': 11,
             'c_gw_dpid': 12,
             'session_entry_duration': [0, 0]
            }
            
rule_parser = RuleParser("ext/scheduling.xml")
def process_rxed_cmd_from_sch(xml_path_rule):
  session_id = rule_parser.session_num_of_sch_rule(xml_path_rule)
  info_dict['session_ids'].append(session_id)
  rule_parser.modify_by_cmd(xml_path_rule)
  if _install_schrules_proactively:
    install_proactive_scheduling_flows(session_id)
  
  # Send "I am done with the job(sch realization)" TO SCH_CONT
  job_res = {'type':'job_response',
             'session_id':session_id,
             'response': 'Done'
            }
  client(info_dict['schcont_listening_from_ip'], info_dict['schcont_listening_from_port'],
         json.dumps(job_res))
  
def install_proactive_scheduling_flows(session_id):
  dict_I = rule_parser.rule_dict_for_session_I(str(session_id))
  #print "dict_I: ", dict_I
  print "rule_parser.hm_from_dpid: ", rule_parser.hm_from_dpid
  for conn in core.openflow.connections:
    dpid = str(conn.dpid) #str(event.connection.dpid)
    try:
      hm = rule_parser.hm_from_dpid[dpid]
    except (KeyError):
      print "\n ---> No entry in hm_from_dpid for dpid: ", dpid, "\n"
      continue
    
    def dev_to_port(dev_str):
      eth_part = dev_str.split('-', 1)[1]
      return int(eth_part.strip('eth'))
      
    l_dict = None
    counter = 0
    while (counter <= hm):
      l_dict = dict_I[dpid, counter]
      typ = l_dict['typ']
      rule_dict = l_dict['rule_dict']
      wc_dict = l_dict['wc_dict']

      if typ == 'forward':
        send_ofmod_forward('initial_flows',conn,wc_dict['src_ip'],wc_dict['dst_ip'],
        wc_dict['tp_dst'],dev_to_port(rule_dict['fport']), info_dict['session_entry_duration'])
        #send_stat_req(conn)
      elif typ == 'modify_forward':
        send_ofmod_modify_forward('initial_flows', conn, wc_dict['src_ip'], 
        wc_dict['dst_ip'],wc_dict['tp_dst'],rule_dict['new_dst_ip'],
        rule_dict['new_dst_mac'],dev_to_port(rule_dict['fport']), info_dict['session_entry_duration'])
        #send_stat_req(conn)
      
      counter = counter + 1

# Basic send functions for communicating with SWs
def send_stat_req(conn):
    print "ofp_stats_request is sent to ", dpid_to_str(conn.dpid)
    conn.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def send_ofmod_forward (_called_from, conn, nw_src, nw_dst, tp_dst, o_port, duration):
  msg = of.ofp_flow_mod()
  #msg.match = of.ofp_match.from_packet(packet)
  msg.priority = 0x7000
  #msg.match = of.ofp_match(dl_type = pkt.ethernet.IP_TYPE, nw_proto = pkt.ipv4.UDP_PROTOCOL, nw_dst=IPAddr(nw_dst))
  msg.match.dl_type = 0x800 # Ethertype / length (e.g. 0x0800 = IPv4)
  msg.match.nw_src = IPAddr(nw_src)
  msg.match.nw_dst = IPAddr(nw_dst)
  msg.match.nw_proto = 17 #UDP
  if tp_dst != None:
    msg.match.tp_dst = int(tp_dst)
  msg.idle_timeout = duration[0]
  msg.hard_timeout = duration[1]
  #print "event.ofp.buffer_id: ", event.ofp.buffer_id
  if _called_from == 'packet_in':
    msg.buffer_id = event.ofp.buffer_id
  msg.actions.append(of.ofp_action_output(port = o_port))
  conn.send(msg)
  print "\nFrom dpid: ", conn.dpid, "send_ofmod_forward ", "src_ip: ", nw_src
  print " dst_ip: ",nw_dst,"fport: ",o_port," is sent\n"

def send_ofmod_modify_forward (_called_from, conn, nw_src, nw_dst, tp_dst, new_dst, new_dl_dst,o_port, duration):
  msg = of.ofp_flow_mod()
  msg.priority = 0x7000
  msg.match.dl_type = 0x800 # Ethertype / length (e.g. 0x0800 = IPv4)
  msg.match.nw_src = IPAddr(nw_src)
  msg.match.nw_dst = IPAddr(nw_dst)
  msg.match.nw_proto = 17 #UDP
  if tp_dst != None:
    msg.match.tp_dst = int(tp_dst)
  msg.idle_timeout = duration[0]
  msg.hard_timeout = duration[1]
  if _called_from == 'packet_in':
    msg.buffer_id = event.ofp.buffer_id
  msg.actions.append(of.ofp_action_nw_addr(nw_addr = IPAddr(new_dst), type=7))
  msg.actions.append(of.ofp_action_dl_addr(dl_addr = EthAddr(new_dl_dst), type=5))
  msg.actions.append(of.ofp_action_output(port = o_port))
  conn.send(msg)
  print "\nFrom dpid: ", conn.dpid, "send_ofmod_modify_forward", "src_ip: ",nw_src,
  print " dst_ip: ",nw_dst," tp_dst: ",tp_dst," new_dst_ip: ",new_dst, " new_dst_mac: ", new_dl_dst, " fport: ", o_port, " is sent\n"

class Controller1 (object):
  def __init__ (self):
    self.dict_ = rule_parser.rule_dict_for_session(str(info_dict['session_num']))
    # for listening scheduler
    self.HOST = info_dict['listen_sch_from_ip'] #socket.gethostbyname(socket.gethostname())
    self.PORT = info_dict['listen_sch_from_port'] 
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
    core.openflow.addListenerByName("PacketIn", self._handle_PacketIn  )
  
  def _handle_PacketIn (self, event):
    packet = event.parsed
    self.handle_data_packet(event, packet)    

  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection)
    """
    if _install_deneme_flow and event.connection.dpid == 3:
      print "Sending deneme_flow to sw_dpid:%s " %(event.connection.dpid)
      send_ofmod_forward ('handle_conn_up', event.connection, '10.0.0.32', '10.0.0.31', 
                          6000, 4, info_dict['session_entry_duration'])
    """
  def _handle_FlowStatsReceived (self, event):
    stats = flow_stats_to_list(event.stats)
    print "FlowStatsReceived from ",dpidToStr(event.connection.dpid), ": ",stats
  
  def clear_sw_table(self, event):
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    event.connection.send(msg)
    print "Clearing flows from %s." %(dpid_to_str(event.connection.dpid),)
  
  #Since the SW rules are set proactively from the beginning no packet_in is expected !
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
    
    if typ == 'forward':
      send_ofmod_forward('packet_in', event.connection, wc_dict['src_ip'], 
      wc_dict['dst_ip'], wc_dict['tp_dst'], int(rule_dict['fport']), info_dict['session_entry_duration'])
      #send_stat_req(event.connection)
    elif   typ == 'modify_forward':
      send_ofmod_modify_forward('packet_in', event.connection, wc_dict['src_ip'], 
      wc_dict['dst_ip'],wc_dict['tp_dst'], rule_dict['new_dst_ip'], 
      rule_dict['new_dst_mac'], int(rule_dict['fport']), info_dict['session_entry_duration'])
      #send_stat_req(event.connection)
    
_install_schrules_proactively = None
_install_deneme_flow = None

def launch (proactive_install=True, deneme_flow=False, session_num=1):
  global _install_schrules_proactively, _install_deneme_flow
  
  _install_schrules_proactively = str_to_bool(proactive_install)
  _install_deneme_flow = str_to_bool(deneme_flow)
  info_dict['session_num'] = int(session_num)
  
  core.registerNew(Controller1)


