from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
from pox.openflow.of_json import *
#from pox.lib.util import dpid_to_str
from scheduler import Scheduler #, EventChief
import pprint
log = core.getLogger()

info_dict = {'scher_vip': '10.0.0.255',
             'scher_vmac': '00:00:00:00:00:00',
             'sching_port': 7000,
            }
  
class SchController(object):
  def __init__(self):
    self.scheduler = Scheduler(xml_net_num = 1,
                               sching_logto = 'console')
    #
    self.scheduler.event_chief.addListenerByName("SendMsgToUser",
                                                 self._handle_SendMsgToUser)
    #
    self.dpid_conn_dict = {}
    #core.addListeners(self)
    core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", self._handle_FlowStatsReceived)
    core.openflow.addListenerByName("PacketIn", self._handle_PacketIn  )
  
  #########################  _handle_*** methods  #######################
  def _handle_SendMsgToUser(self, event):
    print '_handle_SendMsgToUser;'
    #dict_ includes info necessary to send packet_out
    dict_ = event.info_dict
    conn = self.dpid_conn_dict[dict_['gw_dpid']]
    self.send_udp_packet_out(
          conn, payload=event.msg, fw_port=dict_['gw_conn_port'],
          tp_src=info_dict['sching_port'], tp_dst=info_dict['sching_port'],
          src_ip=info_dict['scher_vip'], dst_ip=dict_['ip'],
          src_mac=info_dict['scher_vmac'], dst_mac=dict_['mac'] )
  
  def _handle_PacketIn(self, event):
    eth_packet = event.parsed
    conn = event.connection
    print '\nsch_controller: eth_packet is rxed from sw_dpid=%s' % conn.dpid
    ip_packet = eth_packet.find('ipv4')
    if ip_packet is None:
      print 'eth_packet=%s doesnt have ip_payload' %  eth_packet
      return
    #
    src_ip = (ip_packet.srcip).toStr()
    src_mac = (eth_packet.src).toStr()
    #handle_recv - assume only dts users know about udp_dts_port, no checking
    dtsuserinfo_dict = {'src_ip': src_ip,
                        'src_mac': src_mac,
                        'src_gw_dpid':conn.dpid,
                        'src_gw_conn_port':event.port}
    msg = (ip_packet.payload).payload
    print 'msg=%s' % msg
    print 'dtsuserinfo_dict='
    pprint.pprint(dtsuserinfo_dict)
    self.scheduler._handle_recvfromdtsuser(msg, dtsuserinfo_dict)
  
  def _handle_ConnectionUp(self, event):
    print "ConnectionUp %s" % (event.connection)
    self.dpid_conn_dict[event.connection.dpid] = event.connection
    self.install_default_to_controller(event)
    #self.install_drop_sch_response(event)
  
  def _handle_FlowStatsReceived (self, event): 
    stats = flow_stats_to_list(event.stats)
    print "FlowStatsReceived from sw",event.connection.dpid, ": ",stats
  #######################  send_*** methods  ###################################
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
  
  def send_stat_req(self, event):
    print "ofp_stats_request is sent to sw", event.connection.dpid
    event.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
  #########################  install_*** methods  #######################
  def install_drop_sch_response(self, event):
    fm = of.ofp_flow_mod()
    fm.priority = 0x0002 # should be higher than default_to_controller !
    fm.match.dl_type = ethernet.IP_TYPE
    fm.match.nw_src = IPAddr(info_dict['scher_vip'])
    fm.match.nw_proto = 17 #UDP
    fm.match.tp_dst = info_dict['sching_port']
    fm.idle_timeout = 0
    fm.hard_timeout = 0
    event.connection.send(fm)
    print "install_drop_sch_response is done for ", event.connection
  
  def install_default_to_controller(self, event):
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
  ##############################################################################
def launch ():
  core.registerNew(SchController)
  
