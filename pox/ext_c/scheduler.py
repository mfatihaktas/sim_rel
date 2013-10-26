import socket, SocketServer, threading, json
import pprint, itertools, os, inspect, sys
from xmlparser import XMLParser
from graphman import GraphMan
from scheduling_optimization import SchingOptimizer
from perf_plot import PerfPlotter

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"ext")))
if cmd_subfolder not in sys.path:
   sys.path.insert(0, cmd_subfolder)
# to import pox modules while __name__ == "__main__"
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parentdir not in sys.path:
  sys.path.insert(0,parentdir)

import xml.dom.minidom

info_dict = {'cont1_listening_from_ip': '192.168.56.1',
             'cont1_listening_from_port': 7999,
             'listen_conts_from_ip': '192.168.56.1',
             'listen_conts_from_port': 7998,
             'scher_virtual_src_ip':'10.0.0.255',
             'base_session_port':6000,
            }

def client(ip, port, message):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip, port))
  try:
      sock.sendall(message)
      print "scheduler: sent to_ip: {}, to_port: {}".format(ip,port)
      response = sock.recv(1024)
      print "scheduler: received: {}".format(response)
  finally:
      sock.close()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    data = self.request.recv(1024)
    job_res = json.loads(data)
    #get rid of unicode strings
    job_res = dict([(str(k), str(v)) for k, v in job_res.items()])
    cur_thread = threading.current_thread()
    
    session_id = int(job_res['session_id'].encode('ascii','ignore'))
    msg_type = job_res['type'].encode('ascii','ignore')
    res = job_res['response'].encode('ascii','ignore')
    print "SCHER rxed cur_thread:{}, job_res:{}".format(cur_thread.name, job_res)
    # update sessions_being_served_dict to show sch_job is done for session with session_num
    #print 'self.sessions_being_served_dict: '
    #pprint.pprint(self.sessions_being_served_dict)
    self.sessions_being_served_dict[session_id]['sch_job_done']=True
    sch_res = {'type':'sch_response',
               'response':"yes",#right now either qos is guaranteed or not at all,
               'session_id':session_id,
               'tp_dst':str(self.sessions_being_served_dict[session_id]['tp_dst'])
              }
    # !!! make sch_cont to send_sch_res
    Scheduler.event_chief.raise_event('sch_res_ready_to_be_sent',sch_res)
    response = "OK"
    self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

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
      args = ["Generic"] #[sch_res, "Generic"]
      self.raiseEvent(SchResReadyToBeSent(arg)) #sch_res
    elif event_type == 'tpr_rule_ready_to_be_sent':
      args = ["Generic"]
      self.raiseEvent(TprRuleReadyToBeSent(arg)) #tpr_rule
    else:
      print 'Unknown event_type: ', event_type
      raise KeyError('Unknown event_type')
#

