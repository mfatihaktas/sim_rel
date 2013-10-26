from cvxpy import *

N = 3 # number of active transport sessions
# optimization variable matrix
a = variable(5,N, name='a')
#print 'a[0,0]:', a[0,0].value
# resource allocation matrix
k = 10 # number of actual resources
r = parameter(k,N, name='r')
"""
  Actual resource info dict: r_info_dict; key:device_id
  --
  net_links btw in-transit resources and sws are out of problem formulation.
  --
  bw in Mbps, proc in Mflop/s, stor in MB
  --
"""
r_info_dict = {
  0:{'type': 'net_link', 'C':{'bw':100,'proc':0,'stor':0}},
  1:{'type': 'net_link', 'C':{'bw':100,'proc':0,'stor':0}},
  2:{'type': 'net_link', 'C':{'bw':100,'proc':0,'stor':0}},
  3:{'type': 'net_link', 'C':{'bw':100,'proc':0,'stor':0}},
  4:{'type': 'net_link', 'C':{'bw':100,'proc':0,'stor':0}},
  301:{'type': 'it_host', 'C':{'bw':0,'proc':100,'stor':100}},
  302:{'type': 'it_host', 'C':{'bw':0,'proc':100,'stor':100}},
  303:{'type': 'it_host', 'C':{'bw':0,'proc':100,'stor':100}},
  401:{'type': 'it_host', 'C':{'bw':0,'proc':100,'stor':100}},
  402:{'type': 'it_host', 'C':{'bw':0,'proc':100,'stor':100}},
  403:{'type': 'it_host', 'C':{'bw':0,'proc':100,'stor':100}},
}
"""
  Actual resource capacity matrix
  Every column vector represents [trans, proc, stor] capacity in order
  numpy matrix can be used !!!
"""
# C = parameter(3,k, name='r')

"""
  Necessary session and modeling info will be kept in arrays or matrices.
  e.g. 
  - slack_time, data_amount, latency
  - func_dict, func_comp_constant_dict
"""
# slack_time_dict in ms
slack_time_dict = {
  0:100,
  1:200,
  2:150
}
#print '1/slack_time[:,1]: ', 1/slack_time[:,1]
#print 'slack_time[:,0]/slack_time[:,1]: ', slack_time[:,0]/slack_time[:,1]
#print 'leq(slack_time[:,2],10): ', leq(slack_time[:,2],10)

# data_amount_dict in MB
data_amount_dict = {
  0:1,
  1:2,
  2:1.5
}

# latency_dict in ms
latency_dict = {
  0:100,
  1:100,
  2:100
}

# func_dict; key:session_num
func_dict = {
  0:['f1','f2','f3'],
  1:['f3','f2'],
  2:['f2','f1','f3','f4']
}

# func_comp_constant_dict; key:function, val:comp_constant (2-8)
func_comp_constant_dict = {
  'f1':2,
  'f2':4,
  'f3':2.5,
  'f4':5
}

# modeling functions
def R_hard(session_num, scol_a):
  """
  def total_func_comp(func_num):
    comp = 0
    cnt = 0
    func_list = func_dict[session_num]
    while cnt < func_num:
      comp = comp + func_comp_constant_dict[func_list[cnt]]
      cnt = cnt + 1
    return comp
  """
  # for now assume func_com for ever func is 1
  tx_time = data_amount_dict[session_num]*quad_over_lin(1, scol_a[0,:])
  tfc = scol_a[4,:]#total_func_comp(1)
  proc_time = data_amount_dict[session_num]*quad_over_lin(tfc, scol_a[1,:])
  stage_time = scol_a[3,:]
  trans_time = tx_time + proc_time + stage_time
  #print 'trans_time.is_convex():', trans_time.is_convex()
  total_time = trans_time-slack_time_dict[session_num]
  #print 'total_time: ', total_time
  return  power_pos(total_time, 2)

def R_soft(session_num, scol_a):
  n = scol_a[4,:]
  func_list = func_dict[session_num]
  return n*pow(len(func_list),-1)

# modeling penalty and utility functions
"""
  Assumptions for simplicity of the initial modeling attempts;
  * Penalty and utility functions are linear functions passing through
  origin and can be defined by only its 'slope'
  p_s: penalty func slope
  u_s: utility func slope
  
  App requirements will be reflected to the optimization problem by
  auto-tune of penalty and utility functions (look at report for more)
  In this case, three coupling types will tune 'function slopes' as;
  Tight Coupling: p_s >> u_s
  Loose Coupling: p_s ~ u_s
  Dataflow Coupling: p_s << u_s
"""
s_dict = {
  0:{'p':0.9, 'u':0.1},
  1:{'p':0.5, 'u':0.5},
  2:{'p':0.1, 'u':0.9}
}

# objective function
def F0(a):
  s_num = 0
  r_func = 0
  while s_num < N:
    r_func = r_func + s_dict[s_num]['p']*R_hard(s_num, a[:,s_num])
    s_num = s_num + 1
  return r_func

def F1(a):
  s_num = 0
  r_func = 0
  while s_num < N:
    r_func = r_func + s_dict[s_num]['u']*R_soft(s_num, a[:,s_num])
    s_num = s_num + 1
  return -1*r_func

def main():
  '''
  global a
  F = F0(a)+F1(a)
  #print 'F: \n', F
  #print 'a: \n', a
  #print 'F0(a).is_convex(): ', F0(a).is_convex()
  #print 'F1(a).is_convex(): ', F1(a).is_convex()
  print 'F.is_convex(): ', F.is_convex()
  '''
  dur = variable(name='dur')
  stor = variable(name='stor')
  bw = variable(name='bw')
  stor_p = parameter(name='stor_p', attribute = 'nonnegative')
  bw_p = parameter(name='bw_p', attribute = 'nonnegative')
  #exp= stor*bw
  #e_1 = power_p(bw,2)
  #dur*bw #quad_over_lin(stor, e_1)
  #x = variable(2,1, name='x')
  #exp_ = geo_mean(x)
  #exp_ = square( geo_mean(vstack( (dur, bw) )) )
  x = variable(name='x')
  y = variable(name='y')
  #exp_ = square(x+y)-square(x)-square(y)
  exp_ = y*2*exp(x) #square(x+y)-sqrt(x)-sqrt(y)
  '''
  print 'bw_p: ', bw_p
  prog = program(minimize(dur),
                  [
                    geq(stor, 0),
                    geq(bw, 0),
                    geq(dur, 0),
                    leq(stor, 100),
                    leq(bw, 10),
                    leq(dur, 10),
                    leq(stor, bw_p*dur)
                  ]
                 )
  print 'prog: \n'
  prog.show()
  print 'prog.is_dcp(): ', prog.is_dcp()
  prog.solve()
  print 'optimal point: \n'
  print 'dur: ', dur.value
  print 'stor: ', stor.value
  print 'bw: ', bw.value
  '''
  print 'exp_: ', exp_
  print 'exp_.is_convex(): ', exp_.is_convex()
  print 'exp_.is_concave(): ', exp_.is_concave()
  
  
  
  
  
  
  
  
  
  
if __name__ == "__main__":
  main()  
 

