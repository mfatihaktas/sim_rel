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

# Test problem 7
class TestProblem7(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_problem7(self):
        seed(2)
        A = randn(50,5)
        b = 20*randn(50,1)
        G = randn(10,5)
        h = 5*randn(10,1)
        alpha = 60
        x = variable(5,1)
        p = program(minimize(norm2(A*x-b)),
                    [leq(norm1(G*x-h),alpha),
                     geq(x,1)])
        self.assertTrue(np.allclose(p.solve(True),138.06906942,
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,
                                    np.matrix([0.99999988,
                                               0.99999994,
                                               1.92943244,
                                               0.99999996,
                                               1.11037549]).T,
                                    self.rtol,self.atol))
