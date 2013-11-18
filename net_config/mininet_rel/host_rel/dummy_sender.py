#!/usr/bin/python

import sys,socket,json
import pprint

class DummySender(object):
  def __init__(self, dst_addr, dst_lport):
    self.dst_addr = dst_addr
    self.dst_lport = dst_lport
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  def dummy_send(self, data_json):
    data = json.dumps(data_json)
    self.sock.sendto(data, (self.dst_addr, self.dst_lport))
    print 'sentto addr:{}, port:{}\ndata:{}'.format(self.dst_addr, self.dst_lport, data)

  def test(self):
    if self.dst_lport == 7000: #send sching msgs
      data_json = {'type': 'itjobrule',
                   'data': {'comp': 2.83333333313,
                            'data_to_ip': u'10.0.0.1',
                            'itfunc_dict': {u'f2': 2.83333333313},
                            'proc': 288.935318788,
                            's_tp': 6000,
                            'datasize': 0.5} }
      self.dummy_send(data_json)
    else: #send dummy_session_data
      dummy_data = ''
      for i in range(0, 2):
        dummy_data += 'dummydata dummydata '
      self.dummy_send(dummy_data)
  
def main():
  if len(sys.argv) != 3:
    raise RuntimeError('argv = [dst_addr, dst_lport]')
  dst_addr = sys.argv[1]
  dst_lport = int(sys.argv[2])
  #
  ds = DummySender(dst_addr, dst_lport)
  ds.test()
  #
  raw_input('Enter')
  
if __name__ == "__main__":
  main()
