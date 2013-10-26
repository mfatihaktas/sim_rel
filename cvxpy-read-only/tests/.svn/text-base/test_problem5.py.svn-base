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

# Test problem 5
class TestProblem5(unittest.TestCase):

    rtol = 1e-4
    atol = 1e-5

    def test_problem5(self):
        G = matrix([[1.0,0.1,0.2,0.1,0.0],
                    [0.1,1.0,0.1,0.1,0.0],
                    [0.2,0.1,2.0,0.2,0.2],
                    [0.1,0.1,0.2,1.0,0.1],
                    [0.0,0.0,0.2,0.1,1.0]])
        Gdiag = matrix(np.diag(np.diag(G)))
        Goff  = G - Gdiag
        p = variable(5,1)
        sigma = 0.5
        u = 1000.
        l = 0.
        tol = 1e-4
        while (u-l) > tol:
            t = (u+l)/2.
            constr = []
            constr += [geq(p,0),
                       leq(p,3),
                       leq(Goff*p + ones((5,1))*sigma, t*Gdiag*p),
                       leq(p[0,0]+p[1,0],4.),
                       leq(p[2,0]+p[3,0]+p[4,0],6),
                       leq(G*p,5.)]
            g = program(minimize(0),constr)
            opt = g.solve(True)
            if opt == 0.0:
                u = t
                pstar = p.value
            else:
                l = t
        fh2 = np.matrix([2.1188,1.8812,1.6444,2.3789,1.8011]).T
        self.assertTrue(np.allclose(pstar,fh2,
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(1/u,1.6884,
                                    self.rtol,self.atol))
