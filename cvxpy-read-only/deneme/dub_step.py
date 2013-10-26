import numpy as np
from cvxpy.defs import *
from cvxpy.utils import *
from cvxpy.interface import *
from cvxpy.arrays import cvxpy_array
from cvxpy.arrays import cvxpy_matrix

# dub_step
def dub_step(x):
    #print 'input: ', x
    #print 'input.value: ', x.value
    #
    # Prepare input
    if (np.isscalar(x) or 
        type(x).__name__ in SCALAR_OBJS):
        arg = vstack([x])
    elif (type(x) is cvxpy_matrix or
          type(x).__name__ in ARRAY_OBJS):
        arg = x
    else:
        raise TypeError('Invalid argument')

    # Prepare output
    if type(arg) is cvxpy_matrix:
        output = zeros(arg.shape)
    else:
        output = cvxpy_array(arg.shape[0],arg.shape[1])
    
    # helper parameter
    p =  parameter(name = 'p')
    
    # Construct program
    for i in range(0,arg.shape[0],1):
        for j in range(0,arg.shape[1],1):
            t = variable()
            v = variable()
            p = program(minimize(t),
                        [less_equals(v,t),less_equals(-t,v)],
                        [v],
                        name='abs')
            output[i,j] = p(arg[i,j])
            """
            print 'arg[0,0]: ', arg[0,0]
            print 'arg[0,0].value: ', arg[0,0].value
            if arg[0,0].value >= 0:
              p.value = 1
              output[i,j] = p
            else:
              p.value = -1
              output[i,j] = p
            """
    # Return output
    if output.shape == (1,1):
        return output[0,0]
    else:
        return output
