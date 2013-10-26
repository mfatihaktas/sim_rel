#***********************************************************************#
# Copyright (C) 2010-2012 Tomas Tinoco De Rubira                        #
# Contributing author: Eugene Brevdo                                    #
#                                                                       #
# Most of this code is based extensively on the cvxopt example:         #
#  http://abel.ee.ucla.edu/cvxopt/examples/book/expdesign.html          #
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

class TestProblemExpDesign(unittest.TestCase):
    def setUp(self):
        from cvxopt import (matrix, normal, spdiag, misc, lapack, spmatrix,
                            solvers, log, blas)
        solvers.options['show_progress'] = 0

        V = matrix([-2.1213,    2.1213,
                    -2.2981,    1.9284,
                    -2.4575,    1.7207,
                    -2.5981,    1.5000,
                    -2.7189,    1.2679,
                    -2.8191,    1.0261,
                    -2.8978,    0.7765,
                    -2.9544,    0.5209,
                    -2.9886,    0.2615,
                    -3.0000,    0.0000,
                    1.5000,    0.0000,
                    1.4772,   -0.2605,
                    1.4095,   -0.5130,
                    1.2990,   -0.7500,
                    1.1491,   -0.9642,
                    0.9642,   -1.1491,
                    0.7500,   -1.2990,
                    0.5130,   -1.4095,
                    0.2605,   -1.4772,
                    0.0000,   -1.5000 ], (2,20))

        n = V.size[1]
        G = spmatrix(-1.0, range(n), range(n))
        h = matrix(0.0, (n,1))
        A = matrix(1.0, (1,n))
        b = matrix(1.0)

        # D-design
        #
        # minimize    f(x) = -log det V*diag(x)*V'
        # subject to  x >= 0
        #             sum(x) = 1
        #
        # The gradient and Hessian of f are
        #
        #     gradf = -diag(V' * X^-1 * V)
        #         H = (V' * X^-1 * V)**2.
        #
        # where X = V * diag(x) * V'.
        def F(x=None, z=None):
            if x is None: return 0, matrix(1.0, (n,1))
            X = V * spdiag(x) * V.T
            L = +X
            try:
                lapack.potrf(L)
            except ArithmeticError: return None
            f = - 2.0 * (log(L[0,0])  + log(L[1,1]))
            W = +V
            blas.trsm(L, W)
            gradf = matrix(-1.0, (1,2)) * W**2
            if z is None: return f, gradf
            H = matrix(0.0, (n,n))
            blas.syrk(W, H, trans='T')
            return f, gradf, z[0] * H**2

        xd = solvers.cp(F, G, h, A = A, b = b)['x']

        (self.V, self.xd) = (V, xd)

    def test_problem_expdesign(self):

        # test problem needs review
        print 'skipping, needs review'
        return
        
        from cvxpy import (matrix, variable, program, minimize,
                           log, det_rootn, diag, sum, geq, eq, zeros)
        tol_exp = 6
        V = matrix(self.V)
        n = V.shape[1]
        x = variable(n)

        # Use cvxpy to solve the problem above
        p = program(minimize(-log(det_rootn(V*diag(x)*V.T))),
                    [geq(x, 0.0), eq(sum(x), 1.0)])
        p.solve(True)
        np.testing.assert_array_almost_equal(
            x.value, self.xd, tol_exp)

    def tearDown(self):
        pass
