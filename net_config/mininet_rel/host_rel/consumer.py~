import SocketServer as SS
import sys,socket,json
import threading, pprint

class ThreadedUDPServer(SS.ThreadingMixIn, SS.UDPServer):
  pass

class ThreadedUDPRequestHandler_SESSION(SS.BaseRequestHandler):
  def handle(self):
    socket = self.request[1]
    sockname_tuple = socket.getsockname()
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    print "\nSocket listening on addr:{} and port:{} is speaking:".format(sockname_tuple[0], sockname_tuple[1])
    print "session_cur_thread {} -> {} wrote:".format(cur_thread.name, self.client_address)
    print data
    '''
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
    socket.sendto(data, (session_info['consumer_ip'], int(session_tp)))
    '''
class Consumer(object):
  def __init__(self, c_addr, c_lport_list):
    self.c_addr = c_addr
    self.c_lport_list = c_lport_list
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.session_server_list = []
    
  def print_consumer(self):
    print '-------HHH---------'
    print 'c_addr: ', self.c_addr
    print 'c_lport_list: ', self.c_lport_list
    print '-------OOO---------'
    
  def create_session_servers(self):
    for i,lport in enumerate(self.c_lport_list):
      print "ThreadedUDPServer started for session_lport:{} ...".format(lport)
      self.session_server_list.append(
        ThreadedUDPServer((self.c_addr, lport), ThreadedUDPRequestHandler_SESSION)
      )  
      session_server_thread = threading.Thread(target=self.session_server_list[i].serve_forever)
      session_server_thread.daemon = True
      session_server_thread.start()
      #
  def test(self):
    #self.print_consumer()
    self.create_session_servers()
    
def main():
  if len(sys.argv) < 3:
    raise RuntimeError('argv = [c_addr, c_lport0, c_lport1, ... ]')
  c_addr = sys.argv[1]
  c_lport_list = []
  for i in range(2, len(sys.argv)):
    c_lport_list.append( int(sys.argv[i]) )
  #
  c = Consumer(c_addr, c_lport_list)
  c.test()
  #
  raw_input('Enter')

if __name__ == "__main__":
  main()
  
