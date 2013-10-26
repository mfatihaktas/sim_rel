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

# Test function norm1
class TestFunctionNorm1(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_norm1_call(self):
        self.assertRaises(TypeError,norm1,[1,2,3])
        self.assertRaises(TypeError,norm1,np.matrix([[1,2,3],[4,5,6]]))
        self.assertRaises(TypeError,norm1,np.array([[1,2,3],[4,5,6]]))
        self.assertTrue(np.allclose(norm1(1),1,self.rtol,self.atol))
        self.assertTrue(np.allclose(norm1(-10),10,self.rtol,self.atol))
        x = variable()
        t = norm1(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),1)
        t = norm1(x+10+parameter())
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(len(t.children[0].children),3)
        A = matrix([1,2,3,4,5,6]).T
        self.assertTrue(np.allclose(norm1(A),21,self.rtol,self.atol))
        self.assertTrue(np.allclose(norm1(-ones((100,1))),100,
                                    self.rtol,self.atol))
        X = variable(3,1)
        f = norm1(X)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertTrue(f.children[i] is X[i,0])
        self.assertEqual(f.item.name,'norm1')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = parameter(3,1)
        f = norm1(A)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertTrue(f.children[i] is A[i,0])
        self.assertEqual(f.item.name,'norm1')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        f = norm1(A+X)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertEqual(f.children[i].type,c.defs.TREE)
            self.assertEqual(len(f.children[i].children),2)
        self.assertEqual(f.item.name,'norm1')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = matrix([[1,-2,3],[4,5,-6]])
        self.assertTrue(np.allclose(norm1(A),9,self.rtol,self.atol))
        seed(1)
        A = randn(1,10)
        self.assertTrue(np.allclose(norm1(A),np.max(np.abs(A)),
                                    self.rtol,self.atol))
        X = variable(5,2)
        f = norm1(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(len(f.children),10)
        x = variable()
        x.value = -10
        t = norm1(x)
        self.assertTrue(np.allclose(t.value,10,self.rtol,self.atol))
        self.assertTrue(np.allclose(norm1(-5),5,self.rtol,self.atol))
        A = randn(5,3)
        self.assertTrue(np.allclose(norm1(A),np.linalg.norm(A,1),
                                    self.rtol,self.atol))
        A = randn(3,5)
        self.assertTrue(np.allclose(norm1(A),np.linalg.norm(A,1),
                                    self.rtol,self.atol))

    def test_norm1_dcp(self):
        x = variable(5,1)
        self.assertTrue(norm1(x).is_convex())
        self.assertFalse(norm1(x).is_concave())
        self.assertTrue(norm1(x).is_dcp())
        self.assertFalse(norm1(x).is_affine())
        self.assertFalse(norm1(abs(x+1)).is_concave())
        self.assertFalse(norm1(abs(x+1)).is_convex())
        self.assertFalse(norm1(abs(2*x+100)).is_dcp())
        self.assertTrue(norm1(parameter(3,1)).is_dcp())
        self.assertFalse(norm1(sqrt(x+1)).is_concave())
        self.assertFalse(norm1(sqrt(x+1)).is_convex())
        self.assertFalse(norm1(sqrt(2*x+100)).is_dcp())
        y = variable(3,4)
        self.assertTrue(norm1(y).is_convex())
        self.assertFalse(norm1(y).is_concave())
        self.assertTrue(norm1(y+1).is_dcp())
        A = randn(2,3)
        self.assertTrue(norm1(A*y+10).is_dcp())

    def test_norm1_in_prog(self):
        x = variable(5,1)
        p = program(minimize(sum(x)),[less_equals(norm1(x+1),5)])
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(p(),-10,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,-2*ones((5,1)),
                                    self.rtol,
                                    self.atol))
        p = program(minimize(norm1(2*x)),[equals(sum(x),1)])
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,0.2*ones((5,1)),
                                    self.rtol,
                                    self.atol))
        x = variable()
        p = program(minimize(x),[leq(norm1(x),1)])
        self.assertTrue(np.allclose(p(),-1,self.rtol,self.atol))
        y = variable(2,5)
        p = program(minimize(sum(y)),[leq(norm1(y),5)])
        self.assertTrue(np.allclose(p(),-25,self.rtol,self.atol))
        self.assertTrue(np.allclose(y.value,-2.5*ones((2,5)),
                                    self.rtol,self.atol))
