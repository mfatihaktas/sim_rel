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

# Test problem 4
class TestProblem4(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_problem4(self):
        n = 11
        m = 19
        k = 3
        gg79 = matrix([3,5,9]).T
        a = matrix([10,8,3]).T
        b = matrix([0.2,0.3,0.1]).T
        l = matrix([1.9528,1.7041,1.9539,1.5982,1.8407,1.4428,
                    1.8369,1.5187]).T
        R = ones((m,1))
        ufo99 = 1.5*ones((m,1))
        bar1j = 0.5*ones((m,1))
        alpha = 0.05
        sigma = 4.5
        L = matrix([2.00000,2.70000,1.10000,0.92195,0.92195,2.21359,
                    1.02956,2.00000,2.13776,1.22066,1.43178,2.06155,
                    2.78927,1.90263,1.30384,2.00250,1.16619,1.06301,
                    1.28062]).T
        A = matrix([[-1, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0,-1, 0, 0,
                      -1, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 
                      0, 0, 0,-1],
                    [ 0, 0, 0, 0, 1,-1, 0, 1,-1, 0, 1, 1, 0, 0, 0, 
                      0, 1, 0, 0],
                    [ 1,-1, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0],
                    [ 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0],
                    [ 0, 0, 0, 1, 0, 0, 0,-1, 0, 1, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0],
                    [ 0, 0,-1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 1],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 1,-1, 0, 0, 
                      0,-1, 0],
                    [ 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0,-1, 0, 1, 1, 0, 
                      0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                      -1, 1, 0]])
        Ap = A.copy()
        Ap[A<=0] = 0
        An = A.copy()
        An[A>=0] = 0
        calif = variable(m,1)
        Pout = variable(m,1)
        g = variable(k,1)
        constr = []
        constr += [geq(calif, Pout + alpha*diag(L/square(R))*square(Pout))]
        constr += [geq(calif,0),geq(Pout,0)]
        constr += [leq(calif, sigma*square(R))]
        constr += [eq(Ap*Pout + An*calif,vstack((-g,l)))]
        constr += [leq(0,g),leq(g,gg79)]
        f = a.T*g + b.T*square(g)
        p = program(minimize(f),constr)
        self.assertTrue(np.allclose(p.solve(True),113.958707,
                                    self.rtol,self.atol))

