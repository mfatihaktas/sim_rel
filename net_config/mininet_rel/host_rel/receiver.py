#!/usr/bin/python

import sys,socket,SocketServer,getopt,threading,commands
#import pprint,json
#########################  UDP Server-Handler  ###########################
class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
  def __init__(self, server_address, RequestHandlerClass):
    self.nofBs_rxed = 0
    SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass)

  def get_nofBs_rxed(self):
    return self.nofBs_rxed

  def inc_nOfBs_rxed(self, howmuch):
    self.nofBs_rxed += howmuch

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    datasize = sys.getsizeof(data)-37 #37 is python string format header length
    #
    s = self.server
    s.inc_nOfBs_rxed(datasize)
    nofBs_rxed = s.get_nofBs_rxed()
    #
    print 'cur_thread=%s; threadedserver_udp:%s rxed' % (cur_thread.name, s.server_address[1])
    print 'datasize=%sB\ndata=%s' % (datasize, '...')
    print 'nofBs_rxed=%s' % nofBs_rxed
  
#########################  TCP Server-Handler  ###########################
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  def __init__(self, server_address, RequestHandlerClass):
    self.nofBs_rxed = 0
    SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
  
  def get_nofBs_rxed(self):
    return self.nofBs_rxed

  def inc_nOfBs_rxed(self, howmuch):
    self.nofBs_rxed += howmuch
  
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    data = self.request.recv(4096)
    cur_thread = threading.current_thread()
    datasize = sys.getsizeof(data)-37 #37 is python string format header length
    #
    s = self.server
    s.inc_nOfBs_rxed(datasize)
    nofBs_rxed = s.get_nofBs_rxed()
    #
    print 'cur_thread=%s; threadedserver_tcp:%s rxed' % (cur_thread.name, s.server_address[1])
    print 'datasize=%sB\ndata=%s' % (datasize, '...')
    print 'nofBs_rxed=%s' % nofBs_rxed

##########################################################################
class Receiver(object):
  def __init__(self, laddr, proto, rx_type, file_url):
    self.laddr = laddr
    self.proto = proto
    self.file_url = file_url
    #
    self.rx_type = rx_type
    if rx_type == 'file':
      self.f_obj = open(self.file_url, 'w')
      self.rx_file()
    elif rx_type == 'dummy':
      if self.proto == 'tcp':
        self.server = ThreadedTCPServer(self.laddr, ThreadedTCPRequestHandler)
        #while trying single thread TCPServer
        #self.server = SocketServer.TCPServer(self.laddr, TCPRequestHandler)
        #print 'rxdummy_{} is listening on laddr={}'.format(self.proto, self.laddr)
        #self.server.serve_forever()
      elif self.proto == 'udp':
        self.server = ThreadedUDPServer(self.laddr, ThreadedUDPRequestHandler)
      server_thread = threading.Thread(target=self.server.serve_forever)
      server_thread.daemon = True
      server_thread.start()
      print 'dummyrx_threaded%sserver started on laddr=%s' % (self.proto, self.laddr)
  
  def rx_file(self):
    print 'filerx_%s_sock is listening on laddr=%s' % (self.proto, self.laddr, )
    if self.proto == 'tcp':
      self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.rx_sock.bind(self.laddr)
      self.rx_sock.listen(1)
      sc, addr = self.rx_sock.accept()
      print '%s_file_recver gets conn from addr=%s' % (self.proto, addr[0])
      #while (True):
      l = sc.recv(1024)
      rxed_tlen = len(l)
      while (l != 'EOF'):
        self.f_obj.write(l)
        l = sc.recv(1024)
        rxed_tlen += len(l)
        print 'rxed size=%sB, rxed_tlen=%sB' % (len(l), rxed_tlen)
      print 'tcp_EOF is rxed.'
      #
      sc.close()
    elif self.proto == 'udp':
      self.rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.rx_sock.bind(self.laddr)      
      l = self.rx_sock.recv(1024)
      rxed_tlen = len(l)
      while (l != 'EOF'):
        self.f_obj.write(l)        
        l = self.rx_sock.recv(1024)
        rxed_tlen += len(l)
        print 'rxed size=%sB, rxed_tlen=%sB' % (len(l), rxed_tlen)
        #print 'rxed data=\n%s' % l
      print 'udp_EOF is rxed.'
    #
    self.f_obj.close()
    self.rx_sock.close()
    print 'rx_file is complete...'
  
def get_laddr(lintf):
  # search and bind to eth0 ip address
  intf_list = commands.getoutput("ifconfig -a | sed 's/[ \t].*//;/^$/d'").split('\n')
  intf_eth0 = None
  for intf in intf_list:
    if lintf in intf:
      intf_eth0 = intf
  intf_eth0_ip = commands.getoutput("ip address show dev " + intf_eth0).split()
  intf_eth0_ip = intf_eth0_ip[intf_eth0_ip.index('inet') + 1].split('/')[0]
  return intf_eth0_ip

def main(argv):
  lport = lintf = proto = rx_type = file_url = None
  try:
    opts, args = getopt.getopt(argv,'',['lport=','lintf=','proto=','rx_type=','file_url='])
  except getopt.GetoptError:
    print 'receiver.py --lport=<> --lintf=<> --proto=tcp/udp --rx_type=file/dummy --file_url=<>'
    sys.exit(2)
  #Initializing variables with comman line options
  for opt, arg in opts:
    if opt == '--lport':
       lport = int(arg)
    elif opt == '--lintf':
       lintf = arg
    elif opt == '--proto':
      if arg == 'tcp' or arg == 'udp':
        proto = arg
      else:
        print 'unknown proto=%s' % arg
        sys.exit(2)
    elif opt == '--rx_type':
      if arg == 'file' or arg == 'dummy':
        rx_type = arg
      else:
        print 'unknown rx_type=%s' % arg
        sys.exit(2)
    elif opt == '--file_url':
      file_url = arg
  #
  lip = get_laddr(lintf)
  dr = Receiver(laddr = (lip, lport),
                proto = proto,
                rx_type = rx_type,
                file_url = file_url )
  #
  raw_input('Enter')
  
if __name__ == "__main__":
  main(sys.argv[1:])
