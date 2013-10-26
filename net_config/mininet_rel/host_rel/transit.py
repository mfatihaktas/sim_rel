import SocketServer as SS
import threading, time
import sys,socket,json
import commands, pprint

class ThreadedUDPRequestHandler_SCH(SS.BaseRequestHandler):
  def handle(self):
    global session_info_dict
    data = self.request[0].strip()
    socket = self.request[1]
    cur_thread = threading.current_thread()
    print "sch_cur_thread {} -> {} wrote:".format(cur_thread.name, self.client_address)
    print data
    #
    sch_cmd = json.loads(data)
    # get rid of unicode strings
    sch_cmd = dict([(str(k), str(v)) for k, v in sch_cmd.items()])
    # print 'sch_cmd: ', sch_cmd
    session_tp = sch_cmd['session_tp']
    if not (session_tp in session_info_dict):
      session_info_dict[session_tp] = {k:v for k,v in sch_cmd.iteritems() if k !='session_tp' }
      session_info_dict[session_tp].\
      update({'session_server': create_session_server(int(session_tp)),
              'session_active_last_time': time.time()})
    else:
      print 'There is already one session with tp: ', session_tp

class ThreadedUDPRequestHandler_SESSION(SS.BaseRequestHandler):
  def handle(self):
    global session_info_dict
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    print "session_cur_thread {} -> {} wrote:".format(cur_thread.name, self.client_address)
    print data
    #
    socket = self.request[1]
    server = self.server
    session_tp = str(server.server_address[1])
    print 'session_tp: ', session_tp
    try:
      session_info = session_info_dict[session_tp]
    except (KeyError):
      print 'No job match for ', server.server_address
      pass
    # process with corresponding in-transit function
    data = it_func_dict[session_info['job']](data)
    # send to consumer
    socket.sendto(data, (session_info['consumer_ip'], int(session_tp)))
    # set session_active_last_time
    session_info_dict['session_active_last_time'] = time.time()
    
class ThreadedUDPServer(SS.ThreadingMixIn, SS.UDPServer):
  pass

p_index = 0.01
# transit data manipulation functions
def f1(data):
  global p_index
  print 'in-transit function f1 is on action'
  time.sleep((64*len(data)/pow(10,9))*p_index*1.1)
  return data
def f2(data):
  global p_index
  print 'in-transit function f2 is on action'
  time.sleep((64*len(data)/pow(10,9))*p_index*1.2)
  return data
def f3(data):
  global p_index
  print 'in-transit function f3 is on action'
  time.sleep((64*len(data)/pow(10,9))*p_index*1.3)
  return data

it_func_dict = {'f1':f1,
                'f2':f2,
                'f3':f3}

def create_session_server(session_l_port):
  global sch_l_addr, session_server_dict
  print "ThreadedUDPServer for SESSION started at session_l_addr:{}, session_l_port:{}...".format(sch_l_addr,session_l_port)
  session_server = \
  ThreadedUDPServer((sch_l_addr, session_l_port), ThreadedUDPRequestHandler_SESSION)
  session_server_thread = threading.Thread(target=session_server.serve_forever)
  session_server_thread.daemon = True
  session_server_thread.start()
  #
  return session_server

sch_l_addr = None
sch_server = None
def create_sch_server(sch_l_port, bind_intf):
  global sch_l_addr, sch_server
  # search and bind to eth0 ip address
  intf_list = commands.getoutput("ifconfig -a | sed 's/[ \t].*//;/^$/d'").split('\n')
  intf_eth0 = None
  for intf in intf_list:
    if bind_intf in intf:
      intf_eth0 = intf
  intf_eth0_ip = commands.getoutput("ip address show dev " + intf_eth0).split()
  intf_eth0_ip = intf_eth0_ip[intf_eth0_ip.index('inet') + 1].split('/')[0]
  sch_l_addr = intf_eth0_ip #socket.gethostbyname(socket.gethostname())
  sch_server = ThreadedUDPServer((sch_l_addr, sch_l_port),ThreadedUDPRequestHandler_SCH)
  print "ThreadedUDPServer for SCH started at sch_l_addr:{}, sch_l_port:{}...".format(sch_l_addr,sch_l_port)
  sch_server_thread = threading.Thread(target=sch_server.serve_forever)
  sch_server_thread.daemon = True
  sch_server_thread.start()

# SCH table tp_dst:func
session_info_dict = {}
def init_transit_service(sch_l_port, bind_intf):
  global session_soft_state_span
  # SCH server
  create_sch_server(sch_l_port, bind_intf)
  session_soft_expire_timer = threading.Timer(session_soft_state_span,
                                              _handle_SessionSoftTimerExpire)
  session_soft_expire_timer.daemon = True
  session_soft_expire_timer.start()

session_soft_state_span = 1000.0
def _handle_SessionSoftTimerExpire():
  global session_soft_state_span, session_info_dict
  while True:
    print '------ _handle_SessionSoftTimerExpire is called !'
    print 'session_info_dict:'
    pprint.pprint(session_info_dict )
    for session_tp, session_info in dict(session_info_dict).iteritems():
      inactive_time_span = time.time() - session_info['session_active_last_time']
      if inactive_time_span >= session_soft_state_span: #soft state expire
        session_info['session_server'].shutdown()
        del session_info_dict[session_tp]
        print 'session with tp: {} is soft-expired !'.format(session_tp)
    #
    print '------'
    # do every 30 secs
    time.sleep(session_soft_state_span)

def main():
  if len(sys.argv) != 3:
    raise RuntimeError('argv = [sch_l_port, bind_intf]')
  sch_l_port=int(sys.argv[1])
  bind_intf = sys.argv[2]
  #
  init_transit_service(sch_l_port, bind_intf)
  
  raw_input('Enter')
    
if __name__ == "__main__":
  main()
  
  """
  Process rxed chunk of data with O(n):simple for loop
  Assume transmitter is sending a number series, number+1 mod(10)
  - linear relation btw computational_time vs. data_amount
  - No increase in amount of data by computation
  """
  """
  ped_data = ''
  for n in data:
    n = (int(n) + 1) % 10
    ped_data = ped_data + str(n)
  #Send the data to the DST
  socket.sendto(ped_data, (t_addr,l_t_port))
  print "ped_data:{} is sent to t_addr:{},t_port:{}".format(ped_data,t_addr,l_t_port)
  """
