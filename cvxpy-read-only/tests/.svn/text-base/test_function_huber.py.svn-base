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

# Test function huber
class TestFunctionHuber(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7
    
    def h(self,x,M=1):
        if np.abs(x) <= M:
            return x*x
        else:
            return M*(2*np.abs(x)-M)

    def test_huber_call(self):
        self.assertRaises(TypeError,huber,[1])
        self.assertRaises(TypeError,huber,
                          c.scalars.cvxpy_obj(c.defs.CONSTANT,5,'5'))
        self.assertRaises(TypeError,huber,np.matrix([1,2,3]),1)
        self.assertRaises(TypeError,huber,variable(),parameter())
        self.assertRaises(ValueError,huber,variable(),-1)
        self.assertTrue(np.allclose(huber(-5,2),self.h(-5,2),
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(huber(5,3),self.h(5,3),
                                    self.rtol,self.atol))
        A = matrix([[1,-2,3],[-3,-4,5]])
        f = huber(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        for i in range(0,2,1):
            for j in range(0,3,1):
                self.assertTrue(np.allclose(self.h(A[i,j]),f[i,j],
                                            self.rtol,self.atol))
        x = variable()
        t = huber(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'huber')
        self.assertTrue(t.children[0] is x)
        self.assertEqual(len(t.children),1)
        a = parameter()
        t = huber(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'huber')
        self.assertTrue(t.children[0] is a)
        self.assertEqual(len(t.children),1)
        t = huber(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'huber')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)
        X = variable(3,4)
        f = huber(X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'huber')
                self.assertTrue(f[i,j].children[0] is X[i,j])
                self.assertEqual(len(f[i,j].children),1)
        A = parameter(3,4)
        f = huber(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'huber')
                self.assertTrue(f[i,j].children[0] is A[i,j])
                self.assertEqual(len(f[i,j].children),1)
        f = huber(A+X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'huber')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)
                self.assertTrue(f[i,j].children[0].children[0] is A[i,j])
                self.assertTrue(f[i,j].children[0].children[1] is X[i,j])

    def test_huber_dcp(self):
        x = variable()
        self.assertTrue(huber(x,2).is_dcp())
        self.assertFalse(huber(x,3).is_affine())
        self.assertTrue(huber(x,5).is_convex())
        self.assertFalse(huber(x).is_concave())
        self.assertFalse(huber(huber(x,2),3).is_dcp())
        self.assertTrue(huber(x+4+2*(x+10),2).is_convex())
        self.assertTrue(huber(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse(huber(sqrt(x)).is_dcp())
        a = parameter()
        self.assertTrue(huber(a).is_dcp())
        self.assertTrue(huber(x+a,2).is_dcp())
        self.assertTrue((huber(x,3)+huber(2*x,4)-3*(x+10)).is_convex())
        self.assertFalse((huber(x)+huber(2*x)-3*(x+10)).is_concave())
        self.assertFalse((huber(x,2)+huber(2*x)-3*(x+10)).is_affine())
        b = parameter(attribute='nonnegative')
        self.assertTrue((b*huber(2*x+10)).is_convex())
        
    def test_huber_in_prog(self):
        x = variable()
        p = program(minimize(x),[less_equals(huber(x+10,3),4)])
        self.assertTrue(np.allclose(p(),-12,self.rtol,self.atol))
        p = program(maximize(x),[less_equals(huber(x+10,2),30)])
        self.assertTrue(np.allclose(p(),-1.5,self.rtol,self.atol))
