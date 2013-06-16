import socket
import threading
import SocketServer, json
from netsensor import NetworkSensor
import networkx as nx
import pprint
import itertools

ifi_map = {}
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
      global ifi_map
      data = self.request.recv(1024)
      ifi_map = json.loads(data)
      cur_thread = threading.current_thread()
      #response = "{}: {}".format(cur_thread.name, data)
      response = "OK"
      self.request.sendall(response)
      print 'ifi_map: ', ifi_map

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

# used to adjust computational time difference between diff functions
func_tcomplexity_dict = {
'f1':1.1, 'f2':1.2, 'f3':1.3, 
'f4':1.4, 'f5':1.5, 'f6':1.6
}
# to keep currently served sessions
# session_number:{'data_amount':, 'slack_metric':, 'start_time': }
session_served_dict = {}

class GraphMan(object):
  def __init__(self):
    self.g = nx.Graph()
  
  def sch_path(self, qos_dict):
    """
    For now: Will assume 
    * All sch request is made to allocate a path between 1 gw-pair(s11-s12)
    * Resource Allocation will be based on FIFO
    * P resources will be allocated over the possible network paths
    * EVERY P resource can run ANY requested computation
    * Best-effort. Only criterion is to increase data quality.
      If delivering data is impossible, ISA will return NACK.
      Data will only be delivered even if no chance for data quality increase due to 
      - strict slack_metric
      - no available transit resource
    * Every P resource can serve for one session only at a time
    * No data amount increase introduced by the transit computations
    -> Initially
    * LINEAR comp_time vs. data_amount relation
    * STATIC scheduling scheme
    qos_dict: {'data_amount(Gb)':, 'slack_metric(ms)':, 'func_list':{}}
    """
    #update global list and dicts
    session_number = len(session_served_dict) + 1
    session_served_dict.update({session_number:qos_dict})
    
    best_path_comb = self.give_best_path_comb(qos_dict)
    print 'best_path_comb: '
    pprint.pprint(best_path_comb)
    
    return best_path_comb
    
  def give_best_path_comb(self, req_dict):
    """
    Will give the best path. Metric for comparison is del_time. The less, the better.
    req_dict: {'data_amount(Gb)':,'slack_metric(ms)':, 'func_list':[]}
    """
    data_amount = req_dict['data_amount']
    slack_metric = req_dict['slack_metric']
    func_list = req_dict['func_list']
    best_path_comb = {'total_cost':float('Inf'),'path_del_cost':float('Inf'),
                      'comp_cost':float('Inf'),'path':None,'path_avcap':None,
                      't_comb':None}
    for path in nx.all_simple_paths(self.g, source='s11', target='s12'):
      path_avcap = self.find_path_avcap(path)
      del_time = float(path_avcap['latency']) + \
                 float(data_amount)*(1+float(path_avcap['loss']))/float(path_avcap['bw']) * \
                 len(path)*2
      #print 'del_time: ', del_time
      if del_time > float(slack_metric):
        continue
      #######################################################################
      """
      P resource alloc needs also be done in this method while considering all
      the possible paths. Procedure:
      * Find all possible available p resources on the path
      * Alloc p resources to maximize the quality of data
        - slack_metric is the constraint (computational_time = p_index(0-1) * data_amount(Gb))
        - order of processing done by given functions MATTERS
        - try to decrease contention at the intermediate SA sws i.e. i.e. out_bw - in_bw
        - available p capacity at each AS i.e. total p_index of available p resources
          in an AS
      """
      node_dict = dict(self.g.nodes(data=True))
      #n_nbrs_dict = {(n if n in t_path else -1):(nbrs if n in t_path else -1) \
      #                for n,nbrs in self.g.adjacency_list()}
      pr_on_path_dict = {}
      #print 'path: ', path
      num_pr_on_path = 0
      for sw in path:
        sw_pr_dict = {node:node_dict[node] for node in node_dict \
                      if (node in self.g.neighbors(sw) and \
                          node_dict[node]['type'] == 't' and \
                          len(node_dict[node]['session']) == 0 )}
        if len(sw_pr_dict) != 0:
          for pr,attr in sw_pr_dict.items():
            pr_on_path_dict[pr] = attr
          num_pr_on_path = num_pr_on_path + len(sw_pr_dict)
          
      #pprint.pprint(pr_on_path_dict)
      
      len_func_list = len(func_list)
      alloc_pr_num = len_func_list if (num_pr_on_path > len_func_list) else num_pr_on_path
      #######################################################################
      def trans_to_ordered_comb(all_combs): #comb is tuple of prs
        for comb in all_combs:
          order_index_list = []
          orderindex_pr_dict = {}
          for pr in comb:
            sa_sw = self.g.neighbors(pr)[0] # each pr is connected to only one sa_sw
            order_index = path.index(sa_sw)
            order_index_list.append(order_index)
            if not (order_index in orderindex_pr_dict):
              orderindex_pr_dict[order_index] = []
            orderindex_pr_dict[order_index].append(pr)
          if order_index_list == sorted(order_index_list):
            continue
          #print 'comb: ', comb, 'order_index_list: ', order_index_list
          order_index_list = list(set(order_index_list)) #to remove the duplicate indexes
          ordered_comb = [pr for i in order_index_list for pr in orderindex_pr_dict[i]]
          all_combs.remove(comb)
          all_combs.append(ordered_comb)
          #print 'ordered_comb: ', ordered_comb
      all_combs = list(itertools.combinations(pr_on_path_dict, r=alloc_pr_num))
      trans_to_ordered_comb(all_combs)
      #######################################################################
      def comb_cost_calc(all_combs):
        """
        Calculate total time for data trans, prop and computation in SAs
        - trans = data_amount / link_bw
        - comp_time = data_amount*p_index*func_t_complexity
        """
        comb_cost_list = []
        for comb in all_combs:
          comb_trans_time = 0
          comb_prop_time = 0
          comb_comp_time = 0
          fl_counter = 0
          for pr in comb:
            link_tuple = list(self.g[pr].iteritems())[0]   #always one entity !
            
            comb_trans_time = comb_trans_time + \
                              4*float(data_amount) / float(link_tuple[1]['bw'])
            comb_prop_time = comb_prop_time + 2*float(link_tuple[1]['delay'])
            comb_comp_time = comb_comp_time + float(data_amount) * \
                             float(pr_on_path_dict[pr]['p_index']) * \
                             func_tcomplexity_dict[func_list[fl_counter]]
            fl_counter = fl_counter + 1
            comb_total_cost = comb_trans_time + comb_prop_time + comb_comp_time
          comb_cost_list.append((comb, {'comb_trans_time':comb_trans_time,
                                        'comb_prop_time':comb_prop_time,
                                        'comb_comp_time':comb_comp_time,
                                        'comb_total_cost':comb_total_cost
                                       }
                               ))
        return comb_cost_list
      comb_cost_list = comb_cost_calc(all_combs)
      #pprint.pprint(comb_cost_list)
      def find_min_total_cost_comb(comb_cost_list):
        min_total_cost = float('Inf')
        min_total_cost_comb = None
        for comb_costmap in comb_cost_list:
          comb_total_cost = comb_costmap[1]['comb_total_cost']
          if comb_total_cost < min_total_cost:
            min_total_cost = comb_total_cost
            min_total_cost_comb = comb_costmap[0]
        return [min_total_cost_comb, {'comb_total_cost':min_total_cost}]
      mincost_comb_cost_list = find_min_total_cost_comb(comb_cost_list)
      comp_time = mincost_comb_cost_list[1]['comb_total_cost']
      best_comb = mincost_comb_cost_list[0]
      #pprint.pprint(mincost_comb_cost_list)
      #print '-------------------'
      #######################################################################
      #del_cost + min_comp_cost
      total_cost = del_time + comp_time
      if total_cost > float(slack_metric):
        continue
      if total_cost < best_path_comb['total_cost']:
          best_path_comb['total_cost'] = total_cost
          best_path_comb['path_del_cost'] = del_time
          best_path_comb['comp_cost'] = comp_time
          best_path_comb['path'] = path
          best_path_comb['path_avcap'] = path_avcap
          best_path_comb['t_comb'] = best_comb
      
    return best_path_comb
    
  def find_path_avcap(self, path):
    """
    Finds and returns the link bw with least in the path.
    path is the list of overlaying nodes.
    """
    path_bw = float('Inf')
    path_latency = 0
    path_success = 1.0
    for j, node in enumerate(path):
      if j == 0: continue
      i = j - 1
      # Simply assume that link bw is shared between the served sessions equally
      link_bw = float(self.g[path[i]][path[j]]['bw']) / (len(self.g[path[i]][path[j]]['session'])+1)
      path_latency = path_latency + int(self.g[path[i]][path[j]]['delay'])
      path_success = path_success*(1-float(self.g[path[i]][path[j]]['loss']))
      
      if link_bw < path_bw:
        path_bw = link_bw
    path_loss = 1 - path_success
    #'bw', 'delay', 'loss'
    return {'bw':path_bw, 'latency':path_latency, 'loss':path_loss}
  
  def graph_add_nodes(self, nodes):
    for node in nodes:
      if node[1]['type'] == 'sw':
        self.g.add_node(node[0], node[1] )
      elif node[1]['type'] == 't':
        self.g.add_node(node[0], dict(node[1].items() + node[2].items() ))
  
  def graph_add_edges(self, edges):
    for edge in edges:
      self.g.add_edge(edge[0],edge[1],dict(edge[2].items() + edge[3].items() ))
    
  def print_graph(self):
    print '# of nodes: ', self.g.number_of_nodes()
    print '# of edges: ', self.g.number_of_edges()
    print 'nodes: ', self.g.nodes()
    print 'edges: ', self.g.edges()
    print 'node overview:'
    pprint.pprint(self.g.nodes(data=True))
    print 'edge overview:'
    pprint.pprint(self.g.edges(data=True))
    """
    for n,nbrs in self.g.adjacency_iter():
      for nbr,eattr in nbrs.items():
        #print 'eattr: ', eattr
        try:
          data=eattr['pre_dev']
          print('(<%s-%s> , <%s-%s> , bw:%s, delay:%s, loss:%s, max_queue_size:%s)'
          % (n,nbr,eattr['pre_dev'],eattr['post_dev'],eattr['bw'],eattr['delay'],
          eattr['loss'],eattr['max_queue_size']))
        except KeyError:
          pass
    """

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
         
