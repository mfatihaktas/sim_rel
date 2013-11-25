from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
import time
from pox.openflow.of_json import *

import os, sys, inspect, threading, json
from scheduler import Scheduler, EventChief

log = core.getLogger()

hostip_gwdpid_dict = {'10.0.0.2':11,
                      '10.0.0.1':12
                     }

info_dict = {'gw_dpid_list': [11,12],
             'scher_virtual_ip': '10.0.0.255',
             'scher_virtual_mac': '00:00:00:00:00:00',
             'p_ip': '10.0.0.2',
             'p_mac': '00:00:00:01:00:02',
             'sching_tp_src': 5000,
             'sching_tp_dst': 7000,
             'p_gw_dpid': 11,
             'c_gw_dpid': 12
            }

class SchController (object):
  def __init__ (self):
    #core.addListeners(self) < bu aptal neden calismiyo anlamadim >
    core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", self._handle_FlowStatsReceived)
    core.openflow.addListenerByName("PacketIn", self._handle_PacketIn  )
    ##########################
    self.scheduler = Scheduler(1)
    self.scheduler.event_chief.addListenerByName("SchResReadyToBeSent", 
                                                 self._handle_SchResReadyToBeSent)
    self.scheduler.event_chief.addListenerByName("TprRuleReadyToBeSent", 
                                                 self._handle_TprRuleReadyToBeSent)
    self.sch_req_id_counter = 0
    self.sch_req_info_map = {}
  
  def _handle_TprRuleReadyToBeSent(self, event):
    print '_handle_TprRuleReadyToBeSent is succesfully called !!!'
    self.send_tpr_rule(event.tpr_rule)
  
  def _handle_SchResReadyToBeSent(self, event):
    print '_handle_SchResReadyToBeSent is succesfully called !!!'
    #print 'event.sch_res: ', event.sch_res
    self.send_sch_response(event.sch_res)
  
  def send_tpr_rule(self, tpr_rule):
    def dev_to_port(dev_str):
        eth_part = dev_str.split('-', 1)[1]
        return int(eth_part.strip('eth'))
    for conn in core.openflow.connections:
      dpid = str(conn.dpid)
      try:
        rules = tpr_rule[dpid]
      except (KeyError):
        #print "\n ---> No entry in tpr_rule for dpid: ", dpid, "\n"
        continue
      for rule in rules:
        #print 'rule: ', rule
        tpr_job = {'session_tp':rule['session_tp'], 'job':rule['assigned_job'],
                   'c_ip':rule['c_ip']}
        #send the rule to corresponding tpr
        self.send_udp_packet_out(
        conn, payload=json.dumps(tpr_job),
        tp_src=info_dict['sching_tp_src'], tp_dst=info_dict['sching_tp_dst'],
        src_ip=info_dict['scher_virtual_ip'], dst_ip=rule['tpr_ip'],
        src_mac=info_dict['scher_virtual_mac'], dst_mac=rule['tpr_mac'],
        fw_port = dev_to_port(rule['swdev_to_tpr'])
      )
  
  def send_sch_response (self, sch_res):
    #Initial preps
    sch_req_id = int(sch_res['session_id'])
    del sch_res['session_id']
    sch_req_info = self.sch_req_info_map[sch_req_id]
    gw_dpid = sch_req_info['gw_dpid']
    
    for conn in core.openflow.connections:
      if conn.dpid == gw_dpid:
        self.send_udp_packet_out(
          conn, payload=json.dumps(sch_res),
          tp_src=info_dict['sching_tp_src'], tp_dst=info_dict['sching_tp_dst'],
          src_ip=info_dict['scher_virtual_ip'], dst_ip=info_dict['p_ip'],
          src_mac=info_dict['scher_virtual_mac'], dst_mac=info_dict['p_mac'] )
  
  # Method for just sending a UDP packet over any sw port (broadcast by default)
  def send_udp_packet_out(self, conn, payload, tp_src, tp_dst,src_ip, dst_ip, 
                          src_mac, dst_mac, fw_port = of.OFPP_ALL):
    msg = of.ofp_packet_out(in_port=of.OFPP_NONE)
    msg.buffer_id = None
    #Make the udp packet
    udpp = pkt.udp()
    udpp.srcport = tp_src
    udpp.dstport = tp_dst
    udpp.payload = payload
    #Make the IP packet around it
    ipp = pkt.ipv4()
    ipp.protocol = ipp.UDP_PROTOCOL
    ipp.srcip = IPAddr(src_ip)
    ipp.dstip = IPAddr(dst_ip)
    # Ethernet around that...
    ethp = pkt.ethernet()
    ethp.src = EthAddr(src_mac)
    ethp.dst = EthAddr(dst_mac)
    ethp.type = ethp.IP_TYPE
    # Hook them up...
    ipp.payload = udpp
    ethp.payload = ipp
    # Send it to the sw
    msg.actions.append(of.ofp_action_output(port = fw_port))
    msg.data = ethp.pack()
    #show msg before sending
    """
    print '*******************'
    print 'msg.show(): ',msg.show()
    print '*******************'
    """
    print "send_udp_packet_out; sw%s and fw_port:%s" %(conn.dpid, fw_port)
    conn.send(msg)
  
  def _handle_PacketIn (self, event):
    packet = event.parsed
    ip_packet = packet.find('ipv4')
    print 'a packet is rxed by controller'
    if ip_packet is None:
      print "packet", packet," isn't IP!"
      return
    print "Rxed packet: ", packet, "from sw", event.connection.dpid
    p_ip = ip_packet.srcip
    c_ip = ip_packet.dstip
    print "Src IP:%s, Dst IP: %s" %(ip_packet.srcip, ip_packet.dstip)
    
    payload = (ip_packet.payload).payload
    sch_req_dict = json.loads(payload)
    print 'sch_req_dict: ', sch_req_dict
    
    req_dict = sch_req_dict['req_dict']
    app_pref_dict = sch_req_dict['app_pref_dict']
    #
    #change from unicode str to STR
    '''
    req_dict_ = {}
    req_dict_['data_amount'] = float(req_dict['data_amount'].encode('ascii','ignore'))
    req_dict_['slack_metric'] = float(req_dict['slack_metric'].encode('ascii','ignore'))
    app_pref_dict_ = {k:v.encode('ascii','ignore') for k,v in app_pref_dict.iteritems()}
    '''
    t_func_list = [func.encode('ascii','ignore') for func in req_dict['func_list']]
    req_dict['func_list'] = t_func_list
    #
    self.scheduler.welcome_session(sch_req_id = self.sch_req_id_counter, \
                                   p_c_ip_list = [p_ip, c_ip], \
                                   p_c_gw_list = [hostip_gwdpid_dict[str(p_ip)],
                                                  hostip_gwdpid_dict[str(c_ip)]], \
                                   req_dict = req_dict, \
                                   app_pref_dict = app_pref_dict )
    self.scheduler.do_sching()
    #
    self.sch_req_info_map[self.sch_req_id_counter]={"gw_dpid":event.connection.dpid}
    self.sch_req_id_counter += 1;
  
  def install_drop_sch_response (self, event):
    fm = of.ofp_flow_mod()
    fm.priority = 0x0002 # should be higher than default_to_controller !
    fm.match.dl_type = ethernet.IP_TYPE
    fm.match.nw_src = IPAddr(info_dict['scher_virtual_ip'])
    fm.match.nw_proto = 17 #UDP
    fm.match.tp_dst = info_dict['sching_tp_dst']
    fm.idle_timeout = 0
    fm.hard_timeout = 0
    event.connection.send(fm)
    print "install_drop_sch_response is done for ", event.connection
  
  def install_default_to_controller (self, event):
    fm = of.ofp_flow_mod()
    fm.priority = 0x0001 # Pretty low
    fm.match.dl_type = ethernet.IP_TYPE
    """
    from OF Spec 1.0.0;
     If both idle_timeout and hard_timeout are zero, the entry is considered
     permanent and will never time out. It can still be removed with a flow_mod
     message of type OFPFC_DELETE
    """
    fm.idle_timeout = 0
    fm.hard_timeout = 0
    fm.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    event.connection.send(fm)
    print "install_default_to_controller is done for ", event.connection
  
  def send_stat_req(self, event):
    print "ofp_stats_request is sent to sw", event.connection.dpid
    event.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    
  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection)
    self.install_default_to_controller(event)
    self.install_drop_sch_response(event)
  
  def _handle_FlowStatsReceived (self, event): 
    stats = flow_stats_to_list(event.stats)
    print "FlowStatsReceived from sw",event.connection.dpid, ": ",stats
  
def launch ():
  core.registerNew(SchController)
  
