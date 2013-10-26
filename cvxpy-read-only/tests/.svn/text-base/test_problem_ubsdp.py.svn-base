#***********************************************************************#
# Copyright (C) 2010-2012 Tomas Tinoco De Rubira                        #
# Contributing author: Eugene Brevdo                                    #
#                                                                       #
# Most of this code is based extensively on the cvxopt example:         #
#  http://abel.ee.ucla.edu/cvxopt/examples/mlbook/ubsdp.html            #
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

class TestProblemUBSDP(unittest.TestCase):
    m = None
    n = None
    c = None
    A = None
    B = None
    Xubsdp = None

    def setUp(self):
        from cvxopt import matrix, normal, spdiag, misc, lapack
        from ubsdp import ubsdp

        m, n = 10, 10
        A = normal(m**2, n)

        # Z0 random positive definite with maximum e.v. less than 1.0.
        Z0 = normal(m,m)
        Z0 = Z0 * Z0.T
        w = matrix(0.0, (m,1))
        a = +Z0
        lapack.syev(a, w, jobz = 'V')
        wmax = max(w)
        if wmax > 0.9:  w = (0.9/wmax) * w
        Z0 = a * spdiag(w) * a.T

        # c = -A'(Z0)
        c = matrix(0.0, (n,1))
        misc.sgemv(A, Z0, c, dims = {'l': 0, 'q': [], 's': [m]}, trans = 'T', alpha = -1.0)

        # Z1 = I - Z0
        Z1 = -Z0
        Z1[::m+1] += 1.0

        x0 = normal(n,1)
        X0 = normal(m,m)
        X0 = X0*X0.T
        S0 = normal(m,m)
        S0 = S0*S0.T
        # B = A(x0) - X0 + S0
        B = matrix(A*x0 - X0[:] + S0[:], (m,m))

        X = ubsdp(c, A, B)

        (self.m, self.n, self.c, self.A, self.B, self.Xubsdp) = (m, n, c, A, B, X)

    def test_problem_ubsdp(self):

        # test problem needs review
        print 'skipping, needs review'
        return
        
        from cvxpy import (matrix, variable, program, minimize,
                           sum, abs, norm2, log, square, zeros, max,
                           hstack, vstack, eye, eq, trace, semidefinite_cone,
                           belongs, reshape)
        (m, n) = (self.m, self.n)
        c = matrix(self.c)
        A = matrix(self.A)
        B = matrix(self.B)
        Xubsdp = matrix(self.Xubsdp)
        tol_exp = 6

        # Use cvxpy to solve
        #
        # minimize  tr(B * X)
        # s.t.      tr(Ai * X) + ci = 0,  i = 1, ..., n
        #           X + S = I
        #           X >= 0,  S >= 0.
        #
        # c is an n-vector.
        # A is an m^2 x n-matrix.
        # B is an m x m-matrix.
        X = variable(m, n)
        S = variable(m, n)
        constr = [eq(trace(reshape(A[:,i], (m, m)) * X) + c[i,0], 0.0)
                  for i in range(n)]
        constr += [eq(X + S, eye(m))]
        constr += [belongs(X, semidefinite_cone),
                   belongs(S, semidefinite_cone)]
        p = program(minimize(trace(B * X)), constr)
        p.solve(True)
        np.testing.assert_array_almost_equal(
            X.value, self.Xubsdp, tol_exp)

        # Use cvxpy to solve
        #
        # minimize  tr(B * X)
        # s.t.      tr(Ai * X) + ci = 0,  i = 1, ..., n
        #           0 <= X <= I
        X2 = variable(m, n)
        constr = [eq(trace(reshape(A[:,i], (m, m)) * X2) + c[i,0], 0.0)
                  for i in range(n)]
        constr += [belongs(X2, semidefinite_cone),
                   belongs(eye(m) - X2, semidefinite_cone)]
        p = program(minimize(trace(B * X2)), constr)
        p.solve(True)
        np.testing.assert_array_almost_equal(
            X2.value, X.value, tol_exp)

    def tearDown(self):
        pass
