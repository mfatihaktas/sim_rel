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

# Test function log
class TestFunctionLog(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_log_call(self):
        self.assertRaises(TypeError,log,[1])
        self.assertRaises(TypeError,log,np.matrix([1,2,3]))
        self.assertTrue(np.allclose(log(25),np.log(25),
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(log(100),np.log(100),
                                    self.rtol,self.atol))
        A = matrix([[1,4,9],[2,25,100]])
        f = log(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        self.assertTrue(np.allclose(np.log(A),f,self.rtol,self.atol))
        x = variable()
        t = log(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log')
        self.assertEqual(len(t.children),1)
        self.assertTrue(t.children[0] is x)
        a = parameter()
        t = log(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log')
        self.assertTrue(t.children[0] is a)
        t = log(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,
                         c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,
                         c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)        
        X = variable(3,4)
        f = log(X)
        self.assertTrue(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'log')
                self.assertTrue(f[i,j].children[0] is X[i,j])
        A = parameter(3,4)
        f = log(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'log')
                self.assertTrue(f[i,j].children[0] is A[i,j])
        f = log(A+X)
        self.assertEqual(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'log')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)

    def test_log_dcp(self):
        x = variable()
        self.assertTrue(log(x).is_dcp())
        self.assertFalse(log(x).is_affine())
        self.assertFalse(log(x).is_convex())
        self.assertTrue(log(x).is_concave())
        self.assertTrue(log(log(x)).is_dcp())
        self.assertTrue(log(x+4+2*(x+10)).is_concave())
        self.assertTrue(log(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse(log(-log(x)).is_dcp())
        self.assertTrue((-4*log(x)).is_convex())
        a = parameter()
        self.assertTrue(log(a).is_dcp())
        self.assertTrue(log(x+a).is_dcp())
        self.assertTrue((log(x)+ log(2*x) - 3*(x+10)).is_concave())
        self.assertFalse((log(x)+ log(2*x) - 3*(x+10)).is_convex())
        self.assertFalse((log(x)+ log(2*x) - 3*(x+10)).is_affine())

    def test_log_in_prog(self):
        x = variable()
        p = program(minimize(x),[greater_equals(log(x+10),4)])
        self.assertTrue(np.allclose(p(),np.exp(4)-10,self.rtol,self.atol))
        p = program(maximize(x),[greater_equals(log(10-x),4)])
        self.assertTrue(np.allclose(p(),10-np.exp(4),self.rtol,self.atol))
