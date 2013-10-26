#***********************************************************************#
# Copyright (C) 2010-2012 Tomas Tinoco De Rubira                        #
#                                                                       #
# This file is part of CVXPY                                            #     
#                                                                       #
# CVXPY is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #   
# (at your option) any later version.                                   # 
#                                                                       #
# CVXPY is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#***********************************************************************#

import unittest
import numpy as np
from cvxpy import *

# Test problem 2
class TestProblem2(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_problem2(self):
        S = matrix([[1, 0, 0, 0, 0, 0],	
                    [-1,1, 0, 0, 0, 0], 
                    [-1,0, 1, 0, 0, 0], 
                    [0,-1, 0, 2,-1, 0],	
                    [0, 0, 0, 0, 1, 0],	
                    [0,-2, 1, 0, 0, 1], 
                    [0,	0,-1, 1, 0, 0],	
                    [0,	0, 0, 0, 0,-1],	
                    [0, 0, 0,-1, 0, 0]]).T
        (m,n) = S.shape
        vmax = matrix([10.10,
                       100,    
                       5.90,	
                       100,	
                       3.70,   
                       100,	
                       100,	
                       100,
                       100]).T
        v = variable(n,1)
        constr = [eq(S*v,0),
                  geq(v,0),
                  leq(v,vmax)]
        obj = v[n-1,0]
        p = program(maximize(obj),constr)
        self.assertTrue(np.allclose(p.solve(True),13.55,
                               self.rtol,self.atol))
        Gmin= 0.2*p.objective.value
        G = zeros((n,n))
        for i in range(0,n,1):
            for j in range(0,n,1):
                p1 = program(maximize(obj),
                     constr+[eq(v[i,0],0),
                             eq(v[j,0],0)],[v[i,0],v[j,0]])
                G[i,j] = p1(0,0)
        foo = []
        for i in range(0,n,1):
            if G[i,i] < Gmin:
                foo += [i+1]
        self.assertEqual(foo,[1,9])
        foo = []
        for i in range(0,n,1):
            for j in range(0,i,1):
                if (i!=j and G[i,j] < Gmin and
                    G[i,i] >= Gmin and G[j,j] >= Gmin):
                    foo += [(i+1,j+1)]
        self.assertEqual(foo,[(3,2),(7,2),(7,4),(7,5)])
