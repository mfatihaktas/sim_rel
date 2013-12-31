#!/usr/bin/python

import sys,logging,getopt,commands,pprint
import SocketServer,threading,time,socket
from errors import CommandLineOptionError,NoItruleMatchError
from control_comm_intf import ControlCommIntf

def get_addr(lintf):
  # search and bind to eth0 ip address
  intf_list = commands.getoutput("ifconfig -a | sed 's/[ \t].*//;/^$/d'").split('\n')
  intf_eth0 = None
  for intf in intf_list:
    if lintf in intf:
      intf_eth0 = intf
  intf_eth0_ip = commands.getoutput("ip address show dev " + intf_eth0).split()
  intf_eth0_ip = intf_eth0_ip[intf_eth0_ip.index('inet') + 1].split('/')[0]
  return intf_eth0_ip
##########################  UDP Server-Handler  ################################
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
  def __init__(self, call_back, server_addr, RequestHandlerClass):
    SocketServer.UDPServer.__init__(self, server_addr, RequestHandlerClass)
    self.call_back = call_back
  
class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    cur_thread = threading.current_thread()
    #socket = self.request[1]
    server = self.server
    data = self.request[0].strip()
    s_tp_dst = int(server.server_address[1])
    logging.info('cur_thread=%s; s_tp_dst=%s, recv_data_size=%sbs', cur_thread.name, s_tp_dst, 8*sys.getsizeof(data))
    #
    server.call_back(s_tp_dst, data)
  
#############################  Class Transit  ##################################
class Transit(object):
  def __init__(self, nodename, tl_ip, tl_port, dtsl_ip, dtsl_port):
    self.nodename = nodename
    self.tl_ip = tl_ip
    self.tl_port = tl_port
    self.dtsl_ip = dtsl_ip
    self.dtsl_port = dtsl_port
    #
    self.s_info_dict = {}
    #for control comm
    self.cci = ControlCommIntf()
    self.cci.reg_commpair(sctag = 't-dts',
                          proto = 'udp',
                          _recv_callback = self._handle_recvfromdts,
                          s_addr = (self.tl_ip,self.tl_port),
                          c_addr = (self.dtsl_ip,self.dtsl_port) )
    #
    self.session_soft_state_span = 1000
    s_soft_expire_timer = threading.Timer(self.session_soft_state_span,
                                          self._handle_SessionSoftTimerExpire)
    s_soft_expire_timer.daemon = True
    s_soft_expire_timer.start()
    #
    logging.info('%s is ready...', self.nodename)
  
  def _handle_SessionSoftTimerExpire(self):
    while True:
      logging.info('_handle_SessionSoftTimerExpire;')
      #print 's_info_dict:'
      #pprint.pprint(s_info_dict )
      for s_tp_dst, s_info in self.s_info_dict.items():
        inactive_time_span = time.time() - s_info['s_active_last_time']
        if inactive_time_span >= self.session_soft_state_span: #soft state expire
          s_info['s_server'].shutdown()
          s_info['s_sock'].close()
          del self.s_info_dict[s_tp_dst]
          logging.info('inactive_time_span=%s\ns with tp_dst:%s is soft-expired.',inactive_time_span,s_tp_dst)
      #
      logging.info('------')
      # do every ... secs
      time.sleep(self.session_soft_state_span)
  
  ##########################  handle dts_comm  #################################
  def _handle_recvfromdts(self, msg):
    #msg = [type_, data_]
    [type_, data_] = msg
    if type_ == 'itjob_rule':
      self.welcome_s(data_)
  
  def welcome_s(self, data_):
    #If new_s with same tpdst arrives, old_s is overwritten by new_s
    stpdst = int(data_['s_tp'])
    if stpdst in self.s_info_dict:
      self.bye_s(stpdst)
    #updating global dicts
    del data_['s_tp']
    jobtobedone = {ftag:1000*data_['datasize']*comp/func_comp_dict[ftag] \
                     for ftag,comp in data_['itfunc_dict'].items()}
    data_.update( {'jobtobedone': jobtobedone} )
    #calc est_prot
    est_proct = proc_time_model(datasize = float(data_['datasize']),
                                func_comp = float(data_['comp']),
                                proc_cap = float(data_['proc']))
    #
    self.s_info_dict[stpdst] = {'itjobrule':data_,
                                's_server':self.create_s_server(stpdst),
                                's_sock':self.create_s_sock(),
                                's_active_last_time':time.time(),
                                'est_proct': est_proct }
    #
    logging.info('welcome new_s; tpdst=%s, s_info=\n%s', stpdst, pprint.pformat(self.s_info_dict[stpdst]))
  
  def bye_s(self, stpdst):
    self.s_info_dict[stpdst]['s_server'].shutdown()
    self.s_info_dict[stpdst]['s_sock'].close()
    #ready to erase s_info
    del self.s_info_dict[stpdst]
    logging.info('bye s; tpdst=%s', stpdst)
  
  #########################  handle s_data_traffic  ############################
  def create_s_sock(self): #return udp sock
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  def create_s_server(self, port):
    s_addr = (self.tl_ip, port)
    s_server = ThreadedUDPServer(self._handle_recvsdata, s_addr, ThreadedUDPRequestHandler)
    s_server_thread = threading.Thread(target=s_server.serve_forever)
    s_server_thread.daemon = True
    s_server_thread.start()
    #
    logging.info('udp_server is started at s_addr=%s', s_addr )
    return s_server
  
  def _handle_recvsdata(self, s_tp_dst, data):
    if not s_tp_dst in self.s_info_dict:
      raise NoItruleMatchError('No itjobrule match', s_tp_dst)
      return
    data = self.proc_pipeline(s_tp_dst = s_tp_dst,
                              data = data )
    self.forward_data(s_tp_dst, data)
  
  def proc_pipeline(self, s_tp_dst, data):
    global itfunc_dict
    itjobrule = self.s_info_dict[s_tp_dst]['itjobrule']
    jobtobedone = itjobrule['jobtobedone']
    proc_cap = itjobrule['proc']
    #datasize_ = 8*len(data) #in bits
    for ftag,compleft in jobtobedone.items():
      if jobtobedone[ftag] > 0:
        datasize = 8*sys.getsizeof(data)
        data = itfunc_dict[ftag](datasize, data, proc_cap)
        #update jobtobedone
        jobtobedone[ftag] -= datasize
    #
    return data
  
  def forward_data(self, s_tp_dst, data):
    s_info = self.s_info_dict[s_tp_dst]
    #
    to_ip = s_info['itjobrule']['data_to_ip']
    sock = s_info['s_sock']
    sock.sendto(data, (to_ip, int(s_tp_dst)) )
    logging.info('proced data is forwarded to_ip:%s', to_ip)
    #update session_active_last_time
    s_info['s_active_last_time']=time.time()
  
