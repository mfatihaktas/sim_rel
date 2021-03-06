#!/usr/bin/python
import sys,socket,json,getopt,struct,time,errno
import numpy as np

class Sender(object):
  def __init__(self, dst_addr, proto, datasize, tx_type, file_url):
    self.dst_addr = dst_addr
    self.proto = proto
    self.datasize = datasize
    self.tx_type = tx_type
    self.file_url = file_url
    self.sock = None
    #
    if self.proto == 'tcp':
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect(self.dst_addr)
    elif self.proto == 'udp':
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
      print 'Unknown proto=%s.', self.proto
      sys.exit(2)
  
  def init_send(self):
    if self.tx_type == 'dummy':
      n = int(float(float(self.datasize)*1024/8/8))-5
      data = self.numpy_random(n)
      packer = struct.Struct('%sd' % n)
      data_str = packer.pack(*data)
      #
      dur = self.dummy_send(data_str)
      print 'dur=%s' % dur
    elif self.tx_type == 'file':
      self.file_send()
  
  def file_send(self):
    print 'start sending file'
    time_s = time.time()
    f=open(self.file_url, "r")
    #
    len_ = 0
    l = f.read(1024)
    while (l):
      c_len_ = len(l)
      #print 'sent size=%sB\n' % c_len_ #8*sys.getsizeof(l)
      len_ += c_len_
      if self.proto == 'tcp':
        self.sock.send(l)
      elif self.proto == 'udp':
        self.sock.sendto(l, self.dst_addr)
      l = f.read(1024)
    if self.proto == 'udp':
      self.sock.sendto('EOF', self.dst_addr)
    #
    tx_dur = time.time() - time_s
    print 'file_over_%s:%s is sent; size=%sB, dur=%ssec' % (self.proto,self.dst_addr,len_,tx_dur)
    return tx_dur
  
  def dummy_send(self, data):
    time_s = time.time()
    if self.proto == 'tcp':
      try:
        self.sock.sendall(data)
      except socket.error, e:
        if isinstance(e.args, tuple):
          print "errno is %d" % e[0]
          if e[0] == errno.EPIPE:
            # remote peer disconnected
            print "Detected remote disconnect"
          else:
            # determine and handle different error
            pass
        else:
          print "socket error ", e
    elif self.proto == 'udp':
      self.sock.sendto(data, self.dst_addr)
    #
    tx_dur = time.time() - time_s
    print 'dummy_over_%s is sent, to addr=%s' % (self.proto, self.dst_addr)
    print 'datasize=%sb, dur=%ssec' % (8*sys.getsizeof(data), tx_dur)
    #print 'data=%s' % data
    return tx_dur
  
  def numpy_random(self, n):
    '''
    Return a list/tuple of n random floats in the range [0, 1).
    float_size = 8Bs
    total size of generated random data_list = 8*n+72 Bs
    '''
    return tuple(np.random.random((n)) )
   
  def numpy_randint(self, a, b, n):
    '''Return a list of n random ints in the range [a, b].'''
    return np.random.randint(a, b, n).tolist()
  
  def test(self):
    if self.dst_addr[1] == 7001: #send to t
      data_json = {'type': 'itjob_rule',
                   'data': {'comp': 1.99999998665,
                            'data_to_ip': u'10.0.0.7',
                            'datasize': 1.0,
                            'itfunc_dict': {u'f1': 1.0, u'f2': 0.99999998665},
                            'proc': 183.150248167,
                            's_tp': 6000} }
      self.dummy_send(json.dumps(data_json))
    elif self.dst_addr[1] == 7998: #send to scher
      data_json = {'type': 'sp_sching_reply',
                   'data': 'OK'}
      self.dummy_send(json.dumps(data_json))
    elif self.dst_addr[1] == 7000: #send to p
      data_json = {'type': 'sching_reply',
                   'data': {'datasize':1,
                            'parism_level':1,
                            'par_share':[1],
                            'p_bw':[1],
                            'p_tp_dst':[6000] }}
      self.dummy_send(json.dumps(data_json))
    else:
      self.init_send()
  
def main(argv):
  dst_ip = dst_lport = proto = datasize = tx_type = file_url = None
  try:
    opts, args = getopt.getopt(argv,'',['dst_ip=','dst_lport=','proto=','datasize=','tx_type=', 'file_url='])
  except getopt.GetoptError:
    print 'sender.py --dst_ip=<> --dst_lport=<> --proto=tcp/udp --datasize=Mb --tx_type=dummy/file --file_url=<>'
    sys.exit(2)
  #Initializing variables with comman line options
  for opt, arg in opts:
    if opt == '--dst_ip':
      dst_ip = arg
    elif opt == '--dst_lport':
      dst_lport = int(arg)
    elif opt == '--proto':
      if arg == 'tcp' or arg == 'udp':
        proto = arg
      else:
        print 'unknown proto=%s' % arg
        sys.exit(2)
    elif opt == '--datasize':
      datasize = int(arg)
    elif opt == '--tx_type':
      if arg == 'file' or arg == 'dummy':
        tx_type = arg
      else:
        print 'unknown rx_type=%s' % arg
        sys.exit(2)
    elif opt == '--file_url':
      file_url = arg
  #
  #print 'dst_ip=%s, dst_lport=%s, proto=%s, datasize=%s' % (dst_ip, dst_lport, proto, datasize)
  dst_ip, dst_lport, proto, datasize
  ds = Sender(dst_addr = (dst_ip, dst_lport),
              proto = proto,
              datasize = datasize,
              tx_type = tx_type,
              file_url = file_url )
  ds.test()
  #
  raw_input('Enter')
  
if __name__ == "__main__":
  main(sys.argv[1:])
  
