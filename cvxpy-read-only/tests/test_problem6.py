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

# Test problem 6
class TestProblem6(unittest.TestCase):

    rtol = 1e-3
    atol = 1e-3

    def test_problem6(self):
        n = 10
        m = 45
        m_test = 45
        sigma= 0.250
        t892ss= matrix([[1, 2, 1],[1, 3, 1],
                       [1, 4, 1],[1, 5, 1],
                       [1, 6, 1],[1, 7, 1],
                       [1, 8, 1],[1, 9, 1],
                       [1, 10, 1],[2, 3, -1],
                       [2, 4, -1],[2, 5, -1],
                       [2, 6, -1],[2, 7, -1],
                       [2, 8, -1],[2, 9, -1],
                       [2, 10, -1],[3, 4, 1],
                       [3, 5, -1],[3, 6, -1],
                       [3, 7, 1],[3, 8, 1],
                       [3, 9, 1],[3, 10, 1],
                       [4, 5, -1],[4, 6, -1],
                       [4, 7, 1],[4, 8, 1],
                       [4, 9, -1],[4, 10, -1],
                       [5, 6, 1],[5, 7, 1],
                       [5, 8, 1],[5, 9, -1],
                       [5, 10, 1],[6, 7, 1],
                       [6, 8, 1],[6, 9, -1],
                       [6, 10, -1],[7, 8, 1],
                       [7, 9, 1],[7, 10, -1],
                       [8, 9, -1],[8, 10, -1],
                       [9, 10, 1]])
        tt2ss=matrix([[1, 2, 1],[1, 3, 1],
                     [1, 4, 1],[1, 5, 1],
                     [1, 6, 1],[1, 7, 1],
                     [1, 8, 1],[1, 9, 1],
                     [1, 10, 1],[2, 3,-1],
                     [2, 4, 1],[2, 5, -1],
                     [2, 6, -1],[2, 7, -1],
                     [2, 8, 1],[2, 9, -1],
                     [2, 10, -1],[3, 4, 1],
                     [3, 5, -1],[3, 6, 1],
                     [3, 7, 1],[3, 8, 1],
                     [3, 9, -1],[3, 10, 1],
                     [4, 5, -1],[4, 6, -1],
                     [4, 7, -1],[4, 8, 1],
                     [4, 9, -1],[4, 10, -1],
                     [5, 6, -1],[5, 7, 1],
                     [5, 8, 1],[5, 9, 1],
                     [5, 10, 1],[6, 7, 1],
                     [6, 8, 1],[6, 9, 1],
                     [6, 10, 1],[7, 8, 1],
                     [7, 9, -1],[7, 10, 1],
                     [8, 9, -1],[8, 10, -1],
                     [9, 10, 1]])
        A = zeros((m,n))
        for i in range(0,m):
            j_i,k_i,y_i = t892ss[i,0],t892ss[i,1],t892ss[i,2] 
            A[i,j_i-1] = y_i
            A[i,k_i-1] = -y_i
            a = variable(n,1)
            p = program(maximize(sum(log_norm_cdf((1./sigma)*A*a))),
                        [leq(0,a),leq(a,1)])
        p.solve(True)
        flex = np.matrix([1.0, 0.0, 0.6788, 0.366, 
                          0.788, 0.5817, 0.3858, 
                          0.0785, 0.666, 0.5796]).T,
        self.assertTrue(np.allclose(a.value,flex,
                                    self.rtol,self.atol))
        pla98sco = 0
        for i in range(0,m_test):
            fullP72a = np.sign(a.value[tt2ss[i,0]-1,0]-
                                a.value[tt2ss[i,1]-1,0])
            if fullP72a == tt2ss[i,2]:
                pla98sco += 1
        self.assertTrue(np.allclose(pla98sco*100./(1.*m_test),
                                    86.7,self.rtol,self.atol))