############################  IT data manipulation  ############################
func_comp_dict = {'f0':0.5,
                  'f1':1,
                  'f2':2,
                  'f3':3,
                  'f4':4 }
  
def proc_time_model(datasize, func_comp, proc_cap):
  '''
  proc_time_model used in sching process. To see if the sching results can be reaklized
  by assuming used models for procing are perfectly accurate.
  '''
  return 1000*func_comp*(datasize/64)*(1/proc_cap) #(ms)
  
# transit data manipulation functions
def f0(datasize, data, proc_cap):
  logging.info('f0 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f0'],
                            proc_cap = proc_cap)
  logging.info('f0_sleep=%s', t_sleep)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f1(datasize, data, proc_cap):
  logging.info('f1 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f1'],
                            proc_cap = proc_cap)
  logging.info('f1_sleep=%s', t_sleep)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f2(datasize, data, proc_cap):
  logging.info('f2 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f2'],
                            proc_cap = proc_cap)
  logging.info('f2_sleep=%s', t_sleep)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f3(datasize, data, proc_cap):
  logging.info('f3 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f3'],
                            proc_cap = proc_cap)
  logging.info('f3_sleep=%s', t_sleep)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f4(datasize, data, proc_cap):
  logging.info('f4 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f4'],
                            proc_cap = proc_cap)
  logging.info('f4_sleep=%s', t_sleep)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data

itfunc_dict = {'f0':f0,
               'f1':f1,
               'f2':f2,
               'f3':f3,
               'f4':f4}
  
def main(argv):
  nodename = intf = dtsl_ip = dtsl_port= dtst_port = logto = None
  try:
    opts, args = getopt.getopt(argv,'',['nodename=','intf=','dtsl_ip=','dtsl_port=','dtst_port=','logto='])
  except getopt.GetoptError:
    print 'transit.py --nodename=<> --intf=<> --dtsl_ip=<> --dtsl_port=<> --dtst_port=<> --logto=<>'
    sys.exit(2)
  #Initializing global variables with comman line options
  for opt, arg in opts:
    if opt == '--nodename':
      nodename = arg
    elif opt == '--intf':
      intf = arg
    elif opt == '--dtsl_ip':
      dtsl_ip = arg
    elif opt == '--dtsl_port':
      dtsl_port = int(arg)
    elif opt == '--dtst_port':
      dtst_port = int(arg)
    elif opt == '--logto':
      logto = arg
  #where to log, console or file
  if logto == 'file':
    fname = 'logs/'+nodename+'.log'
    logging.basicConfig(filename=fname,filemode='w',level=logging.DEBUG)
  elif logto == 'console':
    logging.basicConfig(level=logging.DEBUG)
  else:
    raise CommandLineOptionError('Unexpected logto', logto)
  #
  tl_ip = get_addr(intf)
  Transit(nodename = nodename,
          tl_ip = tl_ip,
          tl_port = dtst_port,
          dtsl_ip = dtsl_ip,
          dtsl_port = dtsl_port )
  #
  #raw_input('Enter')
  time.sleep(100000)
  
if __name__ == "__main__":
  main(sys.argv[1:])
  
