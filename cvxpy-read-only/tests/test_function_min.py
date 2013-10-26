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

# Test function min
class TestFunctionMin(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_min_call(self):
        self.assertRaises(TypeError,min,np.matrix([1,2,3]))
        self.assertRaises(TypeError,min,[1,2,3,variable(),parameter()])
        self.assertRaises(TypeError,min,(1,2,variable()))        
        self.assertTrue(np.allclose(min(vstack([-5])),-5,self.rtol,self.atol))
        self.assertTrue(np.allclose(min(hstack((5,2))),2,self.rtol,self.atol))
        self.assertEqual(min(10),10)
        x = variable()
        self.assertTrue(min(x) is x)
        t = x+1
        self.assertTrue(min(t) is t)
        a = parameter()
        self.assertTrue(type(min(hstack([x,2,1,a]))) is c.scalars.cvxpy_tree)
        self.assertRaises(TypeError,min,(variable(2,2),parameter(2,3)))
        self.assertTrue(np.allclose(min(vstack((1,2,3,4))),
                                    1,self.rtol,self.atol))
        t = min(vstack((1,2,3,x,a)))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),5)       
        A = matrix([[1,-2,3],[-20,40,3.3]])
        f = min(A)
        self.assertTrue(np.allclose(np.min(A),f,self.rtol,self.atol))
        self.assertTrue(min(a) is a)
        t = min(vstack([x,a]))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'min')
        self.assertEqual(len(t.children),2)
        self.assertTrue(t.children[0] is x)
        self.assertTrue(t.children[1] is a)
        X = variable(3,5)
        f = min(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'min')
        self.assertEqual(len(f.children),15)
        for i in range(0,3,1):
            for j in range(0,5,1):
                self.assertTrue(f.children[i*5+j] is X[i,j])
        A = parameter(2,3)
        f = min(A)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'min')
        self.assertEqual(len(f.children),6)
        for i in range(0,2,1):
            for j in range(0,3,1):
                self.assertTrue(f.children[i*3+j] is A[i,j])
        f = min(vstack((X.T,A)))
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'min')
        self.assertEqual(len(f.children),21)

    def test_min_dcp(self):
        x = variable()
        self.assertTrue(min(x).is_dcp())
        self.assertTrue(min(vstack([x,2*x+1])).is_dcp())
        self.assertFalse(min(vstack([x,2])).is_affine())
        self.assertFalse(min(variable(4,5)).is_convex())
        self.assertTrue(min(variable(2,3)).is_concave())
        self.assertFalse(min(vstack((square(x),10,-sqrt(x+1)))).is_dcp())
        self.assertTrue(min(hstack((-square(x),10,sqrt(x+1)))).is_dcp())
        self.assertFalse(min(hstack([x,x+10,abs(x+10)])).is_dcp())
        self.assertTrue(min(vstack([sqrt(x),x])).is_dcp())
        a = parameter()
        self.assertTrue(min(vstack([a,4])).is_dcp())
        self.assertTrue(min(vstack((x,a))).is_dcp())
        self.assertTrue((min(vstack([x,-square(x)]))+
                         min(vstack((x,1)))).is_concave())
        self.assertFalse((min(hstack([x,square(x)]))+
                          min(vstack((x,x+1)))).is_affine())
        self.assertFalse((min(hstack([x,abs(x)]))+
                          min(vstack((x,x+1)))).is_concave())

    def test_min_in_prog(self):
        x = variable()
        y = variable()
        p = program(minimize(x+y),[greater_equals(min(vstack([x,y])),10)])
        self.assertTrue(np.allclose(p(),20,self.rtol,self.atol))
        p = program(minimize(x+y),[greater_equals(min(vstack((sqrt(x),y,5))),
                                                  3)])
        self.assertTrue(np.allclose(p(),12,self.rtol,self.atol))