is_scheduler_run = False
class Scheduler(object):
  event_chief = EventChief()
  def __init__(self, xml_network_number):
    if is_scheduler_run:
      self.HOST, self.PORT = '192.168.56.1', 6998
    else:
      self.HOST = info_dict['listen_conts_from_ip']
      self.PORT = info_dict['listen_conts_from_port']
      self.server = ThreadedTCPServer((self.HOST, self.PORT), ThreadedTCPRequestHandler)
      # Start a thread with the server -- that thread will then start one
      # more thread for each request
      self.server_thread = threading.Thread(target=self.server.serve_forever)
      # Exit the server thread when the main thread terminates
      self.server_thread.daemon = True
      self.server_thread.start()
      print "To listen SlaveConts, Server loop running in thread:", self.server_thread.name
      ###########################
    self.gm = GraphMan()
    if is_scheduler_run:
      #self.xml_parser = XMLParser("network_single_path.xml", str(xml_network_number))
      self.xml_parser = XMLParser("network_double_path.xml", str(xml_network_number))
      #self.xml_parser = XMLParser("network_double_path_with_random_redundancy_1.xml", str(xml_network_number))
    else:
      self.xml_parser = XMLParser("ext/network_single_path.xml", str(xml_network_number))
    self.init_network_from_xml()
    # Scher state dicts
    self.sessions_being_served_dict = {}
    self.sessions_pre_served_dict = {}
    self.sessionid_resources_dict = {}
    self.actual_res_dict = self.gm.give_actual_resource_dict()
    #for perf plotting
    self.perf_plotter = PerfPlotter(self.actual_res_dict)
    
  def print_scher_state(self):
    print '<-------------------H--------------------->'
    print 'is_scheduler_run: ', is_scheduler_run
    print 'sessions_being_served_dict:'
    pprint.pprint(self.sessions_being_served_dict)
    print 'sessions_pre_served_dict:'
    pprint.pprint(self.sessions_pre_served_dict)
    print '<-------------------E--------------------->'
    
  def welcome_session(self, sch_req_id, p_c_ip_list, p_c_gw_list, req_dict, app_pref_dict):
    """
    sch_req_id: should be unique for every sch_session
    """
    #update global list and dicts
    session_tp_dst = info_dict['base_session_port'] #len(self.sessions_being_served_dict) + info_dict['base_session_port']
    self.sessions_being_served_dict.update(
      {sch_req_id:{'tp_dst':session_tp_dst,
                   'req_dict':req_dict,
                   'p_c_ip_list':p_c_ip_list,
                   'p_c_gw_list':p_c_gw_list,
                   'app_pref_dict': app_pref_dict,
                   'sch_job_done':False }
      }
    )
    #print 'self.sessions_being_served_dict: '
    #pprint.pprint(self.sessions_being_served_dict)
  
  def do_sching(self):
    '''
    For currently active sessions, get things together to work sching logic and
    then corresponding rules to correspoding actuator (which is a single controller 
    right now !)
    '''
    session_res_alloc_dict = self.allocate_resources()
    print '---------------SCHING STARTED---------------'
    print 'session_res_alloc_dict:'
    pprint.pprint(session_res_alloc_dict)
    self.perf_plotter.save_sching_result(session_res_alloc_dict['s-wise'], 
                                         session_res_alloc_dict['res-wise'])
    #Convert sching decs to rules
    def walkbundle_to_walk(shortest_path, walkbundle):
      walk = shortest_path
      for itr in walkbundle: #walkbundle is assumed to consist only itrs (currently - may change)
        itr_id = self.actual_res_dict['res_id_map'][itr]
        conn_sw = self.actual_res_dict['id_info_map'][itr_id]['conn_sw']
        #
        lasti_conn_sw = len(walk) - walk[::-1].index(conn_sw) - 1
        walk.insert(lasti_conn_sw+1, itr)
        walk.insert(lasti_conn_sw+2, conn_sw)
      return walk
    #
    """
    for s_id in self.sessions_being_served_dict:
      shortest_path = self.sessionid_resources_dict[s_id]['shortest_path']
      walk_bundle = session_res_alloc_dict['s-wise'][s_id]['walk_bundle']
      walk = walkbundle_to_walk(shortest_path, walk_bundle)
      print "session_%d_walk: %s" %(s_id, walk)
      '''
      session_walk_and_tpr_rule = self.form_walkandtpr_rule_from_walk(
        self.sessions_being_served_dict[sch_req_id]['tp_dst'],
        p_c_ip_list,
        sch_path_dict['path'],
        req_dict
      )
      '''
      '''
      self.sessions_being_served_dict.update(
        {sch_req_id:{'tp_dst':session_tp_dst,
                     'req_dict':req_dict,
                     'p_c_ip_list':p_c_ip_list,
                     'p_c_gw_list':p_c_gw_list,
                     'app_pref_dict': app_pref_dict,
                     'sch_job_done':False }
        }
        
      
      path_rule = path_and_tpr_rule['path_rule']
      tpr_rule = path_and_tpr_rule['tpr_rule']
      Scheduler.event_chief.raise_event('tpr_rule_ready_to_be_sent',tpr_rule)
      #print 'path_rule: '
      #pprint.pprint(path_rule)
      #rule: from json to xml
      xml_path_rule = self.form_xml_path_rule(sch_req_id, path_rule)
      #print 'xml_path_rule: \n', (xml.dom.minidom.parseString(xml_path_rule)).toprettyxml()
      #Right now sching decs for all sessions will be driven by one controller.
      #TODO: In the future, if seen necessary total work needs to be distributed
      #over multiple controllers (may be geography-aware, power-aware ... way)
      client(info_dict['cont1_listening_from_ip'],
             info_dict['cont1_listening_from_port'], xml_path_rule)
      '''
    """
  def bye_session(self, sch_req_id):
    # Send sessions whose "sching job" is done is sent to pre_served category
    self.sessions_pre_served_dict.update(
    {sch_req_id: self.sessions_being_served_dict[sch_req_id]})
    del self.sessions_being_served_dict[sch_req_id]
    
  def update_sessionid_resources_dict(self):
    """
    Network resources will be only the ones on the session_shortest path.
    It resources need to lie on the session_shortest path.
    """
    #TODO: sessions whose resources are already specified no need for putting them in the loop
    for s_id in self.sessions_being_served_dict:
      p_c_gw_list = self.sessions_being_served_dict[s_id]['p_c_gw_list']
      s_all_paths = self.gm.give_all_paths(p_c_gw_list[0], p_c_gw_list[1])
      for p in s_all_paths:
        p_net_edge_list = self.gm.pathlist_to_netedgelist(p)
        p_itres_list = self.gm.give_itreslist_on_path(p)
        if not (s_id in self.sessionid_resources_dict):
          self.sessionid_resources_dict[s_id] = {'s_info':{}, 'ps_info':[]}
        self.sessionid_resources_dict[s_id]['ps_info'].append(
          {'path': p,
           'net_edge_list': p_net_edge_list,
           'itres_list': p_itres_list
          })
      
  def allocate_resources(self):
    '''
    returns (session_res_alloc_dict, session_walk_bundles_dict)
    '''
    self.update_sessionid_resources_dict()
    sching_opter = SchingOptimizer(self.sessions_being_served_dict,
                                   self.actual_res_dict,
                                   self.sessionid_resources_dict
                                  )
    sching_opter.solve()
    #
    return sching_opter.get_sching_result()
  
  def sch_path(self, sch_req_id, p_c_ip_list, req_dict):
    ###################################################
    #sch_path_dict = self.gm.sch_path(sch_req_id, req_dict)
    ###################################################
    if sch_path_dict == None:
      #send NACK to p !!!
      return
    #
    path_and_tpr_rule = self.form_walkandtpr_rule_from_walk(session_tp_dst,
                                                      p_c_ip_list, 
                                                      sch_path_dict['path'],
                                                      req_dict)
    path_rule = path_and_tpr_rule['path_rule']
    tpr_rule = path_and_tpr_rule['tpr_rule']
    Scheduler.event_chief.raise_event('tpr_rule_ready_to_be_sent',tpr_rule)
    #print 'path_rule: '
    #pprint.pprint(path_rule)
    #rule: from json to xml
    xml_path_rule = self.form_xml_path_rule(sch_req_id, path_rule)
    #print 'xml_path_rule: \n', (xml.dom.minidom.parseString(xml_path_rule)).toprettyxml()
    #########################
    #Send the sch_job_msg to corresponding transit_session controller
    #PS: Right now there is only one controller responsible for all the sessions
    #cont1_ip&l_port = '192.168.56.1', 9999
    client(info_dict['cont1_listening_from_ip'],
           info_dict['cont1_listening_from_port'], xml_path_rule)
    print '--------------------------------------------'
  """
  def give_dpid_of_tpr_sw(self, tpr_name):
    tpr_sw_name = self.gm.give_tpr_sw_name(tpr_name)
    tpr_sw = self.gm.get_node(tpr_sw_name)
    if tpr_sw['type'] == 'sw':
      return tpr_sw['dpid']
    else:
      print "tpr_sw is not SW !!!"
      raise KeyError('Wrong tpr_sw')
  """
  def form_walkandtpr_rule_from_walk(self,session_tp_dst,p_c_ip_list,path,f_Dp_map):
    tpr_rule_dict = {}
    tpr_rule_counter = 0
    #
    path_rule = []
    cur_from_ip = p_c_ip_list[0]
    cur_to_ip = p_c_ip_list[1]
    duration = 50
    cur_node_str = None
    for i,node_str in list(enumerate(path)):#node = next_hop
      if i == 0: 
        cur_node_str = node_str
        continue
      cur_node = self.gm.get_node(cur_node_str)
      if cur_node['type'] == 't':
        cur_node_str = node_str
        continue
      
      node = self.gm.get_node(node_str)
      edge = self.gm.get_edge(cur_node_str, node_str)
      if node['type'] == 't': #sw-t
        path_rule.append({'conn':[cur_node['dpid'],cur_from_ip],
                          'typ':'modify_forward',
                          'wc':[cur_from_ip,cur_to_ip,int(session_tp_dst)],
                          'rule':[node['ip'],node['mac'],edge['pre_dev'],duration]
                         })
        """
        By assuming the func_list is distributed over the sched_tprs respective
        to the order.
        """
        if not (cur_node['dpid'] in tpr_rule_dict):
          tpr_rule_dict[cur_node['dpid']] = [{
          'tpr_ip':node['ip'],
          'tpr_mac':node['mac'],
          'swdev_to_tpr':edge['pre_dev'],
          'assigned_job':req_dict['func_list'][tpr_rule_counter],
          'session_tp': int(session_tp_dst),
          'consumer_ip': cur_to_ip.toStr()
          }]
        else:
          tpr_rule_dict[cur_node['dpid']].append({
          'tpr_ip':node['ip'],
          'tpr_mac':node['mac'],
          'swdev_to_tpr':edge['pre_dev'],
          'assigned_job':req_dict['func_list'][tpr_rule_counter],
          'session_tp': int(session_tp_dst),
          'consumer_ip': cur_to_ip.toStr()
           })
        tpr_rule_counter = tpr_rule_counter + 1
        cur_from_ip = node['ip']
      elif node['type'] == 'sw': #sw-sw
        path_rule.append({'conn':[cur_node['dpid'],cur_from_ip],
                          'typ':'forward',
                          'wc':[cur_from_ip,cur_to_ip,int(session_tp_dst)],
                          'rule':[edge['pre_dev'], duration]
                         })
        #for reverse path: to deliver sch_response to src
        path_rule.append({'conn':[node['dpid'],info_dict['scher_virtual_src_ip']],
                          'typ':'forward',
                          'wc':[info_dict['scher_virtual_src_ip'],p_c_ip_list[0]],
                          'rule':[edge['post_dev'], duration]
                         })
      else:
        raise KeyError('Unknown node_type')
      cur_node_str = node_str
    #default rule to forward packet to consumer
    path_rule.append({'conn':[12,cur_from_ip],
                      'typ':'forward',
                      'wc':[cur_from_ip,cur_to_ip,int(session_tp_dst)],
                      'rule':['s12-eth3',duration]
                      })
    #default rule to forward sch_response to producer
    """
    path_rule.append({'conn':[11,info_dict['scher_virtual_src_ip']],
                      'typ':'forward',
                      'wc':[info_dict['scher_virtual_src_ip'],p_c_ip_list[0]],
                      'rule':['s11-eth1',duration]
                      })
    """
    return {'path_rule':path_rule, 'tpr_rule':tpr_rule_dict}

  def form_xml_single_rule(self, rule):
    dpid, from_ip = rule['conn'][0], rule['conn'][1]
    typ = rule['typ']
    src_ip, dst_ip = rule['wc'][0], rule['wc'][1]
    no_tp_dst = False
    tp_dst = None
    try:
      tp_dst = rule['wc'][2]
    except (IndexError):
      no_tp_dst = True
      pass
      
    xml_rule = '<connection dpid="{}" from="{}">'.format(dpid, from_ip)
    xml_rule = xml_rule + '<type>{}</type>'.format(typ)
    if no_tp_dst:
      xml_rule = xml_rule + \
      '<wildcards src_ip="{}" dst_ip="{}"/>'.format(src_ip, dst_ip)
    else:
      xml_rule = xml_rule + \
      '<wildcards src_ip="{}" dst_ip="{}" tp_dst="{}"/>'.format(src_ip, dst_ip, tp_dst)
    if typ == 'forward':
      xml_rule = xml_rule + \
      '<rule fport="{}" duration="{}"/>'.format(rule['rule'][0],rule['rule'][1])
    elif typ == 'modify_forward':
      xml_rule = xml_rule + \
      '<rule new_dst_ip="{}" new_dst_mac="{}" fport="{}" duration="{}"/>'.format(rule['rule'][0],
      rule['rule'][1], rule['rule'][2], rule['rule'][3])
    xml_rule = xml_rule + '</connection>'
    return xml_rule
  
  def form_xml_path_rule(self, session_num, path_rule):
    xml_path_rule = '<scheduling>'
    xml_path_rule = xml_path_rule + '<session number="{}">'.format(session_num)
    for rule in path_rule:
      xml_path_rule = xml_path_rule + self.form_xml_single_rule(rule)
      
    xml_path_rule = xml_path_rule + '</session>'
    xml_path_rule = xml_path_rule + '</scheduling>'
    return xml_path_rule
    
  def send_to_controller(self, ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
      sock.sendall(message)
      response = sock.recv(1024)
      print "Received: {}".format(response)
    finally:
      sock.close()
      
  def init_network_from_xml(self):
    node_edge_lst = self.xml_parser.give_node_and_edge_list_from_xml()
    #print 'node_lst:'
    #pprint.pprint(node_edge_lst['node_lst'])
    #print 'edge_lst:'
    #pprint.pprint(node_edge_lst['edge_lst'])
    self.gm.graph_add_nodes(node_edge_lst['node_lst'])
    self.gm.graph_add_edges(node_edge_lst['edge_lst'])
    
  def test(self):
    # 0: Tight
    # 1: Dataflow
    num_session = 3
    '''
    sr1:
      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']}
      {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0}
    '''
    '''
    {'data_amount':2, 'slack_metric':60, 'func_list':['f1', 'f2']},
    {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
    {'data_amount':0.1, 'slack_metric':4, 'func_list':['f1']},
    '''
    req_dict_list = [ {'data_amount':1, 'slack_metric':15, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
                      {'data_amount':1, 'slack_metric':24, 'func_list':['f1','f2','f3']},
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
    {'m_p': 1,'m_u': 10,'x_p': 0.02,'x_u': 0.02},
    """
    app_pref_dict_list = [
                          {'m_p': 10,'m_u': 0.1,'x_p': 0,'x_u': 0},
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
    p_c_ip_list_list = [
                        ['10.0.0.2','10.0.0.1'],
                       ]
    p_c_gw_list_list = [
                        ['s11', 's12'],
                       ]
    for i in range(0, num_session):
      self.welcome_session(i, p_c_ip_list_list[0], p_c_gw_list_list[0],
                           req_dict_list[i], app_pref_dict_list[i] )
    """
    (session_res_alloc_dict, session_walk_bundles_dict) = self.allocate_resources()
    print 'session_res_alloc_dict:'
    pprint.pprint(session_res_alloc_dict)
    print 'session_walk_bundles_dict:'
    pprint.pprint(session_walk_bundles_dict)
    self.perf_plotter.save_sching_result(session_res_alloc_dict['s-wise'], 
                                         session_res_alloc_dict['res-wise'])
    """
    self.do_sching()
    #self.print_scher_state()
    #self.bye_session(0)
    #self.print_scher_state()
    
def main():
  global is_scheduler_run
  is_scheduler_run = True
  sch = Scheduler(1)
  
  sch.test()
  
  """
  rule = {'conn':[11,'10.0.0.2'],'typ':'forward','wc':['10.0.0.2','10.0.0.1'],'rule':[2,50]}
  #print 'xml_rule: ', sch.form_xml_single_rule(rule)
  
  path_rule = [
  {'conn':[11,'10.0.0.2'],'typ':'forward','wc':['10.0.0.2','10.0.0.1'],'rule':[2,50]},
  {'conn':[1,'10.0.0.2'],'typ':'modify_forward','wc':['10.0.0.2','10.0.0.1'],
  'rule':['10.0.0.11','00:00:00:00:01:01',4,50]},
  {'conn':[1,'10.0.0.11'],'typ':'forward','wc':['10.0.0.11','10.0.0.21'],'rule':[2,50]},
  {'conn':[2,'10.0.0.21'],'typ':'forward','wc':['10.0.0.21','10.0.0.1'],'rule':[4,50]},
  {'conn':[12,'10.0.0.21'],'typ':'forward','wc':['10.0.0.21','10.0.0.1'],'rule':[3,50]},
  ]
  xml_path_rule = sch.form_xml_path_rule(1, path_rule)
  #print 'xml_path_rule: ', xml_path_rule
  #sch.send_to_controller('192.168.56.1', 9999, xml_path_rule)
  """
  raw_input('Enter')
  #server.shutdown()


if __name__ == "__main__":
  main()
  
  """
  def initial_network_formation(self):
    lw_p_capacity = {'p_index':0.05, 'session':[]}
    mw_p_capacity = {'p_index':0.03, 'session':[]}
    hw_p_capacity = {'p_index':0.01, 'session':[]}
    self.gm.graph_add_nodes([
    ['s11',{'type':'sw', 'out_bw':0, 'in_bw':0}],
    ['s1',{'type':'sw', 'out_bw':0, 'in_bw':0}],
    ['s2',{'type':'sw', 'out_bw':0, 'in_bw':0}],
    ['s3',{'type':'sw', 'out_bw':0, 'in_bw':0}],
    ['s4',{'type':'sw', 'out_bw':0, 'in_bw':0}],
    ['s12',{'type':'sw', 'out_bw':0, 'in_bw':0}],
    ['t11',{'type':'t','ip':'10.0.0.11'},hw_p_capacity],
    ['t12',{'type':'t','ip':'10.0.0.12'},mw_p_capacity],
    ['t13',{'type':'t','ip':'10.0.0.13'},lw_p_capacity],
    ['t21',{'type':'t','ip':'10.0.0.21'},hw_p_capacity],
    ['t22',{'type':'t','ip':'10.0.0.22'},mw_p_capacity],
    ['t23',{'type':'t','ip':'10.0.0.23'},lw_p_capacity],
    ['t31',{'type':'t','ip':'10.0.0.31'},hw_p_capacity],
    ['t32',{'type':'t','ip':'10.0.0.32'},mw_p_capacity],
    ['t33',{'type':'t','ip':'10.0.0.33'},lw_p_capacity],
    ['t41',{'type':'t','ip':'10.0.0.41'},hw_p_capacity],
    ['t42',{'type':'t','ip':'10.0.0.42'},mw_p_capacity],
    ['t43',{'type':'t','ip':'10.0.0.43'},lw_p_capacity]
    ])
    
    local_link = {'bw':10, 'delay':'5', 'loss':0, 'max_queue_size':1000}
    wide_area_link = {'bw':10, 'delay':'50', 'loss':0, 'max_queue_size':1000}
    isa_link = {'bw':1000, 'delay':'1', 'loss':0, 'max_queue_size':10000}
    self.gm.graph_add_edges([
    ['s11','s1',{'pre_dev':'s11-eth2','post_dev':'s1-eth1','session':[]},local_link],
    ['s11','s3',{'pre_dev':'s11-eth3','post_dev':'s3-eth1','session':[]},local_link],
    ['s1','s2',{'pre_dev':'s1-eth2','post_dev':'s2-eth1','session':[]},local_link],
    ['s3','s4',{'pre_dev':'s3-eth2','post_dev':'s4-eth1','session':[]},local_link],
    ['s2','s12',{'pre_dev':'s2-eth2','post_dev':'s12-eth1','session':[]},local_link],
    ['s4','s12',{'pre_dev':'s4-eth2','post_dev':'s12-eth2','session':[]},local_link],
    ['s1','s4',{'pre_dev':'s1-eth3','post_dev':'s4-eth3','session':[]},local_link],
    ['s3','s2',{'pre_dev':'s3-eth3','post_dev':'s2-eth3','session':[]},local_link],
    ['s1','t11',{'pre_dev':'s1-eth4','post_dev':'t11-eth0','session':[]},isa_link],
    ['s1','t12',{'pre_dev':'s1-eth5','post_dev':'t12-eth0','session':[]},isa_link],
    ['s1','t13',{'pre_dev':'s1-eth6','post_dev':'t13-eth0','session':[]},isa_link],
    ['s2','t21',{'pre_dev':'s2-eth4','post_dev':'t21-eth0','session':[]},isa_link],
    ['s2','t22',{'pre_dev':'s2-eth5','post_dev':'t22-eth0','session':[]},isa_link],
    ['s2','t23',{'pre_dev':'s2-eth6','post_dev':'t23-eth0','session':[]},isa_link],
    ['s3','t31',{'pre_dev':'s3-eth4','post_dev':'t31-eth0','session':[]},isa_link],
    ['s3','t32',{'pre_dev':'s3-eth5','post_dev':'t32-eth0','session':[]},isa_link],
    ['s3','t33',{'pre_dev':'s3-eth6','post_dev':'t32-eth0','session':[]},isa_link],
    ['s4','t41',{'pre_dev':'s4-eth4','post_dev':'t41-eth0','session':[]},isa_link],
    ['s4','t42',{'pre_dev':'s4-eth5','post_dev':'t42-eth0','session':[]},isa_link],
    ['s4','t43',{'pre_dev':'s4-eth6','post_dev':'t43-eth0','session':[]},isa_link]
    ])
  """
