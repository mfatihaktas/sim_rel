#***********************************************************************#
# Copyright (C) 2010-2012 Tomas Tinoco De Rubira                        #
# Contributing author: Eugene Brevdo                                    #
#                                                                       #
# Most of this code is based extensively on the cvxopt example:         #
#  http://abel.ee.ucla.edu/cvxopt/examples/mlbook/robsvm.html           #
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

class TestProblemRobSVM(unittest.TestCase):


    def setUp(self):
        from robsvm import robsvm
        from cvxopt import matrix, normal, uniform, spmatrix, solvers
        solvers.options['show_progress'] = 0

        # parameters
        m, n = 60, 2
        gamma = 10.0

        # generate random problem data
        X = 2.0*uniform(m,n)-1.0
        d = matrix(1,(m,1))

        # generate noisy labels
        w0 = matrix([2.0,1.0])+normal(2,1); b0 = 0.4
        z = 0.2*normal(m,1)
        for i in range(m):
            if (X[i,:]*w0)[0] + b0 < z[i]: d[i] = -1

        # generate uncertainty ellipsoids
        k = 2
        P = [0.1*normal(4*n,n) for i in range(k)]
        P = [ p.T*p for p in P]
        e = matrix(0,(m,1))
        for i in xrange(m):
            if d[i] == -1: e[i] = 1

        # solve SVM training problem
        w, b, u, v, iterations = robsvm(X, d, gamma, P, e)

        (self.w, self.b, self.u, self.v, self.k, self.m, self.n,
         self.X, self.d, self.gamma, self.P, self.e) = (
             w, b, u, v, k, m, n, X, d, gamma, P, e)

    def test_problem_robsvm(self):
        
        # test problem needs review
        print 'skipping, needs review'
        return 
        
        from cvxpy import (matrix, variable, program, minimize,
                           sum, abs, norm2, log, square, zeros, max,
                           semidefinite_cone, belongs, geq, diag, quad_form)

        tol_exp = 6

        # Use cvxpy to solve the following robust SVM training problem:
        #
        #        minimize    (1/2) w'*w + gamma*sum(v)
        #        subject to  diag(d)*(X*w + b*1) >= 1 - v + E*u
        #                    || S_j*w ||_2 <= u_j,  j = 1...t
        #                    v >= 0
        #
        # The variables are w, b, v, and u. The matrix E is a selector
        # matrix with zeros and one '1' per row.  E_ij = 1 means that the
        # i'th training vector is associated with the j'th uncertainty
        # ellipsoid.
        #
        X = matrix(self.X)
        d = matrix(self.d)
        e = self.e
        (k, m, n) = (self.k, self.m, self.n)
        gamma = self.gamma
        P = [matrix(p) for p in self.P]

        E = zeros((m,k))
        for j in range(m): E[j, e[j]] = 1.

        w = variable(n)
        b = variable()
        v = variable(m)
        u = variable(k)

        constr = [geq(diag(d)*(X*w + b), 1 - v + E*u),
                  geq(v, 0)]
        constr += [geq(u[j,0], norm2(P[j]*w)) for j in range(k)]

        p = program(minimize(0.5*quad_form(u, 1.0) + gamma*sum(v)),
                    constr)
        p.solve(True)

        np.testing.assert_array_almost_equal(
            u.value, self.u, tol_exp)
        np.testing.assert_array_almost_equal(
            b.value, self.b, tol_exp)
        np.testing.assert_array_almost_equal(
            v.value, self.v, tol_exp)
        np.testing.assert_array_almost_equal(
            w.value, self.w, tol_exp)

    def tearDown(self):
        pass
