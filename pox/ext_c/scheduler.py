import json, pprint, os, inspect, sys
from xmlparser import XMLParser
from graphman import GraphMan
from scheduling_optimization import SchingOptimizer
from perf_plot import PerfPlotter
from control_comm_intf import ControlCommIntf

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"ext")))
if cmd_subfolder not in sys.path:
   sys.path.insert(0, cmd_subfolder)
# to import pox modules while __name__ == "__main__"
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parentdir not in sys.path:
  sys.path.insert(0,parentdir)
  
"""
from pox.lib.revent.revent import Event, EventMixin
class SchResReadyToBeSent (Event):
  def __init__ (self, sch_res = None):
    Event.__init__(self)
    self.sch_res = sch_res
 
  @property
  def get_sch_res (self):
    return self.sch_res

class TprRuleReadyToBeSent (Event):
  def __init__ (self, tpr_rule = None):
    Event.__init__(self)
    self.tpr_rule = tpr_rule
 
  @property
  def get_tpr_rule (self):
    return self.tpr_rule

class EventChief (EventMixin):
  _eventMixin_events = set([
    SchResReadyToBeSent,
    TprRuleReadyToBeSent,
  ])
  def raise_event(self, event_type, arg):
    if event_type == 'sch_res_ready_to_be_sent':
      #sargs = ["Generic"] #[sch_res, "Generic"]
      self.raiseEvent(SchResReadyToBeSent(arg)) #sch_res
    elif event_type == 'tpr_rule_ready_to_be_sent':
      #args = ["Generic"]
      self.raiseEvent(TprRuleReadyToBeSent(arg)) #tpr_rule
    else:
      print 'Unknown event_type: ', event_type
      raise KeyError('Unknown event_type')
#
"""
info_dict = {'acterl_addr':('127.0.0.1',7999), #192.168.56.1
             'lacter_addr':('127.0.0.1',7998),
             'scher_vip':'10.0.0.255',
             'base_sport':6000,
             'sching_tp_src':7001,
             'sching_tp_dst':7000
            }
  
