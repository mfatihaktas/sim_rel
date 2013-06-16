import socket, sys

def client(ip, port, message):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip, port))
  try:
      sock.sendall(message)
      response = sock.recv(1024)
      print "Received: {}".format(response)
  finally:
      sock.close()

# mininet mapping between sFlow ifIndex numbers and switch/port names
# This will be called by Controller and NetSensor will get this info from 
def map_ifi():
  ifi_to_dev = {};
  dev_to_port = {};
  dev_path = '/sys/devices/virtual/net/';
  devs = os.walk(dev_path).next()[1]

  for dev in devs:
    f = open(dev_path + dev + '/ifindex')
    ifi = (f.readlines())[0].strip()
    f.close()
    ifi_to_dev[ifi] = dev
    try:
      f=open(dev_path + dev + '/brport/port_no')
      port = (f.readlines())[0].strip('0x')
      f.close()
    except IOError:
      continue
    dev_to_port[dev] = port
    
  return (ifi_to_dev, dev_to_port)
  #print ifi_to_dev
  #print dev_to_port

def main():
  if len(sys.argv) != 3:
    raise RuntimeError('argv = [s_addr, s_port]')
  s_addr = sys.argv[1]
  s_port = int(sys.argv[2])
  client(s_addr, s_port, 'SOS 1')
  client(s_addr, s_port, 'SOS 2')
  client(s_addr, s_port, 'SOS 3')
  client(s_addr, s_port, 'SOS 4')

if __name__ == "__main__":
  main()
  
