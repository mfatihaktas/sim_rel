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

# Test problem 1
class TestProblem1(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_problem1(self):
        x = matrix([0.1,0.2,-0.05,0.1]).T
        S = variable(4,4)
        constr = []
        constr += [eq(S[0,0],0.2),
                   geq(S[0,1],0),
                   geq(S[0,2],0),
                   geq(S[1,0],0),
                   eq(S[1,1],0.1),
                   leq(S[1,2],0),
                   leq(S[1,3],0),
                   geq(S[2,0],0),
                   leq(S[2,1],0),
                   eq(S[2,2],0.3),
                   geq(S[2,3],0),
                   leq(S[3,1],0),
                   geq(S[3,2],0),
                   eq(S[3,3],0.1)]
        constr += [belongs(S,semidefinite_cone),eq(S,S.T)]
        p = program(maximize(x.T*S*x),constr)
        self.assertTrue(np.allclose(p.solve(True),0.0151662,
                                    self.rtol,self.atol))
