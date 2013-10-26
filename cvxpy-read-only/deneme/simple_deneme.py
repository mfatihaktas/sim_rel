import numpy as np

"""
def norm_square(v):
  vs = v.shape
  print 'vs: ', vs
  if vs[1] != 1:
    print 'vector shape is not suitable for norm_square'
    sys.exit()
  #
  r_ = 0
  for i in range(0,vs[0]):
    r_ += v[i]**2
  
  return r_
"""

def tt_time(data_amount, max_bw, max_proc, num_func):
  tx_time =  data_amount * 1000/max_bw # in (ms)
  tfc = num_func #total_func_comp(1)
  proc_time = data_amount * 1000*(tfc**2)/max_proc # in (ms)
  trans_time = tx_time + proc_time #+ path_latency
  
  return trans_time

def main():
  print 'tt_time(2, 10, 50, 2): ', tt_time(2, 10, 50, 2)
  '''
  v = np.array([[1, 2, 3]]).T
  
  ns = norm_square(v)
  print 'ns: ', ns
  '''
  
  
if __name__ == "__main__":
  main()
