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

# Test function abs
class TestFunctionAbs(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_abs_call(self):
        self.assertRaises(TypeError,abs,[1])
        self.assertRaises(TypeError,abs,np.matrix([1,2,3]))
        self.assertRaises(TypeError,abs,
                          c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5)))
        self.assertRaises(TypeError,abs,np.array([[1,2],[3,4]]))
        self.assertTrue(np.allclose(abs(-5),5,self.rtol,self.atol))
        self.assertTrue(np.allclose(abs(5),5,self.rtol,self.atol))
        A = matrix([[1,-2,3],[-3,-4,5]])
        f = abs(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        self.assertTrue(np.allclose(np.abs(A),f,self.rtol,self.atol))
        x = variable()
        t = abs(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'abs')
        self.assertEqual(t.children,[x])
        a = parameter()
        t = abs(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'abs')
        self.assertEqual(t.children,[a])
        t = abs(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'abs')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)
        X = variable(3,4)
        f = abs(X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.type,c.defs.FUNCTION)
                self.assertEqual(f[i,j].item.name,'abs')
                self.assertTrue(f[i,j].children[0] is X[i,j])
        A = parameter(3,4)
        f = abs(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.type,c.defs.FUNCTION)
                self.assertEqual(f[i,j].item.name,'abs')
                self.assertTrue(f[i,j].children[0] is A[i,j])
        f = abs(A+X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'abs')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertTrue(f[i,j].children[0].children[0] is A[i,j])
                self.assertTrue(f[i,j].children[0].children[1] is X[i,j])
    
    def test_abs_dcp(self):
        x = variable()
        self.assertTrue(abs(x).is_dcp())
        self.assertFalse(abs(x).is_affine())
        self.assertTrue(abs(x).is_convex())
        self.assertFalse(abs(x).is_concave())
        self.assertFalse(abs(square(x)).is_dcp())
        self.assertTrue(abs(x+4+2*(x+10)).is_convex())
        self.assertTrue(abs(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse(abs(sqrt(x)).is_dcp())
        a = parameter()
        self.assertTrue(abs(a).is_dcp())
        self.assertTrue(abs(x+a).is_dcp())
        self.assertTrue((abs(x)+abs(2*x)-3*(x+10)).is_convex())
        self.assertFalse((abs(x)+abs(2*x)-3*(x+10)).is_concave())
        self.assertFalse((abs(x)+abs(2*x)-3*(x+10)).is_affine())
        self.assertFalse((a*abs(x+1)).is_dcp())
        b = parameter(attribute='nonpositive')
        self.assertTrue((b*abs(x+1)).is_dcp())                     

    def test_abs_in_prog(self):
        x = variable()
        p = program(minimize(x),[less_equals(abs(x+10),4)])
        self.assertTrue(np.allclose(p(),-14,self.rtol,self.atol))
        p = program(maximize(x),[less_equals(abs(x+10),4)])
        self.assertTrue(np.allclose(p(),-6,self.rtol,self.atol))
