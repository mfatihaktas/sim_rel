import SocketServer as SS
import sys,json,logging,threading,pprint,getopt

class ThreadedUDPServer(SS.ThreadingMixIn, SS.UDPServer):
  pass

class ThreadedUDPRequestHandler_SESSION(SS.BaseRequestHandler):
  def handle(self):
    socket = self.request[1]
    sockname_tuple = socket.getsockname()
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    #
    addr_port = sockname_tuple[0]+'.'+sockname_tuple[1]
    logging.info('%s, consumer recved over addr.port=%s, data_size=%s',cur_thread.name,addr_port,sys.getsizeof(data))
    #print data

class Consumer(object):
  def __init__(self, laddr, lport_list):
    self.laddr = laddr
    self.lport_list = lport_list
    self.s_server_list = []
  
  def log_consumer(self):
    logging.info('-------')
    logging.info('laddr=%s',self.laddr)
    logging.info('lport_list=%s',json.dumps(self.lport_list))
    logging.info('-------')
  
  def init_sservers(self):
    for i,lport in enumerate(self.lport_list):
      self.s_server_list.append(
        ThreadedUDPServer((self.laddr, lport), ThreadedUDPRequestHandler_SESSION)
      )
      s_server_thread = threading.Thread(target=self.s_server_list[i].serve_forever)
      s_server_thread.daemon = True
      s_server_thread.start()
      logging.info('ThreadedUDPServer started for lport=%s', lport)
  
  def shutdown_sservers(self):
    for i,lport in enumerate(self.lport_list):
      self.s_server_list[i].shutdown()
      logging.info('s_server with lport=%s is shutdown', lport)
  
  def test(self):
    self.log_consumer()
    self.init_sservers()
  
def main(argv):
  laddr = logto = lports = None
  lport_list = []
  try:
    opts, args = getopt.getopt(argv,'',['laddr=','logto=', 'lports='])
  except getopt.GetoptError:
    print 'transit.py --laddr=<>  --logto=<> --lports=lport1,lport2, ...'
    sys.exit(2)
  #Initializing global variables with comman line options
  for opt, arg in opts:
    if opt == '--laddr':
       laddr = arg
    elif opt == '--logto':
       logto = arg
    elif opt == '--lports':
       lports = arg
  #
  for lport in lports.split(','):
    lport_list.append(int(lport))
  #where to log, console or file
  if logto == 'file':
    logging.basicConfig(filename='c.log',level=logging.DEBUG)
  elif logto == 'console':
    logging.basicConfig(level=logging.DEBUG)
  else:
    raise CommandLineOptionError('Unexpected logto', logto)
  #
  c = Consumer(laddr, lport_list)
  c.test()
  #
  raw_input('Enter')
  c.shutdown_sservers()
  
if __name__ == "__main__":
  main(sys.argv[1:])
  
