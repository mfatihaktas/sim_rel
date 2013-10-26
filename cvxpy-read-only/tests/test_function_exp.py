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

# Test function exp
class TestFunctionExp(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_exp_call(self):
        self.assertRaises(TypeError,exp,[1])
        self.assertRaises(TypeError,exp,np.matrix([1,2,3]))
        self.assertRaises(TypeError,exp,np.ones((3,2)))
        self.assertRaises(TypeError,exp,
                          c.scalars.cvxpy_obj(c.defs.CONSTANT,4,'4'))
        self.assertTrue(np.allclose(exp(-5),np.exp(-5),self.rtol,self.atol))
        self.assertTrue(np.allclose(exp(5),np.exp(5),self.rtol,self.atol))
        A = matrix([[1,-2,3],[-3,-4,5]])
        f = exp(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        self.assertTrue(np.allclose(np.exp(A),f,self.rtol,self.atol))
        x = variable()
        t = exp(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'exp')
        self.assertTrue(t.children[0] is x)
        self.assertEqual(len(t.children),1)
        a = parameter()
        t = exp(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'exp')
        self.assertEqual(len(t.children),1)
        self.assertTrue(t.children[0] is a)
        t = exp(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'exp')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)
        X = variable(3,4)
        f = exp(X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'exp')
                self.assertTrue(f[i,j].children[0] is X[i,j])
        A = parameter(3,4)
        f = exp(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'exp')
                self.assertTrue(f[i,j].children[0] is A[i,j])
        f = exp(A+X)
        self.assertTrue(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'exp')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertTrue(f[i,j].children[0].children[0] is A[i,j])
                self.assertTrue(f[i,j].children[0].children[1] is X[i,j])
    
    def test_exp_dcp(self):
        x = variable()
        self.assertTrue(exp(x).is_dcp())
        self.assertFalse(exp(x).is_affine())
        self.assertTrue(exp(x).is_convex())
        self.assertFalse(exp(x).is_concave())
        self.assertTrue(exp(exp(x)).is_dcp())
        self.assertTrue((exp(square(x+1)) + 10).is_dcp())
        self.assertFalse((exp(sqrt(x))).is_dcp())
        self.assertTrue(exp(x+4+2*(x+10)).is_convex())
        self.assertTrue(exp(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse((exp(square(x)+abs(x)+sqrt(x))).is_dcp())
        a = parameter()
        self.assertTrue(exp(a).is_dcp())
        self.assertTrue(exp(x+a).is_convex())
        self.assertTrue((exp(x)+exp(2*x)-3*(x+10)).is_convex())
        self.assertFalse((exp(x)+exp(2*x)-3*(x+10)).is_concave())
        self.assertFalse((exp(x)+exp(2*x)-3*(x+10)).is_affine())
        self.assertFalse((a*exp(2*x+10)).is_convex())
        b = parameter(attribute='nonpositive')
        self.assertTrue((-b*exp(2*x+10)).is_convex())

    def test_exp_in_prog(self):
        x = variable()
        p = program(maximize(x),[less_equals(exp(x+2),4)])
        self.assertTrue(np.allclose(p(),np.log(4)-2,self.rtol,self.atol))
        p = program(minimize(exp(x+2)),[greater_equals(x,4)])
        self.assertTrue(np.allclose(p(),np.exp(6),self.rtol,self.atol))
