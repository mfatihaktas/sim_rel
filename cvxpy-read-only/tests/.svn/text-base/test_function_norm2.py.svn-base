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

# Test function norm2
class TestFunctionNorm2(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_norm2_call(self):
        self.assertRaises(TypeError,norm2,[1,2,3])
        self.assertRaises(TypeError,norm2,np.matrix([[1,2,3],[4,5,6]]))
        self.assertRaises(TypeError,norm2,np.array([[1,2,3],[4,5,6]]))
        self.assertTrue(np.allclose(norm2(10),10,self.rtol,self.atol))
        self.assertTrue(np.allclose(norm2(-10),10,self.rtol,self.atol))
        x = variable()
        t = norm2(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertTrue(t.children[0] is x)
        t = norm2(x+10)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        A = matrix([1,2,3,4,5,6]).T
        self.assertTrue(np.allclose(norm2(A),
                                    np.linalg.norm(A),
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(norm2(-ones((100,1))),10,
                                    self.rtol,self.atol))
        X = variable(3,1)
        f = norm2(X)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertTrue(f.children[i] is X[i,0])
        self.assertEqual(f.item.name,'norm2')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = parameter(3,1)
        f = norm2(A)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertTrue(f.children[i] is A[i,0])
        self.assertEqual(f.item.name,'norm2')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        f = norm2(A+X)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertEqual(f.children[i].type,c.defs.TREE)
            self.assertEqual(len(f.children[i].children),2)
        self.assertEqual(f.item.name,'norm2')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        X = variable(4,4)
        f = norm2(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(len(f.children),16)
        self.assertTrue(f.children[0] is X[0,0])
        X = parameter(3,2)
        f = norm2(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(len(f.children),6)
        self.assertTrue(f.children[0] is X[0,0])
        X = parameter(2,5) + 4*variable(2,5)
        f = norm2(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(len(f.children),10)
        A = matrix([[1,2,3,4],[5,6,7,8]])
        self.assertTrue(np.allclose(norm2(A),
                                    np.max(np.linalg.svd(A)[1]),
                                    self.rtol,self.atol))
        seed(1)
        A = randn(5,7)
        self.assertTrue(np.allclose(norm2(A),
                                    np.max(np.linalg.svd(A)[1]),
                                    self.rtol,self.atol))
        A = matrix([1,2,3,4,5])
        self.assertTrue(np.allclose(norm2(A),
                                    np.sqrt(np.sum(np.square(A))),
                                    self.rtol,
                                    self.atol))

    def test_norm2_dcp(self):
        x = variable(5,1)
        self.assertTrue(norm2(x).is_convex())
        self.assertFalse(norm2(x).is_concave())
        self.assertTrue(norm2(x).is_dcp())
        self.assertFalse(norm2(x).is_affine())
        self.assertFalse(norm2(huber(x+1)).is_concave())
        self.assertFalse(norm2(huber(x+1)).is_convex())
        self.assertFalse(norm2(huber(2*x+100)).is_dcp())
        self.assertTrue(norm2(parameter(3,1)).is_dcp())
        self.assertFalse(norm2(log(x+1)).is_concave())
        self.assertFalse(norm2(log(x+1)).is_convex())
        self.assertFalse(norm2(log(2*x+100)).is_dcp())
        X = variable(4,6)
        self.assertTrue(norm2(X).is_dcp())
        self.assertTrue(norm2(X).is_convex())
        self.assertFalse(norm2(X).is_concave())
        seed(1)
        A = randn(5,4)
        self.assertTrue(norm2(A*X+1).is_dcp())
        self.assertTrue(norm2(A*X+1).is_convex())
        self.assertFalse(norm2(A*X+1).is_concave())
        self.assertFalse(norm2(abs(X)+1).is_dcp())
        self.assertFalse(norm2(sqrt(X)).is_convex())
        self.assertFalse(norm2(sqrt(X)).is_concave())
        a = parameter(1,4)
        x = parameter(1,4)
        self.assertTrue(norm2(2*x+a).is_convex())
        self.assertTrue(norm2(2*x+1).is_dcp())
        self.assertFalse(norm2(2*x+1).is_concave())

    def test_norm2_in_prog(self):
        x = variable(5,1)
        p = program(minimize(sum(x)),[less_equals(norm2(x+1),5)])
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(p(),-16.1803398,
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,
                                    -3.236067*ones((5,1)),
                                    self.rtol,
                                    self.atol))
        p = program(minimize(norm2(2*x)),[equals(sum(x),1)])
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(p(),0.89442719,
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,
                                    0.2*ones((5,1)),
                                    self.rtol,
                                    self.atol))
        x = variable()
        p = program(minimize(x),[leq(norm2(x),1)])
        self.assertTrue(np.allclose(p(),-1,self.rtol,self.atol))
        X = variable(4,5)
        p = program(minimize(norm2(X)),[geq(X,1)])
        self.assertTrue(np.allclose(p(),4.472136,self.rtol,self.atol))
        x = variable()
        A = diag(vstack([1,2,3]))
        p = program(maximize(x),[leq(norm2(x*A),10)])
        self.assertTrue(np.allclose(p(),3.333333,self.rtol,self.atol))
