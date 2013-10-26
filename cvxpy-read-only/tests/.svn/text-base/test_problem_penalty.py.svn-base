#***********************************************************************#
# Copyright (C) 2010-2012 Tomas Tinoco De Rubira                        #
# Contributing author: Eugene Brevdo                                    #
#                                                                       #
# Most of this code is based extensively on the cvxopt example:         #
#  http://abel.ee.ucla.edu/cvxopt/examples/book/penalties.html          #
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

class TestProblemPenalty(unittest.TestCase):

    m = None
    n = None
    A = None
    b = None
    x1 = None
    x2 = None
    xdz = None
    cxlb = None

    def setUp(self):
        """
        Use cvxopt to get ground truth values
        """

        from cvxopt import lapack,solvers,matrix,spdiag,log,div,normal,setseed
        from cvxopt.modeling import variable,op,max,sum
        solvers.options['show_progress'] = 0

        setseed()
        m,n = 100,30
        A = normal(m,n)
        b = normal(m,1)
        b /= (1.1*max(abs(b)))
        self.m,self.n,self.A,self.b = m,n,A,b

        # l1 approximation
        # minimize || A*x + b ||_1
        x = variable(n)
        op(sum(abs(A*x+b))).solve()
        self.x1 = x.value

        # l2 approximation
        # minimize || A*x + b ||_2
        bprime = -matrix(b)
        Aprime = matrix(A)
        lapack.gels(Aprime,bprime)
        self.x2 = bprime[:n]

        # Deadzone approximation
        # minimize sum(max(abs(A*x+b)-0.5, 0.0))
        x = variable(n)
        dzop = op(sum(max(abs(A*x+b)-0.5, 0.0)))
        dzop.solve()
        self.obj_dz = sum(np.max([np.abs(A*x.value+b)-0.5,np.zeros((m,1))],axis=0))

        # Log barrier
        # minimize -sum (log ( 1.0 - (A*x+b)**2))
        def F(x=None, z=None):
            if x is None: return 0, matrix(0.0,(n,1))
            y = A*x+b
            if max(abs(y)) >= 1.0: return None
            f = -sum(log(1.0 - y**2))
            gradf = 2.0 * A.T * div(y, 1-y**2)
            if z is None: return f, gradf.T
            H = A.T * spdiag(2.0*z[0]*div(1.0+y**2,(1.0-y**2)**2))*A
            return f,gradf.T,H
        self.cxlb = solvers.cp(F)['x']

    def test_problem_penalty(self):
        """
        Compare cvxpy solutions to cvxopt ground truth
        """

        from cvxpy import (matrix,variable,program,minimize,
                           sum,abs,norm2,log,square,zeros,max,
                           hstack,vstack)

        m, n = self.m, self.n
        A = matrix(self.A)
        b = matrix(self.b)

        # set tolerance to 5 significant digits
        tol_exp = 5

        # l1 approximation
        x = variable(n)
        p = program(minimize(sum(abs(A*x + b))))
        p.solve(True)
        np.testing.assert_array_almost_equal(x.value,self.x1,tol_exp)

        # l2 approximation
        x = variable(n)
        p = program(minimize(norm2(A*x + b)))
        p.solve(True)
        np.testing.assert_array_almost_equal(x.value,self.x2,tol_exp)

        # Deadzone approximation - implementation is currently ugly (need max along axis)
        x = variable(n)
        Axbm = abs(A*x+b)-0.5
        Axbm_deadzone = vstack([max(hstack((Axbm[i,0],0.0))) for i in range(m)])
        p = program(minimize(sum(Axbm_deadzone)))
        p.solve(True)
        obj_dz_cvxpy = np.sum(np.max([np.abs(A*x.value+b)-0.5,np.zeros((m,1))],axis=0))
        np.testing.assert_array_almost_equal(obj_dz_cvxpy,self.obj_dz,tol_exp)

        # Log barrier
        x = variable(n)
        p = program(minimize(-sum(log(1.0-square(A*x + b)))))
        p.solve(True)
        np.testing.assert_array_almost_equal(x.value,self.cxlb,tol_exp)

    def tearDown(self):
        pass
