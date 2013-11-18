#!/usr/bin/python

#import SocketServer as SS
import sys,socket,json,pprint,logging,subprocess,getopt
from errors import *

class Producer(object):
  def __init__(self, c_addr, c_lport):
    self.c_addr = c_addr
    self.c_lport = c_lport
    #
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  def send_sch_request(self, sch_req):
    data = json.dumps(sch_req)
    self.sock.sendto(data, (self.c_addr, self.c_lport))
    logging.info('sentto addr:%s, port:%s\ndata_size:%s',self.c_addr,self.c_lport,sys.getsizeof(data))
  
  def generate_sdata(self, datasize):
    numbytes = (datasize*1000)/8
    logging.info('over UDP to ip=%s, port=%s, datasize=%sBs', self.c_addr,self.c_lport,numbytes)
    'iperf -u -c 127.0.0.1 -p 7000 -n 1000 -b 1m'
    cli_o = subprocess.check_output(['iperf','-u',
                                     '-c',self.c_addr,'-p',str(self.c_lport),
                                     '-n',str(numbytes),'-b','1m'] )
    logging.info('\n%s',cli_o)
  def test(self, datasize):
    '''
    sch_req = {'req_dict': {'data_amount': 1, 'slack_metric': 24, 'func_list': ['f1', 'f2', 'f3']},
               'app_pref_dict': {'m_p': 1,'m_u': 1,'x_p': 0,'x_u': 0}
              }
    self.send_sch_request(sch_req)
    '''
    self.generate_sdata(datasize)
  
def main(argv):
  c_addr = cl_port = fname = logto = datasize = None
  try:
    opts, args = getopt.getopt(argv,'',['c_addr=','cl_port=','datasize=','logto='])
  except getopt.GetoptError:
    print 'transit.py --c_addr=<>  --cl_port=<> --datasize=<in Mbs> --logto=<>'
    sys.exit(2)
  #Initializing global variables with comman line options
  for opt, arg in opts:
    if opt == '--c_addr':
       c_addr = arg
    elif opt == '--cl_port':
       cl_port = int(arg)
    elif opt == '--datasize':
       datasize = int(arg)
    elif opt == '--logto':
       logto = arg
  #where to log, console or file
  if logto == 'file':
    logging.basicConfig(filename='p.log',level=logging.DEBUG)
  elif logto == 'console':
    logging.basicConfig(level=logging.DEBUG)
  else:
    raise CommandLineOptionError('Unexpected logto', logto)
  #
  p = Producer(c_addr, cl_port)
  p.test(datasize)
  #
  raw_input('Enter')
  
if __name__ == "__main__":
  main(sys.argv[1:])
  