class Scheduler(object):
  #event_chief = EventChief()
  def __init__(self, xml_network_number):
    self.gm = GraphMan()
    if is_scheduler_run:
      self.xml_parser = XMLParser("net_xmls/net_2p_stwithsingleitr.xml", str(xml_network_number))
    else:
      self.xml_parser = XMLParser("ext/net_xmls/net_2p_stwithsingleitr.xml", str(xml_network_number))
    self.init_network_from_xml()
    #Useful state variables
    self.last_sch_req_id_given = -1
    self.last_tp_dst_given = info_dict['base_sport']-1
    #Scher state dicts
    self.N = 0 #num_activesessions
    self.sessions_beingserved_dict = {}
    self.sessions_pre_served_dict = {}
    self.sid_res_dict = {}
    self.actual_res_dict = self.gm.give_actual_resource_dict()
    #for perf plotting
    self.perf_plotter = PerfPlotter(self.actual_res_dict)
    #for control_comm
    self.cci = ControlCommIntf()
    self.cci.reg_commpair(sctag = 'scher-acter',
                          proto = 'tcp',
                          _recv_callback = self._handle_recvfromacter,
                          s_addr = info_dict['lacter_addr'],
                          c_addr = info_dict['acterl_addr'] )
  
  def _handle_recvfromacter(self, msg):
    #msg = [type_, data_]
    print 'recvedfromacter msg=%s' % msg
  
  def print_scher_state(self):
    print '<-------------------H--------------------->'
    print 'is_scheduler_run: ', is_scheduler_run
    print 'sessions_beingserved_dict:'
    pprint.pprint(self.sessions_beingserved_dict)
    print 'sessions_pre_served_dict:'
    pprint.pprint(self.sessions_pre_served_dict)
    print '<-------------------E--------------------->'
  
  def next_sch_req_id(self):
    self.last_sch_req_id_given += 1
    return  self.last_sch_req_id_given
  
  def next_tp_dst(self):
    self.last_tp_dst_given += 1
    return  self.last_tp_dst_given
  
  def welcome_session(self, p_c_ip_list, p_c_gw_list, req_dict, app_pref_dict):
    """
    sch_req_id: should be unique for every sch_session
    """
    #update global var, list and dicts
    self.N += 1
    s_tp_dst_list = [self.next_tp_dst() for i in range(0,req_dict['parism_level'])]
    sch_req_id = self.next_sch_req_id()
    self.sessions_beingserved_dict.update(
      {sch_req_id:{'tp_dst_list':s_tp_dst_list,
                   'req_dict':req_dict,
                   'p_c_ip_list':p_c_ip_list,
                   'p_c_gw_list':p_c_gw_list,
                   'app_pref_dict': app_pref_dict,
                   'sch_job_done':False }
      }
    )
    #print 'self.sessions_beingserved_dict: '
    #pprint.pprint(self.sessions_beingserved_dict)
  
  def bye_session(self, sch_req_id):
    self.N -= 1
    # Send sessions whose "sching job" is done is sent to pre_served category
    self.sessions_pre_served_dict.update(
    {sch_req_id: self.sessions_beingserved_dict[sch_req_id]})
    del self.sessions_beingserved_dict[sch_req_id]
  
  def update_sid_res_dict(self):
    """
    Network resources will be only the ones on the session_shortest path.
    It resources need to lie on the session_shortest path.
    """
    print '------ update_sid_res_dict ------'
    #TODO: sessions whose resources are already specified no need for putting them in the loop
    for s_id in self.sessions_beingserved_dict:
      p_c_gw_list = self.sessions_beingserved_dict[s_id]['p_c_gw_list']
      s_all_paths = self.gm.give_all_paths(p_c_gw_list[0], p_c_gw_list[1])
      #print out all_paths for debugging
      dict_ = {i:p for i,p in enumerate(s_all_paths)}
      print 's_id:%i, all_paths:' % s_id
      pprint.pprint(dict_)
      #
      for i,p in dict_.items():
        p_net_edge_list = self.gm.pathlist_to_netedgelist(p)
        p_itres_list = self.gm.give_itreslist_on_path(p)
        if not (s_id in self.sid_res_dict):
          self.sid_res_dict[s_id] = {'s_info':{}, 'ps_info':{}}
        self.sid_res_dict[s_id]['ps_info'].update(
          {i: {'path': p,
               'net_edge_list': p_net_edge_list,
               'itres_list': p_itres_list
              }}
        )
    print '---------------- OOO ----------------'
  
  def do_sching(self):
    '''
    For currently active sessions, get things together to work sching logic and
    then send corresponding rules to correspoding actuator (which is a single 
    actuator right now !)
    '''
    alloc_dict = self.allocate_resources()
    print '---------------SCHING Started ---------------'
    print 'alloc_dict:'
    pprint.pprint(alloc_dict)
    #'''
    self.perf_plotter.save_sching_result(alloc_dict['general'],
                                         alloc_dict['s-wise'], 
                                         alloc_dict['res-wise'])
    #'''
    #Convert sching decs to rules
    print '**** self.N: ', self.N
    for s_id in range(0,self.N):
      s_allocinfo_dict = alloc_dict['s-wise'][s_id]
      #
      itwalkinfo_dict = s_allocinfo_dict['itwalkinfo_dict']
      p_walk_dict = s_allocinfo_dict['pwalk_dict']
      for p_id in range(0,s_allocinfo_dict['parism_level']):
        p_walk = p_walk_dict[p_id]
        #Dispatching rule to actuator_actuator
        sp_walk__tprrule = \
          self.get_spwalkrule__sptprrule(s_id, p_id,
                                         p_walk = p_walk,
                                         pitwalkbundle_dict = itwalkinfo_dict[p_id])
        print 'for s_id:%i, p_id:%i;' % (s_id, p_id)
        #print 'walkrule:'
        #pprint.pprint(sp_walk__tprrule['walk_rule'])
        #print 'itjob_rule:'
        #pprint.pprint(sp_walk__tprrule['itjob_rule'])
        msg = json.dumps({'type':'sp_sching_dec',
                          'data':{'s_id':s_id, 'p_id':p_id, 
                                  'walk_rule':sp_walk__tprrule['walk_rule'],
                                  'itjob_rule':sp_walk__tprrule['itjob_rule']} })
        self.cci.send_to_client('scher-acter', msg)
    print '---------------SCHING End---------------'
  
  def get_spwalkrule__sptprrule(self,s_id,p_id,p_walk,pitwalkbundle_dict):
    #print '---> for s_id:%i' % s_id
    #print 'pitwalkbundle_dict:'
    #pprint.pprint(pitwalkbundle_dict)
    #print 'p_walk: ', p_walk
    s_info_dict =  self.sessions_beingserved_dict[s_id]
    s_tp_dst = s_info_dict['tp_dst_list'][p_id]
    p_c_ip_list = s_info_dict['p_c_ip_list']
    #
    itjob_rule_dict = {}
    #
    walk_rule = []
    cur_from_ip = p_c_ip_list[0]
    cur_to_ip = p_c_ip_list[1]
    duration = 50
    cur_node_str = None
    for i,node_str in list(enumerate(p_walk)):#node = next_hop
      if i == 0:
        cur_node_str = node_str
        #for adding reverse-walk rule for gw_sw
        #TODO: 's11-eth1' must be gotten autonomously
        node = self.gm.get_node(node_str)
        walk_rule.append({'conn':[node['dpid'],cur_to_ip],
                          'typ':'forward',
                          'wc':[cur_to_ip,p_c_ip_list[0],int(s_tp_dst)],
                          'rule':['s11-eth1', duration] })
        #
        continue
      cur_node = self.gm.get_node(cur_node_str)
      if cur_node['type'] == 't':
        cur_node_str = node_str
        continue
      #
      node = self.gm.get_node(node_str)
      edge = self.gm.get_edge(cur_node_str, node_str)
      if node['type'] == 't': #sw-t
        walk_rule.append({'conn':[cur_node['dpid'],cur_from_ip],
                          'typ':'modify_forward',
                          'wc':[cur_from_ip,cur_to_ip,int(s_tp_dst)],
                          'rule':[node['ip'],node['mac'],edge['pre_dev'],duration]
                         })
        if not (cur_node['dpid'] in itjob_rule_dict):
          itjob_rule_dict[cur_node['dpid']] = [{
            'tpr_ip':node['ip'],
            'tpr_mac':node['mac'],
            'swdev_to_tpr':edge['pre_dev'],
            'assigned_job': pitwalkbundle_dict['itbundle'][node_str],
            'session_tp': int(s_tp_dst),
            'consumer_ip': cur_to_ip,
            'datasize': pitwalkbundle_dict['p_info']['datasize'] }]
        else:
          itjob_rule_dict[cur_node['dpid']].append( [{
            'tpr_ip':node['ip'],
            'tpr_mac':node['mac'],
            'swdev_to_tpr':edge['pre_dev'],
            'assigned_job':pitwalkbundle_dict['itbundle'][node_str],
            'session_tp': int(s_tp_dst),
            'consumer_ip': cur_to_ip,
            'datasize': pitwalkbundle_dict['p_info']['datasize'] }] )
        cur_from_ip = node['ip']
      elif node['type'] == 'sw': #sw-sw
        walk_rule.append({'conn':[cur_node['dpid'],cur_from_ip],
                          'typ':'forward',
                          'wc':[cur_from_ip,cur_to_ip,int(s_tp_dst)],
                          'rule':[edge['pre_dev'], duration] })
        cur_from_ip
        #for reverse walk: data from c to p
        walk_rule.append({'conn':[node['dpid'],cur_to_ip],
                          'typ':'forward',
                          'wc':[cur_to_ip,p_c_ip_list[0],int(s_tp_dst)],
                          'rule':[edge['post_dev'], duration] })
        '''
        #to deliver sch_response to src
        walk_rule.append({'conn':[node['dpid'],info_dict['scher_vip']],
                          'typ':'forward',
                          'wc':[info_dict['scher_vip'],p_c_ip_list[0], info_dict['sching_tp_dst']],
                          'rule':[edge['post_dev'], duration] })
        '''
      else:
        raise KeyError('Unknown node_type')
      cur_node_str = node_str
    #default rule to forward packet to consumer
    #TODO: 's12-eth2' must be gotten autonomously
    walk_rule.append({'conn':[12,cur_from_ip],
                      'typ':'forward',
                      'wc':[cur_from_ip,cur_to_ip,int(s_tp_dst)],
                      'rule':['s12-eth2',duration]
                     })
    """
    #default rule to forward sch_response to producer
    walk_rule.append({'conn':[11,info_dict['scher_vip']],
                      'typ':'forward',
                      'wc':[info_dict['scher_vip'],p_c_ip_list[0]],
                      'rule':['s11-eth1',duration]
                     })
    """
    return {'walk_rule':walk_rule, 'itjob_rule':itjob_rule_dict}
  
  def allocate_resources(self):
    #returns alloc_dict
    self.update_sid_res_dict()
    sching_opter = SchingOptimizer(self.sessions_beingserved_dict,
                                   self.actual_res_dict,
                                   self.sid_res_dict
                                  )
    sching_opter.solve()
    #
    return sching_opter.get_sching_result()
  
  def init_network_from_xml(self):
    node_edge_lst = self.xml_parser.give_node_and_edge_list_from_xml()
    #print 'node_lst:'
    #pprint.pprint(node_edge_lst['node_lst'])
    #print 'edge_lst:'
    #pprint.pprint(node_edge_lst['edge_lst'])
    self.gm.graph_add_nodes(node_edge_lst['node_lst'])
    self.gm.graph_add_edges(node_edge_lst['edge_lst'])
  
  def test(self):
    num_session = 2
    '''
    sr1:
      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3']}
      {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0}
    '''
    '''
    {'data_size':2, 'slack_metric':60, 'func_list':['f1', 'f2']},
    {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
    {'data_size':0.1, 'slack_metric':4, 'func_list':['f1']},
    '''
    req_dict_list = [ {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':1, 'par_share':[1]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                      {'data_size':1, 'slack_metric':24, 'func_list':['f1','f2','f3'], 'parism_level':2, 'par_share':[0.5, 0.5]},
                    ]
    """
    app_pref_dict_list = [
                          {'m_p': 1,'m_u': 0.1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                         ]
    """
    app_pref_dict_list = [
                          {'m_p': 10,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 10,'m_u': 0.5,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 0.5,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                          {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0},
                         ]
    p_c_ip_list_list = [
                        ['10.0.0.2','10.0.0.1'],
                       ]
    p_c_gw_list_list = [
                        ['s11', 's12'],
                       ]
    for i in range(0, num_session):
      self.welcome_session(p_c_ip_list_list[0], p_c_gw_list_list[0],
                           req_dict_list[i], app_pref_dict_list[i] )
    self.do_sching()
    """
    #DENEME
    g_info_dict = {'max_numspaths':2, 'll_index':4}
    #for p_r__alloc plotting
    s_info_dict = {
      0: {
          'p_bw': [24.84343386893252, -2.4547204946537794e-21],
          'p_dur': [4.0098990234282693e-08, 1.4525739583368101e-22],
          'p_proc': [294.37116687292303, -2.9347854917429113e-19],
         },
      1: {
          'p_bw': [24.84343386893252, -2.4547204946537794e-21],
          'p_dur': [4.0098990234282693e-08, 1.4525739583368101e-22],
          'p_proc': [294.37116687292303, -2.9347854917429113e-19],
         },
      2: {
          'p_bw': [24.84343386893252, -2.4547204946537794e-21],
          'p_dur': [4.0098990234282693e-08, 1.4525739583368101e-22],
          'p_proc': [294.37116687292303, -2.9347854917429113e-19],
         },
      3: {
          'p_bw': [24.84343386893252, -2.4547204946537794e-21],
          'p_dur': [4.0098990234282693e-08, 1.4525739583368101e-22],
          'p_proc': [294.37116687292303, -2.9347854917429113e-19],
         }
    }
    #self.perf_plotter.save_sching_result(g_info_dict, s_info_dict, None)
    #for res session portion alloc plotting
    res_info_dict = {
      0: {'bw': 56.546990163154547,
          'bw_palloc_list': [24.843370569526662,
                             10.304778192360112,
                             11.094062391141305,
                             10.304778192188895]},
      1: {'bw': 56.546990163154547,
          'bw_palloc_list': [24.843370569526662,
                             10.304778192360112,
                             11.094062391141305,
                             10.304778192188895]},
      2: {'bw': 99.999999991730704,
          'bw_palloc_list': [24.843370569526662,
                             24.28381900217388,
                             26.588991417878624,
                             24.283819002151606]},
      3: {'bw': 43.453009828576164,
          'bw_palloc_list': [-9.366893991447322e-34,
                             13.979040809813766,
                             15.49492902673732,
                             13.979040809962711]},
      4: {'bw': 99.999999991730704,
          'bw_palloc_list': [24.843370569526662,
                             24.28381900217388,
                             26.588991417878624,
                             24.283819002151606]},
      5: {'dur_palloc_list': [6.6527897977695746e-09,
                              6.964034371911032e-09,
                              5.79412850313757e-09,
                              6.9640344165499515e-09],
          'proc_palloc_list': [98.12618834860451,
                               0.6234061671802416,
                               0.626998865206443,
                               0.6234061672075883]},
      6: {'dur_palloc_list': [3.6687930228967406e-18,
                              3.4733829064567034e-09,
                              2.8884192155580274e-09,
                              3.4733828703764218e-09],
          'proc_palloc_list': [4.399418514918891e-18,
                               23.82312662679616,
                               52.35374651644713,
                               23.823126627002626]},
      7: {'dur_palloc_list': [2.778359340740923e-19,
                              3.4733829098222416e-09,
                              2.8884189600808926e-09,
                              3.4733830026069085e-09],
          'proc_palloc_list': [-8.929869324033728e-19,
                               23.823126626799475,
                               52.353746516737765,
                               23.823126626708657]},
      8: {'dur_palloc_list': [1.0959833174366283e-18,
                              3.4733829212014637e-09,
                              2.888419251834689e-09,
                              3.4733826370267986e-09],
          'proc_palloc_list': [1.7540003622870305e-18,
                               23.823126626883827,
                               52.35374651672901,
                               23.82312662663306]},
      9: {'dur_palloc_list': [8.057118791661958e-18,
                              3.4733827853772818e-09,
                              2.8884182561784826e-09,
                              3.4733824276965557e-09],
          'proc_palloc_list': [1.6662375988161964e-18,
                               23.823126626845692,
                               52.353746516580635,
                               23.823126626819597]},
      10: {'dur_palloc_list': [-3.349129480374196e-18,
                               3.4733834313550116e-09,
                               2.888419330870589e-09,
                               3.473382717244568e-09],
           'proc_palloc_list': [6.316048746285588e-18,
                                23.82312662682369,
                                52.353746516473905,
                                23.82312662694829]},
      11: {'dur_palloc_list': [-1.1104957900058857e-17,
                               3.4733821624979717e-09,
                               2.8884190713851053e-09,
                               3.473383294430109e-09],
           'proc_palloc_list': [6.764673292784063e-19,
                                23.823126626821423,
                                52.35374651663706,
                                23.823126626787413]},
      12: {'dur_palloc_list': [6.652789742217586e-09,
                               6.9640347738148275e-09,
                               5.794128105937587e-09,
                               6.964035192969033e-09],
           'proc_palloc_list': [98.12618834860756,
                                0.6234061671786015,
                                0.6269988652061944,
                                0.6234061672064036]},
      13: {'dur_palloc_list': [6.652789806352765e-09,
                               6.9640342062035945e-09,
                               5.794128685031484e-09,
                               6.964034151689216e-09],
           'proc_palloc_list': [98.12618834863456,
                                0.6234061671794716,
                                0.6269988651799244,
                                0.6234061672048473]}
    }
    self.perf_plotter.save_sching_result(g_info_dict, s_info_dict, res_info_dict)
    """
  
is_scheduler_run = False
def main():
  global is_scheduler_run
  is_scheduler_run = True
  sch = Scheduler(1)
  sch.test()
  #
  raw_input('Enter')
  #server.shutdown()


if __name__ == "__main__":
  main()
  
