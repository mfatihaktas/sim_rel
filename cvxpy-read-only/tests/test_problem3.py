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

# Test problem 3
class TestProblem3(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_problem3(self):
        a = [0.5,-0.5,0.2,-0.7,0.6,-0.2,0.7]	
        l=[10,5,5,5,10,5,10]
        f7w = np.linspace(a[0],a[0]*l[0],l[0],endpoint=True)
        for i in range(1,len(l),1):
            f7w = np.hstack((f7w,np.linspace(f7w[-1]+a[i],
                                               f7w[-1]+a[i]*l[i],
                                               l[i],
                                               endpoint=True)))
        f7w = matrix(f7w).T
        T=sum(l)
        grHigh_max=20.
        Pmg_min=-6.
        Pmg_max=6.
        free38=100.
        eta=0.1
        gamma=0.1
        grHigh = variable(T,1)
        Pmg = variable(T,1)
        Pbr = variable(T,1)
        E = variable(T+1,1)
        constr = []
        constr += [eq(f7w,grHigh + Pmg - Pbr)]
        constr += [geq(Pbr,0)]
        constr += [leq(0,grHigh),
                   leq(grHigh,grHigh_max)]
        constr += [leq(Pmg_min,Pmg),
                   leq(Pmg,Pmg_max)]
        for i in range(0,T,1):
            constr += [leq(E[i+1,0],E[i,0] - Pmg[i,0] - eta*abs(Pmg[i,0]))]
        constr += [leq(0,E),
                   leq(E,free38)]
        constr += [eq(E[0,0],E[T,0])]
        obj = sum(grHigh + gamma*square(grHigh))
        p = program(minimize(obj),constr)
        self.assertTrue(np.allclose(p.solve(True),326.331528,
                                    self.rtol,self.atol))
