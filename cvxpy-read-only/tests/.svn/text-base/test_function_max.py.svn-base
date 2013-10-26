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

# Test function max
class TestFunctionMax(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_max_call(self):
        self.assertRaises(TypeError,max,np.matrix([1,2,3]))
        self.assertRaises(TypeError,max,[1,2,3,variable()])
        self.assertRaises(TypeError,max,(1,2,3,4,parameter()))
        self.assertTrue(np.allclose(max(hstack([-5])),-5,self.rtol,self.atol))
        self.assertTrue(np.allclose(max(hstack((5,2))),5,self.rtol,self.atol))
        self.assertEqual(max(1),1)
        x = variable()
        self.assertTrue(max(x) is x)
        t = x+1
        self.assertTrue(max(t) is t)
        a = parameter()
        self.assertTrue(type(max(hstack([x,2,1,a]))) is c.scalars.cvxpy_tree)
        self.assertTrue(np.allclose(max(vstack((1,2,3,4))),
                                    4,self.rtol,self.atol))
        t = max(vstack((1,2,3,x,a)))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),5)
        A = matrix([[1,-2,3],[-20,40,3.3]])
        f = max(A)
        self.assertTrue(np.allclose(np.max(A),f,self.rtol,self.atol))
        self.assertTrue(max(a) is a)
        t = max(hstack([a,x]))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'max')
        self.assertEqual(len(t.children),2)
        self.assertTrue(t.children[0] is a)
        self.assertTrue(t.children[1] is x)
        t = max(vstack([x,a]))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'max')
        self.assertEqual(len(t.children),2)
        self.assertTrue(t.children[0] is x)
        self.assertTrue(t.children[1] is a)
        X = variable(3,5)
        f = max(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'max')
        self.assertEqual(len(f.children),15)
        for i in range(0,3,1):
            for j in range(0,5,1):
                self.assertTrue(f.children[i*5+j] is X[i,j])
        A = parameter(2,3)
        f = max(A)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'max')
        self.assertEqual(len(f.children),6)
        for i in range(0,2,1):
            for j in range(0,3,1):
                self.assertTrue(f.children[i*3+j] is A[i,j])
        f = max(vstack((X.T,A)))
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'max')
        self.assertEqual(len(f.children),21)
    
    def test_max_dcp(self):
        x = variable()
        self.assertTrue(max(x).is_dcp())
        self.assertFalse(max(vstack([x,1])).is_affine())
        self.assertTrue(max(variable(4,2)).is_convex())
        self.assertFalse(max(variable(3,3)).is_concave())
        self.assertTrue(max(vstack((square(x),10,-sqrt(x+1)))).is_dcp())
        self.assertFalse(max(hstack((square(x),10,sqrt(x+1)))).is_dcp())
        self.assertTrue(max(hstack([x,x+10,abs(x+10)])).is_dcp())
        self.assertFalse(max(vstack([sqrt(x),x])).is_dcp())
        a = parameter()
        self.assertTrue(max(vstack([a,2])).is_dcp())
        self.assertTrue(max(vstack((x,a))).is_dcp())
        self.assertTrue((max(hstack([x,square(x)]))+
                         max(vstack((x,x+1)))).is_convex())
        self.assertFalse((max(hstack([x,square(x)]))+
                          max(vstack((x,x+1)))).is_affine())
        self.assertFalse((max(hstack([x,abs(x)]))+
                          max(vstack((x,x+1)))).is_concave())

    def test_max_in_prog(self):
        x = variable()
        y = variable()
        p = program(maximize(x+y),[less_equals(max(vstack([x,y])),10)])
        self.assertTrue(np.allclose(p(),20,self.rtol,self.atol))
        p = program(maximize(x+y),[less_equals(max(vstack((square(x),y,5))),
                                               9)])
        self.assertTrue(np.allclose(p(),12,self.rtol,self.atol))
