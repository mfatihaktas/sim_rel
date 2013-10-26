#***********************************************************************#
# Copyright (C) 2010-2012 Tomas Tinoco De Rubira                        #
# Contributing author: Eugene Brevdo                                    #
#                                                                       #
# Most of this code is based extensively on the cvxopt example:         #
#  http://abel.ee.ucla.edu/cvxopt/examples/book/huber.html              #
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
from resources import open_resource
from cPickle import load

class TestRobustRegression(unittest.TestCase):
    xh = None
    A = None
    b = None

    def setUp(self):
        #
        # Use cvxopt to get ground truth values
        #
        from cvxopt import solvers, lapack, matrix, spmatrix
        solvers.options['show_progress'] = 0
        solvers.options['feastol'] = 1e-9
        solvers.options['abstol'] = 1e-9
        solvers.options['reltol'] = 1e-8

        data = load(open_resource('huber.bin','rb'))
        u, v = data['u'], data['v']
        m, n = len(u), 2

        A = matrix( [m*[1.0], [u]] )
        b = +v
        self.m, self.n, self.A, self.b = m, n, A, b

        # Robust least squares.
        #
        # minimize  sum( h( A*x-b ))
        #
        # where h(u) = u^2           if |u| <= 1.0
        #            = 2*(|u| - 1.0) if |u| > 1.0.
        #
        # Solve as a QP (see exercise 4.5):
        #
        # minimize    (1/2) * u'*u + 1'*v
        # subject to  -u - v <= A*x-b <= u + v
        #             0 <= u <= 1
        #             v >= 0
        #
        # Variables  x (n), u (m), v(m)
        novars = n+2*m
        P = spmatrix([],[],[], (novars, novars))
        P[n:n+m,n:n+m] = spmatrix(1.0, range(m), range(m))
        q = matrix(0.0, (novars,1))
        q[-m:] = 1.0

        G = spmatrix([], [], [], (5*m, novars))
        h = matrix(0.0, (5*m,1))

        # A*x - b <= u+v
        G[:m,:n] = A
        G[:m,n:n+m] = spmatrix(-1.0, range(m), range(m))
        G[:m,n+m:] = spmatrix(-1.0, range(m), range(m))
        h[:m] = b

        # -u - v <= A*x - b
        G[m:2*m,:n] = -A
        G[m:2*m,n:n+m] = spmatrix(-1.0, range(m), range(m))
        G[m:2*m,n+m:] = spmatrix(-1.0, range(m), range(m))
        h[m:2*m] = -b

        # u >= 0
        G[2*m:3*m,n:n+m] = spmatrix(-1.0, range(m), range(m))

        # u <= 1
        G[3*m:4*m,n:n+m] = spmatrix(1.0, range(m), range(m))
        h[3*m:4*m] = 1.0

        # v >= 0
        G[4*m:,n+m:] = spmatrix(-1.0, range(m), range(m))

        self.xh = solvers.qp(P, q, G, h)['x'][:n]

    def test_robust_regression(self):
        #
        # Compare cvxpy solutions to cvxopt ground truth
        #
        from cvxpy import (matrix, variable, program, minimize,
                           huber, sum, leq, geq, square, norm2,
                           ones, zeros, quad_form)
        tol_exp = 5 # Check solution to within 5 decimal places
        m, n = self.m, self.n
        A = matrix(self.A)
        b = matrix(self.b)

        # Method 1: using huber directly
        x = variable(n)
        p = program(minimize(sum(huber(A*x - b, 1.0))))
        p.solve(True)

        np.testing.assert_array_almost_equal(
            x.value, self.xh, tol_exp)

        # Method 2: solving the dual QP
        x = variable(n)
        u = variable(m)
        v = variable(m)
        p = program(minimize(0.5*quad_form(u, 1.0) + sum(v)),
                    [geq(u, 0.0), leq(u, 1.0), geq(v, 0.0),
                     leq(A*x - b, u + v), geq(A*x - b, -u - v)])
        p.solve(True)
        np.testing.assert_array_almost_equal(
            x.value, self.xh, tol_exp)

    def tearDown(self):
        pass