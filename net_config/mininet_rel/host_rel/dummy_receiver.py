#!/usr/bin/python

import SocketServer as SS
import sys,socket,json,getopt,threading,commands
import pprint

class ThreadedUDPServer(SS.ThreadingMixIn, SS.UDPServer):
  pass

class ThreadedUDPRequestHandler_SESSION(SS.BaseRequestHandler):
  def handle(self):
    #socket = self.request[1]
    #sockname_tuple = socket.getsockname()
    data = self.request[0].strip()
    cur_thread = threading.current_thread()
    print "\ndummy_recver rxed cur_thread={}, data=\n{}".format(cur_thread.name, data)

class DummyReceiver(object):
  def __init__(self, laddr, lport):
    self.laddr = laddr
    self.lport = lport
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server = ThreadedUDPServer((self.laddr, lport), ThreadedUDPRequestHandler_SESSION)
    server_thread = threading.Thread(target=self.server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print 'dummy_recver is started on laddr={}, lport={}'.format(laddr, lport)
  
  def shutdown_recver(self):
    self.server.shutdown()
    print 'dummy_recver is shutdown.'
  
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
  lport = lintf = None
  try:
    opts, args = getopt.getopt(argv,'',['lport=','lintf='])
  except getopt.GetoptError:
    print 'transit.py --lport=<> --lintf=<>'
    sys.exit(2)
  #Initializing variables with comman line options
  for opt, arg in opts:
    if opt == '--lport':
       lport = int(arg)
    elif opt == '--lintf':
       lintf = arg
  #
  laddr = get_laddr(lintf)
  dr = DummyReceiver(laddr, lport)
  #
  raw_input('Enter')
  dr.shutdown_recver()
  
if __name__ == "__main__":
  main(sys.argv[1:])
