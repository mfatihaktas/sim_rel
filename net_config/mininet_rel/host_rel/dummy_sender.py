#!/usr/bin/python
import sys,socket,json,getopt,struct
import pprint
import numpy as np
class DummySender(object):
  def __init__(self, dst_ip, dst_lport, proto, datasize):
    self.dst_ip = dst_ip
    self.dst_lport = dst_lport
    self.proto = proto
    self.datasize = datasize
    self.sock = None
    #
    if self.proto == 'tcp':
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect((self.dst_ip, self.dst_lport))
    elif self.proto == 'udp':
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
      print 'Unknown proto=%s.', self.proto
      sys.exit(2)
  
  def dummy_send(self, data):
    if self.proto == 'tcp':
      self.sock.sendall(data)
    elif self.proto == 'udp':
      self.sock.sendto(data, (self.dst_ip, self.dst_lport))
    #
    print 'proto:{}, sentto ip:{}, port:{}\ndata:{}'.format(self.proto, self.dst_ip, self.dst_lport, data)
  
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
    if self.dst_lport == 7001: #send sching msgs
      """
      data_json = {'type': 'sp_sching_reply',
                   'data': 'OK'}
      """
      """
      data_json = {'type': 'sp_sching_reply',
                   'data': 'OK'}
      """
      """
      data_json = {'type': 'itjob_rule',
                   'data': {'comp': 2.83333333313,
                            'data_to_ip': '10.0.0.1',
                            'itfunc_dict': {'f2': 2.83333333313},
                            'proc': 288.935318788,
                            's_tp': 6000,
                            'datasize': 0.5} }
      """
      #sching_res for num_session=0
      data_json = {'type': 'itjob_rule',
                   'data': {'comp': 1.99999998665,
                            'data_to_ip': u'10.0.0.7',
                            'datasize': 1.0,
                            'itfunc_dict': {u'f1': 1.0, u'f2': 0.99999998665},
                            'proc': 183.150248167,
                            's_tp': 6000} }
      self.dummy_send(json.dumps(data_json))
    elif self.dst_lport == 7998: #send to scher
      data_json = {'type': 'sp_sching_reply',
                   'data': 'OK'}
      self.dummy_send(data_json)
    else: #send random_session_data
      n = int(float(float(self.datasize)*1024/8/8))-5
      data = self.numpy_random(n)
      #print 'random_data=', data
      #print 'random_data_size=%sBs' % (sys.getsizeof(data))
      #data_str = ''.join(str(e) for e in data)
      #data_str = json.dumps(data)
      #data_str = struct.pack('%sd' % 3, 1.0, 2.0, 3.0)
      packer = struct.Struct('%sd' % n)
      data_str = packer.pack(*data)
      #print 'data_str=\n%s' % data_str
      print 'data_str_size=%sbs' % (8*sys.getsizeof(data_str))
      #self.dummy_send(data_str)
      """
      dummy_data = ''
      for i in range(0, 100):
        dummy_data += '1'
      self.dummy_send(dummy_data)
      print 'dummy_data_size=%sBs' % (sys.getsizeof(dummy_data))
      """
  
def main(argv):
  dst_ip = dst_lport = proto = datasize = None
  try:
    opts, args = getopt.getopt(argv,'',['dst_ip=','dst_lport=','proto=','datasize='])
  except getopt.GetoptError:
    print 'dummy_sender.py --dst_ip=<> --dst_lport=<> --proto=tcp/udp --datasize=Mb'
    sys.exit(2)
  #Initializing variables with comman line options
  for opt, arg in opts:
    if opt == '--dst_ip':
      dst_ip = arg
    elif opt == '--dst_lport':
      dst_lport = int(arg)
    elif opt == '--proto':
      proto = arg
    elif opt == '--datasize':
      datasize = int(arg)
  #
  #print 'dst_ip=%s, dst_lport=%s, proto=%s, datasize=%s' % (dst_ip, dst_lport, proto, datasize)
  ds = DummySender(dst_ip, dst_lport, proto, datasize)
  ds.test()
  #
  raw_input('Enter')
  
if __name__ == "__main__":
  main(sys.argv[1:])
  
