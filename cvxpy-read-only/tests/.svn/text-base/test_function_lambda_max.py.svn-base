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
import cvxpy as c

# Test function lambda_max
class TestFunctionLambdaMax(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_lambda_max_call(self):
        self.assertRaises(TypeError,lambda_max,[variable(),2])
        self.assertRaises(TypeError,lambda_max,np.matrix([[1,2],[3,4]]))
        self.assertRaises(TypeError,lambda_max,np.array([[1,2],[3,4]]))
        self.assertRaises(ValueError,lambda_max,matrix([[1,2,3],[4,5,6]]))
        self.assertRaises(ValueError,lambda_max,variable(4,3))
        self.assertRaises(ValueError,lambda_max,
                          parameter(2,4)+variable(2,4))
        self.assertRaises(ValueError,lambda_max,parameter(5,2))
        self.assertEqual(lambda_max(1),1)
        x = variable()
        self.assertTrue(lambda_max(x) is x)
        t = x + parameter()
        self.assertTrue(lambda_max(t) is t)
        self.assertEqual(lambda_max(matrix([[1,2],[3,4]])),np.inf)
        A = matrix([[1,2,3],[2,5,6],[3,6,9]])
        self.assertTrue(np.allclose(lambda_max(A),
                                    np.max(np.linalg.eig(A)[0]),
                                    self.rtol,self.atol))
        B = diag(vstack([1,2,3,4,5,6,7,8]))
        self.assertTrue(np.allclose(lambda_max(B),8,
                                    self.rtol,self.atol))
        X = variable(3,3)
        f = lambda_max(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertTrue(f.children[i*3+j] is X[i,j])
        self.assertEqual(f.item.name,'lambda_max')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = parameter(3,3)
        f = lambda_max(A)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertTrue(f.children[i*3+j] is A[i,j])
        self.assertEqual(f.item.name,'lambda_max')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        f = lambda_max(A+X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertEqual(f.children[i*3+j].type,c.defs.TREE)
                self.assertTrue(f.children[i*3+j].children[0] is A[i,j])
                self.assertTrue(f.children[i*3+j].children[1] is X[i,j])
        self.assertEqual(f.item.name,'lambda_max')
        self.assertEqual(f.item.type,c.defs.FUNCTION)

    def test_lambda_max_dcp(self):
        x = variable(5,5)
        f = lambda_max(x+1)
        self.assertTrue(f.is_convex())
        self.assertFalse(f.is_concave())
        self.assertTrue(f.is_dcp())
        self.assertFalse(f.is_affine())
        f = -9*lambda_max(2*x+10)
        self.assertFalse(f.is_convex())
        self.assertTrue(f.is_concave())
        self.assertTrue(f.is_dcp())
        self.assertFalse(f.is_affine())
        f = lambda_max(square(x+1))
        self.assertFalse(f.is_convex())
        self.assertFalse(f.is_concave())
        self.assertFalse(f.is_dcp())
        self.assertFalse(f.is_affine())
        f = lambda_max(log(x+1))
        self.assertFalse(f.is_convex())
        self.assertFalse(f.is_concave())
        self.assertFalse(f.is_dcp())
        self.assertFalse(f.is_affine())

    def test_lambda_max_in_prog(self):
        x = variable(4,4)
        p = program(maximize(sum(x)),[less_equals(lambda_max(x),10)])
        self.assertTrue(np.allclose(p(),40,self.rtol,self.atol))
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(x.value,x.value.T,
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(np.max(np.linalg.eig(x.value)[0]),
                                    10,self.rtol,self.atol))
