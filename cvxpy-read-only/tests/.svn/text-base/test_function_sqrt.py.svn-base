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

# Test function sqrt
class TestFunctionSqrt(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_sqrt_call(self):
        self.assertRaises(TypeError,sqrt,[1])
        self.assertRaises(TypeError,sqrt,np.matrix([1,2,3]))
        self.assertRaises(TypeError,sqrt,
                          c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5)))
        self.assertTrue(np.allclose(sqrt(25),5,self.rtol,self.atol))
        self.assertTrue(np.equal(sqrt(-5),-np.inf))
        A = matrix([[1,4,9],[2,25,100]])
        f = sqrt(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        self.assertTrue(np.allclose(np.sqrt(A),f,self.rtol,self.atol))
        x = variable()
        t = sqrt(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'sqrt')
        self.assertEqual(len(t.children),1)
        a = parameter()
        t = sqrt(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'sqrt')
        self.assertEqual(len(t.children),1)
        t = sqrt(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'sqrt')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,
                         c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,
                         c.defs.SUMMATION)
        self.assertEqual(len(t.children[0].children),2)
        X = variable(3,4)
        f = sqrt(X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'sqrt')
                self.assertEqual(len(f[i,j].children),1)
        A = parameter(3,4)
        f = sqrt(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'sqrt')
                self.assertEqual(len(f[i,j].children),1)
        f = sqrt(A+X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'sqrt')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)
     
    def test_sqrt_dcp(self):
        x = variable()
        self.assertTrue(sqrt(x).is_dcp())
        self.assertFalse(sqrt(x).is_affine())
        self.assertFalse(sqrt(x).is_convex())
        self.assertTrue(sqrt(x).is_concave())
        self.assertTrue(sqrt(sqrt(x)).is_dcp())
        self.assertTrue(sqrt(x+4+2*(x+10)).is_concave())
        self.assertTrue(sqrt(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse(sqrt(-sqrt(x)).is_dcp())
        self.assertTrue((-4*sqrt(x)).is_convex())
        a = parameter()
        self.assertTrue(sqrt(a).is_dcp())
        self.assertTrue(sqrt(x+a).is_dcp())
        self.assertTrue((sqrt(x)+ sqrt(2*x)-3*(x+10)).is_concave())
        self.assertFalse((sqrt(x)+ sqrt(2*x)-3*(x+10)).is_convex())
        self.assertFalse((sqrt(x)+ sqrt(2*x)-3*(x+10)).is_affine())

    def test_sqrt_in_prog(self):
        x = variable()
        p = program(minimize(x),[greater_equals(sqrt(x+10),4)])
        self.assertTrue(np.allclose(p(),6,self.rtol,self.atol))
        p = program(maximize(x),[greater_equals(sqrt(10-x),4)])
        self.assertTrue(np.allclose(p(),-6,self.rtol,self.atol))
