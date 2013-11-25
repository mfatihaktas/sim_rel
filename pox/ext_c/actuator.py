"""
Realizing Sching decisions.
(Acting on sching_decs)
"""
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
from pox.openflow.of_json import *
import os, sys, inspect, SocketServer, threading, json, pprint
  
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"ext")))
if cmd_subfolder not in sys.path:
   sys.path.insert(0, cmd_subfolder)
  
from ruleparser import RuleParser
from errors import *
from control_comm_intf import ControlCommIntf

log = core.getLogger()
#Right now this dict is filled up by HAND
#TODO: Do this autonomically
info_dict = {'gw_dpid_list': [11,12],
             'lscher_addr':('127.0.0.1', 7999),
             'scherl_addr':('127.0.0.1', 7998),
             'lsensor_addr':'...',
             'sensorl_addr':'...',
             'acter_vip': '10.0.0.2',
             'acter_vmac': '00:00:00:01:00:02',
             'sid_pidlist_dict': {},
             'sching_tp_src': 7001,
             'sching_tp_dst': 7000,
             's_entry_dur': [0, 0],
            }
  
ruleparser = RuleParser('ext/schedwalks.xml', 'ext/scheditjobs.xml')

class Actuator (object):
  def __init__ (self):
    #TODO: active sching_realization
    #for control comm with scher, ...
    self.cci = ControlCommIntf()
    self.cci.reg_commpair(sctag = 'acter-scher',
                          proto = 'tcp',
                          _recv_callback = self._handle_recvfromscher,
                          s_addr = info_dict['lscher_addr'],
                          c_addr = info_dict['scherl_addr'] )
    #core.addListeners(self) <- bu aptal neden calismiyo anlamadim
    core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", self._handle_FlowStatsReceived)
    core.openflow.addListenerByName("PacketIn", self._handle_PacketIn  )
  
  #########################  _handle_*** methods  #######################
  def _handle_recvfromscher(self, msg):
    #msg = [type_, data_]
    [type_, data_] = msg
    if type_ == 'sp_sching_dec':
      s_id, p_id = int(data_['s_id']), int(data_['p_id'])
      walk_rule = data_['walk_rule']
      itjob_rule = data_['itjob_rule']
      #print 'walk_rule: '
      #pprint.pprint(walk_rule)
      #updating global dicts based on the input rxed from scher
      if not (s_id in info_dict['sid_pidlist_dict']):
        info_dict['sid_pidlist_dict'][s_id] = []
      info_dict['sid_pidlist_dict'][s_id].append(p_id)
      #
      ruleparser.modify_schedwalkxmlfile_by_walkrule(str(s_id),str(p_id),walk_rule)
      ruleparser.modify_scheditjobxmlfile_by_itjobrule(str(s_id),str(p_id),itjob_rule)
      if _install_schrules_proactively:
        self.install_proactive_schedwalk(s_id, p_id)
        self.install_proactive_scheditjob(s_id, p_id)
      # Send "I am done with the job(sch realization)" TO SCHER_CONT
      msg = json.dumps({'type':'sp_sching_reply',
                        'data':'done' } )
      self.cci.send_to_client('acter-scher', msg)
    elif type_ == 'sth_else':
      pass
  
  #Since the SW rules are set proactively from the beginning no packet_in is expected !
  def _handle_PacketIn (self, event):
    packet = event.parsed
    print '---> handle_data_packet is called;'
    ip = packet.find('ipv4')
    if ip is None:
      print "packet", packet," isn't IP!"
      return
    print "Rxed packet: ", packet, "from sw_dpid: ", dpidToStr(event.connection.dpid)
    print "Src IP:%s, Dst IP: %s" %(ip.srcip, ip.dstip)
  
  def _handle_ConnectionUp (self, event):
    print "Connection %s" % (event.connection)
    if _install_deneme_flow and event.connection.dpid == 3:
      print "Sending deneme_flow to sw_dpid:%s " %(event.connection.dpid)
      self.send_ofmod_forward ('handle_conn_up', event.connection, '10.0.0.32', '10.0.0.31', 
                               6000, 4, info_dict['s_entry_dur'])
  
  def _handle_FlowStatsReceived (self, event):
    stats = flow_stats_to_list(event.stats)
    print "FlowStatsReceived from ",dpidToStr(event.connection.dpid), ": ",stats
  
  #ofcourse works only for mininet networks
  def dev_tfport(self, dev_str):
    eth_part = dev_str.split('-', 1)[1]
    return int(eth_part.strip('eth'))
  #########################  install_*** methods  #######################
  def install_proactive_scheditjob(self, s_id, p_id):
    dict_ = ruleparser.get_itjobruledict_forsp(str(s_id), str(p_id))
    print 'itjobdict:'
    pprint.pprint(dict_)
    for conn in core.openflow.connections:
      dpid = str(conn.dpid)
      try:
        itnodeinfo_list = dict_[dpid]
      except KeyError: #sw is not connected to any itnode on the sched walk
        continue
      for itnodeinfo in itnodeinfo_list:
        jobinfo = itnodeinfo['jobinfo']
        walkinfo = itnodeinfo['walkinfo']
        #
        self.send_udp_packet_out(conn=conn,
                                 fw_port=self.dev_tfport(str(walkinfo['swdev_to_node']) ),
                                 payload=json.dumps({'type':'itjobrule',
                                                     'data': jobinfo}),
                                 tp_src=info_dict['sching_tp_src'],
                                 tp_dst=info_dict['sching_tp_dst'],
                                 src_ip=info_dict['acter_vip'],
                                 dst_ip=walkinfo['node_ip'],
                                 src_mac=info_dict['acter_vmac'],
                                 dst_mac=walkinfo['node_mac'] )
  
  def install_proactive_schedwalk(self, s_id,p_id):
    [dict_I, hmfromdpid_dict] = ruleparser.get_walkruledict_forsp(str(s_id), str(p_id))
    #print 'walkruledict:'
    #pprint.pprint(dict_I)
    #print 'hmfromdpid_dict:'
    #pprint.pprint(hmfromdpid_dict)
    for conn in core.openflow.connections:
      dpid = str(conn.dpid) #str(event.connection.dpid)
      try:
        hm = hmfromdpid_dict[dpid]
      except (KeyError):
        print '\n# No entry in hm_from_dpid for dpid=%s' % dpid
        continue
      l_dict = None
      counter = 0
      while (counter <= hm):
        l_dict = dict_I[dpid, counter]
        typ = l_dict['typ']
        rule_dict = l_dict['rule_dict']
        wc_dict = l_dict['wc_dict']

        if typ == 'forward':
          self.send_ofmod_forward('initial_flows',conn,wc_dict['src_ip'],wc_dict['dst_ip'],
                             wc_dict['tp_dst'],self.dev_tfport(rule_dict['fport']), info_dict['s_entry_dur'])
          #self.send_stat_req(conn)
        elif typ == 'modify_forward':
          self.send_ofmod_modify_forward('initial_flows', conn, wc_dict['src_ip'], 
                                    wc_dict['dst_ip'],wc_dict['tp_dst'],rule_dict['new_dst_ip'],
                                    rule_dict['new_dst_mac'],self.dev_tfport(rule_dict['fport']), info_dict['s_entry_dur'])
          #self.send_stat_req(conn)
        counter += 1
  #######################  send_*** methods  ###################################
  # Method for just sending a UDP packet over any sw_port (broadcast by default)
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
    print "self.send_udp_packet_out; sw%s and fw_port:%s" %(conn.dpid, fw_port)
    conn.send(msg)
  
  #Basic send functions for communicating with SWs
  def send_clear_swtable(self, conn):
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    conn.send(msg)
    print 'clearing flows from %s.' % dpid_to_str(event.connection.dpid)
  
  def send_stat_req(self, conn):
    conn.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
    print "\nsend_stat_req to sw_dpid=%s\n" % conn.dpid
  
  def send_ofmod_delete(self, conn, nw_src, nw_dst, tp_dst, duration):
    msg = of.ofp_flow_mod()
    msg.command = OFPFC_DELETE
    #wcs
    msg.match.dl_type = 0x800 # Ethertype / length (e.g. 0x0800 = IPv4)
    msg.match.nw_src = IPAddr(nw_src)
    msg.match.nw_dst = IPAddr(nw_dst)
    msg.match.nw_proto = 17 #UDP
    msg.match.tp_dst = int(tp_dst)
    #
    msg.idle_timeout = duration[0]
    msg.hard_timeout = duration[1]
    conn.send(msg)
    print '\nsend_ofmod_delete to sw_dpid=%s' % conn.dpid
    print 'wcs: src_ip=%s, dst_ip=%s, tp_dst=%s\n' % (nw_src,nw_dst,tp_dst)
  
  def send_ofmod_forward(self, _called_from, conn, nw_src, nw_dst, tp_dst, fport, duration):
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
    msg.actions.append(of.ofp_action_output(port = fport))
    conn.send(msg)
    print '\nsend_ofmod_forward to sw_dpid=%s' % conn.dpid
    print 'wcs: src_ip=%s, dst_ip=%s, tp_dst=%s' % (nw_src,nw_dst,tp_dst)
    print 'acts: fport=%s\n', fport
  
  def send_ofmod_modify_forward(self, _called_from, conn, nw_src, nw_dst, tp_dst, new_dst, new_dl_dst,fport, duration):
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
    msg.actions.append(of.ofp_action_output(port = fport))
    conn.send(msg)
    print '\nsend_ofmod_modify_forward to sw_dpid=%s' % conn.dpid
    print 'wcs: src_ip=%s, dst_ip=%s, tp_dst=%s' % (nw_src,nw_dst,tp_dst)
    print 'acts: new_dst=%s, new_dl_dst=%s, fport=%s\n' % (new_dst, new_dl_dst, fport)
################################################################################
_install_schrules_proactively = None
_install_deneme_flow = None

def launch (proactive_install=True, deneme_flow=False):
  global _install_schrules_proactively, _install_deneme_flow
  #
  _install_schrules_proactively = str_to_bool(proactive_install)
  _install_deneme_flow = str_to_bool(deneme_flow)
  #
  core.registerNew(Actuator)


