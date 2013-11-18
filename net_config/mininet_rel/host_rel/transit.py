#!/usr/bin/python

import SocketServer as SS
import threading, time, sys, json, pprint
import commands, getopt, logging, subprocess
from errors import *

#
info_dict = {'scher_ip':'192.168.239.64', #'192.168.56.1',
             'sching_tp_dst':7000,
             'sthelse_ip': '...'
            }

########################  Comm for Sching  #####################################
class ThreadedUDPRequestHandler_SCH(SS.BaseRequestHandler):
  def handle(self):
    data = self.request[0].strip()
    socket = self.request[1]
    cur_thread = threading.current_thread()
    #print 'client_address:', self.client_address[0]
    #
    if 1: #self.client_address[0] == info_dict['scher_ip']:
      logging.info('ItNode rxed from Scher cur_thread:%s \n data:%s', cur_thread.name, data)
      response = 'OK'
      socket.sendto(response, self.client_address)
      process_rxeddata_fromscher(data)
      #get rid of unicode strings
      #sch_cmd = dict([(str(k), str(v)) for k, v in sch_cmd.items()])
    elif self.client_address[0] == info_dict['sthelse_ip']:
      pass
    else:
      raise UnknownClientError('Unknown RuleSender', data)

def process_rxeddata_fromscher(data):
  #data is in json format: dict={}
  dict_ = json.loads(data)
  try:
    type_ = dict_['type']
  except KeyError:
    log.error('no type field in rxed data from scher')
    raise CorruptMsgError(data = dict_,
                          msg = 'No type field')
    return
  if type_ == 'itjobrule':
    data_ = dict_['data']
    welcome_s(data_)
  elif type_ == 'sth_else':
    pass
  else:
    log.error('type_ is not recognized')
    raise MsgDataError(data = type_,
                       msg = 'Unrecognized type')
  
def welcome_s(data_):
  global s_info_dict
  #If a new s with same tpdst arrives, old info will be overwritten with new one
  stpdst = int(data_['s_tp'])
  if stpdst in s_info_dict:
    bye_s(stpdst)
  #updating global dicts
  stpdst = data_['s_tp']
  del data_['s_tp']
  #
  jobtobedone = {ftag:data_['datasize']*comp/func_comp_dict[ftag] \
                   for ftag,comp in data_['itfunc_dict'].items()}
  data_.update( {'jobtobedone': jobtobedone} )
  s_info_dict[stpdst] = {'itjobrule':data_,
                         's_server':create_s_server(stpdst) }
  #
  logging.info('new s with tpdst:%s is welcomed', stpdst)
  logging.info('s_info_dict[%s]:\n%s', stpdst, pprint.pformat(s_info_dict[stpdst]))
  #print 's_info_dict:'
  #pprint.pprint(s_info_dict)
  #set session_active_last_time
  s_info_dict[stpdst].update( {'s_active_last_time':time.time()} )
  
def bye_s(stpdst):
  global s_info_dict
  s_info_dict[stpdst]['s_server'].shutdown()
  #ready to erase s_info
  del s_info_dict[stpdst]
  logging.info('bye s with tpdst:%s', stpdst)
  
########################  Comm for Transport Sessions  #########################
class ThreadedUDPRequestHandler_SESSION(SS.BaseRequestHandler):
  def handle(self):
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    socket = self.request[1]
    server = self.server
    #
    s_tp_dst = int(server.server_address[1])
    logging.info('ItNode rxed s_data of size:%sBs over cur_thread:%s, s_tp_dst:%s', sys.getsizeof(data), cur_thread.name, s_tp_dst)
    if s_tp_dst in s_info_dict: #itjobrule is previously rxed for s with tp_dst
      pass
    else:
      raise NoItruleMatch('No itjobrule is rxed for s_tp_dst=%s' % s_tp_dst, s_tp_dst)
      logging.error('No itjobrule for %s', server.server_address)
      return
    #
    data = proc_pipeline(s_tp_dst = s_tp_dst,
                         data = data )
    forward_data(s_tp_dst, data, socket)
  
def proc_pipeline(s_tp_dst, data):
  global s_info_dict
  itjobrule = s_info_dict[s_tp_dst]['itjobrule']
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
  
def forward_data(s_tp_dst, data, socket):
  global s_info_dict
  to_ip = s_info_dict[s_tp_dst]['itjobrule']['data_to_ip']
  socket.sendto(data, (to_ip, int(s_tp_dst)) )
  logging.info('proced data is forwarded to_ip:%s', to_ip)
  #update session_active_last_time
  s_info_dict[s_tp_dst].update( {'s_active_last_time':time.time()} )
    
class ThreadedUDPServer(SS.ThreadingMixIn, SS.UDPServer):
  pass
##############################  OOO  ###########################################

def create_s_server(ls_port):
  logging.info("ThreadedUDPServer for SESSION started at session_l_addr:%s, ls_port:%s", lsching_addr,ls_port)
  s_server = \
    ThreadedUDPServer((lsching_addr, ls_port), ThreadedUDPRequestHandler_SESSION)
  s_server_thread = threading.Thread(target=s_server.serve_forever)
  s_server_thread.daemon = True
  s_server_thread.start()
  #
  return s_server

