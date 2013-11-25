from control_comm_intf import ControlCommIntf
#

def recv_data_handler(data):
  print 'recved data=%s' % data

def main():
  cci = ControlCommIntf()
  cci.reg_commpair('scher-acter','udp',recv_data_handler,('127.0.0.1',7000),('127.0.0.1',6000))
  #
  raw_input('Enter')
  
if __name__ == "__main__":
  main()
