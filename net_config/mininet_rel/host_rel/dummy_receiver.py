#!/usr/bin/python

import SocketServer as SS
import sys,socket,json,getopt,threading,commands
import pprint
#########################  UDP Server-Handler  ###########################
class ThreadedUDPServer(SS.ThreadingMixIn, SS.UDPServer):
  pass

class ThreadedUDPRequestHandler(SS.BaseRequestHandler):
  def handle(self):
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    print 'cur_thread={}; dummyrecver_udp rxed \ndatasize={} \ndata={}'.format(cur_thread.name, sys.getsizeof(data), data)
    sock = self.request[1]
    response = 'ok'
    sock.sendto(response, self.client_address)
    print 'response=%s is sent back to client.' % response
  
#########################  TCP Server-Handler  ###########################
class ThreadedTCPServer(SS.ThreadingMixIn, SS.TCPServer):
  pass

class ThreadedTCPRequestHandler(SS.BaseRequestHandler):
  def handle(self):
    data = self.request.recv(1024*10)
    cur_thread = threading.current_thread()
    print 'cur_thread={}; dummyrecver_tcp rxed \ndatasize={} \ndata={}'.format(cur_thread.name, sys.getsizeof(data), data)
    response = 'ok'
    self.request.sendall(response)
    print 'response=%s is sent back to client.' % response
  
##########################################################################
class DummyReceiver(object):
  def __init__(self, laddr, lport, proto):
    self.laddr = laddr
    self.lport = lport
    self.proto = proto
    if self.proto == 'tcp':
      self.server = ThreadedTCPServer((self.laddr, lport), ThreadedTCPRequestHandler)
    elif self.proto == 'udp':
      self.server = ThreadedUDPServer((self.laddr, lport), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=self.server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print 'dummy_recver_{} is started on laddr={}, lport={}'.format(self.proto, laddr, lport)
  
  def shutdown(self):
    self.server.shutdown()
    print 'dummy_recver_%s is shutdown.' % self.proto
  
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
  lport = lintf = proto = None
  try:
    opts, args = getopt.getopt(argv,'',['lport=','lintf=','proto='])
  except getopt.GetoptError:
    print 'dummy_receiver.py --lport=<> --lintf=<> --proto=tcp/udp'
    sys.exit(2)
  #Initializing variables with comman line options
  for opt, arg in opts:
    if opt == '--lport':
       lport = int(arg)
    elif opt == '--lintf':
       lintf = arg
    elif opt == '--proto':
       proto = arg
  #
  laddr = get_laddr(lintf)
  dr = DummyReceiver(laddr, lport, proto)
  #
  raw_input('Enter')
  dr.shutdown()
  
if __name__ == "__main__":
  main(sys.argv[1:])
