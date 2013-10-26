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

# Test function geo_mean
class TestFunctionGeMean(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_geo_mean_call(self):
        self.assertRaises(TypeError,geo_mean,[1])
        self.assertRaises(TypeError,geo_mean,[1,2,3])
        self.assertRaises(TypeError,geo_mean,np.matrix([[1,2,3],[4,5,6]]))
        self.assertRaises(TypeError,geo_mean,np.array([[1,2,3],[4,5,6]]))
        self.assertRaises(ValueError,geo_mean,variable(4,4))
        self.assertRaises(ValueError,geo_mean,parameter(3,2))
        self.assertRaises(ValueError,geo_mean,matrix([1,2,3]))
        self.assertTrue(np.allclose(geo_mean(2),2,self.rtol,self.atol))
        self.assertEqual(geo_mean(-2),-np.inf)
        x = variable()
        t = geo_mean(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertTrue(t.children[0],x)
        A = matrix([1,2,3,4,5,6]).T
        self.assertTrue(np.allclose(geo_mean(A),
                                    720. **(1./6),
                                    self.rtol,self.atol))
        self.assertEqual(geo_mean(-ones((100,1))),-np.inf)
        X = variable(3,1)
        f = geo_mean(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertTrue(f.children[i] is X[i,0])
        self.assertEqual(f.item.name,'geo_mean')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = parameter(3,1)
        f = geo_mean(A)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertTrue(f.children[i] is A[i,0])
        self.assertEqual(f.item.name,'geo_mean')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        f = geo_mean(A+X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            self.assertEqual(f.children[i].type,c.defs.TREE)
            self.assertTrue(f.children[i].children[0] is A[i,0])
            self.assertTrue(f.children[i].children[1] is X[i,0]) 
        self.assertEqual(f.item.name,'geo_mean')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = matrix([1,2,-3,5]).T
        self.assertEqual(geo_mean(A),-np.inf)

    def test_geo_mean_dcp(self):
        x = variable(3,1)
        self.assertFalse(geo_mean(x).is_convex())
        self.assertTrue(geo_mean(x).is_concave())
        self.assertTrue(geo_mean(x).is_dcp())
        self.assertFalse(geo_mean(x).is_affine())
        self.assertFalse(geo_mean(abs(x+1)).is_concave())
        self.assertFalse(geo_mean(abs(x+1)).is_convex())
        self.assertFalse(geo_mean(abs(2*x+100)).is_dcp())
        a = parameter(3,1)
        A = parameter(2,3)
        self.assertTrue(geo_mean(a).is_dcp())
        self.assertTrue(geo_mean(sqrt(A*x+1)).is_concave())
        self.assertFalse(geo_mean(sqrt(x+a)).is_convex())
        self.assertTrue(geo_mean(sqrt(2*x+a+100)).is_dcp())

    def test_geo_mean_in_prog(self):
        x = variable(5,1)
        p = program(maximize(geo_mean(x)),[less_equals(x,2)])
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,2*ones((5,1)),
                                    self.rtol,
                                    self.atol))
        p = program(minimize(sum(x)),[greater_equals(geo_mean(sqrt(x)),4)])
        self.assertTrue(np.allclose(p(),80,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,16*ones((5,1)),1e-3,1e-4))
        self.assertTrue(p.is_dcp())
        x = variable()
        p = program(minimize(x),[geq(geo_mean(x),2)])
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))        
        p = program(minimize(x),[geq(geo_mean(x),-2)])
        self.assertTrue(np.allclose(p(),0,self.rtol,self.atol))
