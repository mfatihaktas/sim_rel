from cvxpy import *
import pylab
from dub_step import *
"""
x = variable(name='x', attribute='nonnegative')

t_exp = 1-(x-1)+power_p(x-1, 2)-power_p(x-1, 3)+power_p(x-1, 4) \
        -power_p(x-1, 5)+power_p(x-1, 6)-power_p(x-1, 7)

print 't_exp: ', t_exp
print 't_exp.is_convex(): ', t_exp.is_convex()
"""
"""
x = variable(name='x')
x.value = 2
y = variable(name='y')
y.value = 2

exp = exp(-1*x)
f = quad_over_lin(1,y)
g = -log(x)
h = power_pos(g, 2)
print 'g.is_convex(): ', g.is_convex()
print 'h.is_convex(): ', h.is_convex()
print 'h: ', h

print 'exp.is_convex(): ', exp.is_convex()
print 'f: ', f
print 'f.is_convex(): ', f.is_convex()
"""
def gl(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = quad_over_lin(1, p) - 1
  y[1,0] = 0
  exp = max(y)
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def gr(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = quad_over_lin(1, p) - 1
  y[1,0] = 0
  exp = -1*min(y)
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def f0(val):
  p =  parameter(name = 'p')
  exp = power_pos(quad_over_lin(1, quad_over_lin(1, p)), 2)
  #exp = power_pos(quad_over_lin(1, p), 2)
  #exp = quad_over_lin(1, p)
  p.value = val
  return exp.value

def d0(val = None):
  p =  parameter(name = 'p')
  exp = power_p(p-1, 1)
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def ds(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = p-1
  y[1,0] = 0
  exp = min(y)
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def h0(val = None):
  p =  parameter(name = 'p')
  exp = power_p(p-1, 1)
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def func0(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = p-1
  y[1,0] = 0
  exp_ = min(y)*power_p(p-1, 1)
  #
  z =  parameter(2,1,name = 'p')
  z[0,0] = quad_over_lin(1, p) - 1
  z[1,0] = 0
  exp = -1*min(z)+exp_
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value
    
def hgl(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = quad_over_lin(1, p) - 1
  y[1,0] = 0
  exp_ = max(y)
  #
  exp = quad_over_lin(1, -1*(exp_-2))
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def hgr(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = p-1
  y[1,0] = 0
  exp_ = min(y)*power_p(p-1, 1)
  #
  z =  parameter(2,1,name = 'p')
  z[0,0] = quad_over_lin(1, p) - 1
  z[1,0] = 0
  exp__ = -1*min(z)+exp_
  #
  exp = quad_over_lin(1, exp__)-1
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def hgl1(val = None):
  p =  parameter(name = 'p')
  y =  parameter(2,1,name = 'p')
  y[0,0] = quad_over_lin(1, p) - 1
  y[1,0] = 0
  exp_ = max(y)
  #
  exp = power_pos(100*exp_,1)
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def hgr1(val = None):
  #p =  parameter(name = 'p', attribute = 'nonnegative')
  p = variable(name = 'p')
  '''
  y =  parameter(2,1,name = 'y')
  y[0,0] = p-1
  y[1,0] = 0
  exp_ = min(y)*power_p(p-1, 1)
  #
  z =  parameter(2,1,name = 'z')
  z[0,0] = quad_over_lin(1, p) - 1
  z[1,0] = 0
  exp__ = -1*min(z) #max(y)#*-1*min(z) #+exp_
  #exp = quad_over_lin(1, -1*(exp__-1))
  #quad_over_lin(1, -1*(p-1))-1 #exp__
  #(-1*power_pos(p, 1))*min(z)
  '''
  '''
  quad_over_lin(p, abs(p))
  power_pos(abs(p), 2) #convex x^2
  '''
  '''
  exp_1 = quad_over_lin(1, p) - 5
  exp_2 = -quad_over_lin(1, p)
  #quad_over_lin(1, quad_over_lin(1, abs(p)) )
  #square(exp_1)
  h_exp_1 = max( vstack((p, 0)) )
  exp = abs(quad_over_lin(1, abs(p)) - 5) * p
  '''
  D = 1 #Mb
  L = 10 #ms
  C = 3
  bw = variable(name = 'bw')
  proc = variable(name = 'proc')
  dur = variable(name = 'dur')
  trans_t = D*quad_over_lin(1, bw)+L+D*C*quad_over_lin(1, proc)+dur
  #
  exp = bw*proc
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def hgl1_p_hgr1(val = None):
  p =  parameter(name = 'p')
  # hgl1
  x =  parameter(2,1,name = 'x')
  x[0,0] = quad_over_lin(1, p) - 1
  x[1,0] = 0
  hgl_exp_ = max(x)
  hgl_exp = power_pos(100*hgl_exp_,1)
  # hgr1
  y =  parameter(2,1,name = 'y')
  y[0,0] = p-1
  y[1,0] = 0
  hgr_exp_ = min(y)*power_p(p-1, 1)
  z =  parameter(2,1,name = 'z')
  z[0,0] = quad_over_lin(1, p) - 1
  z[1,0] = 0
  hgr_exp__ = -1*min(z)+hgr_exp_
  hgr_exp = power_pos(100*hgr_exp__,1)
  # hgl + hgr
  q =  parameter(2,1,name = 'q')
  q[0,0] = hgl_exp
  q[1,0] = hgr_exp
  exp = max(q)
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value


def hgl_p_hgr(val = None):
  p =  parameter(name = 'p')
  # hgl
  x =  parameter(2,1,name = 'p')
  x[0,0] = quad_over_lin(1, p) - 1
  x[1,0] = 0
  hgl_exp_ = max(x)
  hgl_exp = quad_over_lin(1, -1*(hgl_exp_-2))
  # hgr
  y =  parameter(2,1,name = 'p')
  y[0,0] = p-1
  y[1,0] = 0
  hgr_exp_ = min(y)*power_p(p-1, 1)
  z =  parameter(2,1,name = 'p')
  z[0,0] = quad_over_lin(1, p) - 1
  z[1,0] = 0
  hgr_exp__ = -1*min(z)+hgr_exp_
  hgr_exp = quad_over_lin(1, hgr_exp__)-1
  # hgl + hgr
  exp = hgl_exp + hgr_exp
  
  if val == None: #return exp mode on
    return exp
  else:
    p.value = val
    return exp.value

def pen(val = None):
  #p =  parameter(name = 'p', attribute = 'nonnegative')
  p = variable(name = 'p')
  #
  #expr_ = exp(p)
  #expr = max( vstack((expr_-1, 0)) )
  #expr = min( vstack((-1*(p-1), 0)) )
  #
  expr_ = quad_over_lin(1,p)
  expr = quad_over_lin(expr_, 1)
  
  if val == None: #return exp mode on
    return expr
  else:
    p.value = val
    return expr.value

def print_func(func, file_name):
  var_vals = pylab.arange(-20, 20, 0.21) #0.1
  func_val_list = []
  print "for func: ", file_name ,"x, y: "
  for val in var_vals:
    y = func(val)
    print "{}, {}".format(val, y)
    func_val_list.append(y)
    
  pylab.plot(var_vals, func_val_list, 'b')
  pylab.title("")
  pylab.xlabel("x")
  pylab.ylabel("F(x)")
  pylab.grid()
  pylab.savefig(file_name + '.png')
  pylab.show()
  pylab.close()
#####################################################
# attribute = 'nonnegative'
def tx_time(data_amount):
  # data_amount in (Mb)
  # bw = x in (Mbps)
  return 1000*data_amount*quad_over_lin(1, x)

def obj():
  return square(tx_time(1) - slack_time)

def main():
  """
  x =  variable(3,1,name = 'x')
  exp_1 = quad_over_lin(1, x[0,0])
  exp_2 = quad_over_lin(1, x[1,0])
  exp_3 = quad_over_lin(1, x[2,0])
  exp = exp_1 #- (exp_2 + exp_3)
  print 'exp.is_convex(): ', exp.is_convex()
  """
  """
  t =  variable(name = 't')
  p =  parameter(name = 'p', attribute = 'nonnegative')
  data_amount = 1
  slack_time = 40
  #
  tx_time = 1000*data_amount*quad_over_lin(1, p)
  obj = square(tx_time - slack_time)
  #
  print 'obj: ', obj
  print 'obj.is_convex(): ', obj.is_convex()
  #
  prog = program(minimize(obj),
                  [
                    leq(p, 100)
                  ]
                 )
  prog.solve()
  """
  '''
  prog = program(minimize(t),
              [
                leq(obj, t),
                leq(p, 100)
              ]
             )
  '''
  """
  #prog.solve()
  prog.show()
  print 'optimal point: '
  print 'p: \n', p.value
  print 'optimal value: '
  print 'obj: \n', obj.value
  """
  #print 'gl().is_convex(): ', gl().is_convex()
  #print 'gr().is_convex(): ', gr().is_convex()
  #print 'd0().is_convex(): ', d0().is_convex()
  #print 'func0().is_concave(): ', func0(None).is_concave()
  #print 'hgr().is_convex(): ', hgr().is_convex()
  #print 'hgl().is_convex(): ', hgl().is_convex()
  #print 'hgl_p_hgr().is_convex(): ', hgl_p_hgr().is_convex()
  
  print 'pen().is_convex(): ', pen().is_convex()
  print 'pen().is_concave(): ', pen().is_concave()
  
  #print 'hgr1().is_concave(): ', hgr1().is_concave()
  #print 'hgl1().is_convex(): ', hgl1().is_convex()
  #print 'hgl1_p_hgr1().is_convex(): ', hgl1_p_hgr1().is_convex()
  #
  #print 'func0: ', func0(None)
  #print 'hgr: ', hgr(None)
  #print 'hgl: ', hgl(None)
  #print 'hgl_p_hgr: ', hgl_p_hgr(None)
  
  print 'pen: ', pen()
  
  #print 'hgl1: ', hgl1(None)
  #print 'hgl1_p_hgr1: ', hgl1_p_hgr1(None)
  #
  print_func(pen, 'pen')
  #print_func(d0, 'd0')
  #print_func(gl, 'gl')
  #print_func(gr, 'gr')
  #print_func(ds, 'ds')
  #print_func(h0, 'h0')
  #print_func(func0, 'func0')
  #print_func(hgr, 'hgr')
  #print_func(hgl, 'hgl')
  #print_func(hgl_p_hgr, 'hgl_p_hgr')
  
  #print_func(hgr1, 'hgr1')
  
  #print_func(hgl1, 'hgl1')
  #print_func(hgl1_p_hgr1, 'hgl1_p_hgr1')
  
  #print 'ds(2): ', ds(2)
  #print 'ds(-2): ', ds(-2)
  
if __name__ == "__main__":
  main()
