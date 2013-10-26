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

# Test function quad_over_lin
class TestFunctionQuadOverLin(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_quad_over_lin_call(self):
        y = variable()
        self.assertRaises(TypeError,quad_over_lin,[1,2],y)
        self.assertRaises(TypeError,quad_over_lin,np.matrix([1,2,3]).T,y)
        self.assertRaises(TypeError,quad_over_lin,np.array([1,2,3]).T,y)
        self.assertRaises(TypeError,quad_over_lin,variable(1,3),y)
        self.assertRaises(TypeError,quad_over_lin,parameter(3,3),y)
        self.assertRaises(TypeError,quad_over_lin,variable(),[1,2,3])
        self.assertRaises(TypeError,quad_over_lin,variable(),variable(3,1))
        self.assertRaises(TypeError,quad_over_lin,variable(),parameter(3,3))
        self.assertEqual(quad_over_lin(variable(),-1),np.inf)
        self.assertEqual(quad_over_lin(variable(3,1),0),np.inf)
        seed(1)
        x = rand(10,1)
        self.assertTrue(np.allclose(quad_over_lin(x,10),
                                    float(x.T*x)/10.,
                                    self.rtol,self.atol))

        self.assertTrue(np.allclose(quad_over_lin(5,10),
                                    25./10,self.rtol,self.atol))
        x = variable()
        y = variable()
        f = quad_over_lin(x,y)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertEqual(f.item.name,'quad_over_lin')
        self.assertEqual(len(f.children),2)
        a = parameter(3,1)
        b = parameter()
        f = quad_over_lin(a,b)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertEqual(f.item.name,'quad_over_lin')
        self.assertEqual(len(f.children),4)
        x = variable(3,1)
        f = quad_over_lin(x,10)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertEqual(f.item.name,'quad_over_lin')
        self.assertEqual(len(f.children),4)
        self.assertEqual(f.children[3].type,c.defs.CONSTANT)
        self.assertEqual(f.children[3].name,str(10))
        self.assertEqual(f.children[3].value,10)
        f = quad_over_lin(matrix([1,2,3]).T,y)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertEqual(f.item.name,'quad_over_lin')
        for i in range(0,3,1):
            self.assertEqual(f.children[i].type,c.defs.CONSTANT)
            self.assertEqual(f.children[i].name,str(i+1.))
            self.assertEqual(f.children[i].value,i+1.)
        self.assertTrue(f.children[3] is y)

    def test_quad_over_lin_dcp(self):
        x = variable()
        y = variable()
        self.assertTrue(quad_over_lin(x,y).is_dcp())
        self.assertTrue(quad_over_lin(x,y).is_convex())
        self.assertFalse(quad_over_lin(x,y).is_concave())
        self.assertFalse(quad_over_lin(x,y).is_affine())
        self.assertTrue(quad_over_lin(x,10).is_dcp())
        self.assertTrue(quad_over_lin(x,10).is_convex())
        self.assertFalse(quad_over_lin(x,10).is_concave())
        self.assertFalse(quad_over_lin(x,10).is_affine())
        self.assertTrue(quad_over_lin(x,log(y)).is_dcp())
        self.assertTrue(quad_over_lin(x,log(y)).is_convex())
        self.assertFalse(quad_over_lin(x,log(y)).is_concave())
        self.assertFalse(quad_over_lin(x,log(y)).is_affine())
        x = variable(4,1)
        A = ones((3,4))
        self.assertTrue(quad_over_lin(A*x+10,sqrt(y)).is_dcp())
        self.assertTrue(quad_over_lin(A*x+10,sqrt(y)).is_convex())
        self.assertFalse(quad_over_lin(A*x+10,sqrt(y)).is_concave())
        self.assertFalse(quad_over_lin(A*x+10,huber(y)).is_affine())
        self.assertFalse(quad_over_lin(A*x+10,huber(y)).is_dcp())
        self.assertFalse(quad_over_lin(A*x+10,huber(y)).is_convex())
        self.assertFalse(quad_over_lin(A*x+10,huber(y)).is_concave())
        self.assertFalse(quad_over_lin(A*x+10,huber(y)).is_affine())
        self.assertTrue(quad_over_lin(10,min(vstack([y,10]))).is_dcp())
        self.assertTrue(quad_over_lin(10,min(vstack([y,10]))).is_convex())
        self.assertFalse(quad_over_lin(10,min(vstack([y,10]))).is_concave())
        self.assertFalse(quad_over_lin(10,min(vstack([y,10]))).is_affine())
        y = variable(3,1)
        self.assertTrue(quad_over_lin(matrix([1,2,3]).T,
                                      geo_mean(y)).is_dcp())
        self.assertTrue(quad_over_lin(matrix([1,2,3]).T,
                                      geo_mean(y)).is_convex())
        self.assertFalse(quad_over_lin(matrix([1,2,3]).T,
                                       geo_mean(y)).is_concave())
        self.assertFalse(quad_over_lin(matrix([1,2,3]).T,
                                       geo_mean(y)).is_affine())
        
    def test_quad_over_lin_in_prog(self):
        x = variable(3,1)
        y = variable()
        p = program(minimize(quad_over_lin(x,y)),
                    [less_equals(square(y),9),
                     greater_equals(x,5)])
        self.assertTrue(np.allclose(p(),25,self.rtol,self.atol))
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(y.value,3,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,5*ones((3,1)),
                                    self.rtol,self.atol))
        p = program(minimize(y+10),
                    [less_equals(quad_over_lin(matrix([1,2,3]).T,y+5),7)])
        self.assertTrue(np.allclose(p(),7,self.rtol,self.atol))
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(y.value,-3,self.rtol,self.atol))
        p = program(maximize(sum(x)),
                    [less_equals(quad_over_lin(x,10),10)])
        self.assertTrue(np.allclose(p(),17.3205080,self.rtol,self.atol))
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(x.value,
                                    5.77350269*ones((3,1)),
                                    self.rtol,self.atol))