def create_sching_server(lsching_port, bind_intf):
  global lsching_addr, sching_server
  # search and bind to eth0 ip address
  intf_list = commands.getoutput("ifconfig -a | sed 's/[ \t].*//;/^$/d'").split('\n')
  intf_eth0 = None
  for intf in intf_list:
    if bind_intf in intf:
      intf_eth0 = intf
  intf_eth0_ip = commands.getoutput("ip address show dev " + intf_eth0).split()
  intf_eth0_ip = intf_eth0_ip[intf_eth0_ip.index('inet') + 1].split('/')[0]
  lsching_addr = intf_eth0_ip #socket.gethostbyname(socket.gethostname())
  sching_server = ThreadedUDPServer((lsching_addr, lsching_port),ThreadedUDPRequestHandler_SCH)
  logging.info('ThreadedUDPServer for SCHING started at lsching_addr:%s, lsching_port:%s',lsching_addr,lsching_port)
  sching_server_thread = threading.Thread(target=sching_server.serve_forever)
  sching_server_thread.daemon = True
  sching_server_thread.start()

def _handle_SessionSoftTimerExpire():
  global s_info_dict
  while True:
    logging.info('_handle_SessionSoftTimerExpire is called !')
    print 's_info_dict:'
    pprint.pprint(s_info_dict )
    for s_tp_dst, s_info in s_info_dict.items():
      inactive_time_span = time.time() - s_info['s_active_last_time']
      if inactive_time_span >= session_soft_state_span: #soft state expire
        s_info['s_server'].shutdown()
        del s_info_dict[s_tp_dst]
        logging.info('s with tp_dst:%s is soft-expired.',s_tp_dst)
    #
    logging.info('------')
    # do every 30 secs
    time.sleep(session_soft_state_span)

def init_tservice(lsching_port, bind_intf):
  # SCH server
  create_sching_server(lsching_port, bind_intf)
  s_soft_expire_timer = threading.Timer(session_soft_state_span,
                                        _handle_SessionSoftTimerExpire)
  s_soft_expire_timer.daemon = True
  s_soft_expire_timer.start()
  #
  logging.info('%s is ready...', nodename)
  #for mininet: to printout even while logging to file
  print '%s is ready...' % nodename

def shutdown_tservice():
  sching_server.shutdown()
  logging.info('sching_server is shutdown.')
  for stpdst in s_info_dict:
    s_info_dict[stpdst]['s_server'].shutdown()
    logging.info('stpdst=%s, s_server is shutdown.',stpdst)
  logging.shutdown()
  
############################  IT data manipulation  ############################
func_comp_dict = {'f0':1,
                  'f1':2,
                  'f2':4,
                  'f3':2.5,
                  'f4':5 }
  
def proc_time_model(datasize, func_comp, proc_cap):
  '''
  proc_time_model used in sching process. To see if the sching results can be reaklized
  by assuming used models for procing are perfectly accurate.
  '''
  return datasize*func_comp*(1/proc_cap) #sec
  
# transit data manipulation functions
def f0(datasize, data, proc_cap):
  logging.info('f0 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f0'],
                            proc_cap = proc_cap)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f1(datasize, data, proc_cap):
  logging.info('f1 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f1'],
                            proc_cap = proc_cap)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f2(datasize, data, proc_cap):
  logging.info('f2 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f2'],
                            proc_cap = proc_cap)
  print 't_sleep: ', t_sleep
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f3(datasize, data, proc_cap):
  logging.info('f3 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f3'],
                            proc_cap = proc_cap)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data
  
def f4(datasize, data, proc_cap):
  logging.info('f4 is on action')
  t_sleep = proc_time_model(datasize = datasize,
                            func_comp = func_comp_dict['f4'],
                            proc_cap = proc_cap)
  time.sleep(t_sleep)
  #for now no manipulation on data, just move the data forward !
  return data

itfunc_dict = {'f0':f0,
               'f1':f1,
               'f2':f2,
               'f3':f3,
               'f4':f4}
  
#global variables
nodename = lsching_port = bind_intf = logto = None
lsching_addr = sching_server = None
# SCH table s_tp_dst:{'itjobrule':<>, 'info':<>}
s_info_dict = {}
session_soft_state_span = 1000.0
#
def log_globalvars():
  logging.info('\nnodename=%s\nlsching_port=%s\nbind_intf=%s\nlogto=%s',
               nodename, lsching_port, bind_intf, logto)
  
def main(argv):
  global nodename,lsching_port,bind_intf,logto
  try:
    opts, args = getopt.getopt(argv,'',['nodename=','lsching_port=','bind_intf=','logto='])
  except getopt.GetoptError:
    print 'transit.py --nodename=<>  --lsching_port=<> --bind_intf=<> --logto=<>'
    sys.exit(2)
  #Initializing global variables with comman line options
  for opt, arg in opts:
    if opt == '--nodename':
       nodename = arg
    elif opt == '--lsching_port':
       lsching_port = int(arg)
    elif opt == '--bind_intf':
       bind_intf = arg
    elif opt == '--logto':
       logto = arg
  #where to log, console or file
  if logto == 'file':
    fname = nodename+'.log'
    logging.basicConfig(filename=fname,filemode='w',level=logging.DEBUG)
  elif logto == 'console':
    logging.basicConfig(level=logging.DEBUG)
  else:
    raise CommandLineOptionError('Unexpected logto', logto)
  #
  log_globalvars()
  init_tservice(lsching_port, bind_intf)
  #
  #raw_input('Enter')
  time.sleep(100000)
  shutdown_tservice()
  
if __name__ == "__main__":
  main(sys.argv[1:])
  