class Scheduler(object):
  def __init__(self):
    self.HOST, self.PORT = '192.168.56.1', 9998 #socket.gethostbyname(socket.gethostname())
    self.server = ThreadedTCPServer((self.HOST, self.PORT), ThreadedTCPRequestHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    # Exit the server thread when the main thread terminates
    self.server_thread.daemon = True
    self.server_thread.start()
    print "To listen NetSensor, Server loop running in thread:", self.server_thread.name
    self.gm = GraphMan()
    self.xml_parser = XMLParser("network.xml", "1")
    self.init_network_from_xml()
    #self.gm.print_graph()
    
  def form_xml_single_rule(self, rule):
    dpid, from_ip = rule['conn'][0], rule['conn'][1]
    typ = rule['typ']
    src_ip, dst_ip = rule['wc'][0], rule['wc'][1]
    
    xml_rule = '<connection dpid="{}" from="{}">'.format(dpid, from_ip)
    xml_rule = xml_rule + '<type>{}</type>'.format(typ)
    xml_rule = xml_rule + '<wildcards src_ip="{}" dst_ip="{}"/>'.format(src_ip, dst_ip)
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
  def sch_path(self, qos_dict):
    self.gm.sch_path(qos_dict)
  
  def init_network_from_xml(self):
    node_edge_lst = self.xml_parser.give_node_and_edge_list_from_xml()
    #print 'node_lst:'
    #pprint.pprint(node_edge_lst['node_lst'])
    #print 'edge_lst:'
    #pprint.pprint(node_edge_lst['edge_lst'])
    self.gm.graph_add_nodes(node_edge_lst['node_lst'])
    self.gm.graph_add_edges(node_edge_lst['edge_lst'])
    
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class XMLParser(object):
  def __init__(self, xmlfile_url, network_number):
    self.network_number = network_number
    self.xmlfile_url=xmlfile_url
    self.tree = ET.parse(xmlfile_url)
    #self.node_tree = self.tree.getiterator('node')
    self.root = self.tree.getroot()
    
  def give_node_and_edge_list_from_xml(self):
    node_lst = []
    edge_lst = []
    for network in self.root:
      if network.get('number') == self.network_number:
        nodes = network.find('nodes')
        for node in nodes:
          node_type = node.get('type')
          if node_type == 'sw':
            node_lst.append([node.tag, 
                            {'type':node_type,'out_bw':node.get('out_bw'),
                            'in_bw':node.get('in_bw')}
                            ])
          elif node_type == 't':
            node_lst.append([node.tag, 
                            {'type':node_type,'ip':node.get('ip')},
                            {'p_index':node.get('p_index'),'session':[]}
                            ])
          else:
            raise KeyError('Unknown node_type')
        edges = network.find('edges')
        for edge in edges:
          dev = edge.find('dev')
          session = edge.find('session')
          lc = edge.find('link_cap')
          edge_lst.append([edge.get('pre_node'),edge.get('post_node'),
                           {'pre_dev':dev.get('pre_dev'), 
                            'post_dev':dev.get('post_dev'),'session':[]},
                           {'bw':lc.get('bw'),'delay':lc.get('delay'),
                            'loss':lc.get('loss'),
                            'max_queue_size':lc.get('max_queue_size')}
                          ])
    return {'node_lst':node_lst,'edge_lst':edge_lst}
          
def main():
  sch = Scheduler()
  qos_dict = {'data_amount':0.01, 'slack_metric':24, 'func_list':['f1','f2','f3']  }
  sch.sch_path(qos_dict)
  
  
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
