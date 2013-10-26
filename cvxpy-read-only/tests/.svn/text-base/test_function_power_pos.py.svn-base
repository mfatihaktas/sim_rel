#***********************************************************************#
# Copyright (C) 2010-2013 Tomas Tinoco De Rubira                        #
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
from scipy.stats import norm

# Test function power_pos
class TestFunctionPowerPos(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_power_pos_call(self):
        self.assertRaises(TypeError,power_pos,[1],2.)
        self.assertRaises(TypeError,power_pos,np.matrix([1,2,3]),3.)
        self.assertRaises(TypeError,power_pos,variable(),[1.])
        self.assertRaises(TypeError,power_pos,variable(),variable())
        self.assertRaises(ValueError,power_pos,variable(),0.9999)
        self.assertRaises(ValueError,power_pos,variable(),0.5)
        self.assertTrue(np.allclose(power_pos(6.,4.521),6.**4.521,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_pos(3.,1.),3.,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_pos(-3.,1.),0.,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_pos(-3.,4.5),0.,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_pos(3.,2.),3.**2.,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_pos(10.,7.8829),10.**7.8829,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_pos(1000.,2.32),1000.**2.32,self.rtol,self.atol))
        self.assertRaises(ValueError,power_pos,10,9.)
        A = matrix([[1,4,-9],[2,-5,10]])
        f = power_pos(A,5.68912)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        b = 5.68912
        B = matrix([[1.,4.**b,0.],[2.**b,0.,10.**b]])
        self.assertTrue(np.allclose(B,f,self.rtol,self.atol))
        x = variable()
        t = power_pos(x,1.688)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'power_pos')
        self.assertEqual(len(t.children),1)
        self.assertTrue(t.children[0] is x)
        a = parameter()
        t = power_pos(a,3.333)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'power_pos')
        self.assertTrue(t.children[0] is a)
        t = power_pos(x+a,4.3)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'power_pos')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,
                         c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,
                         c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)        
        X = variable(3,4)
        f = power_pos(X,7.2)
        self.assertTrue(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'power_pos')
                self.assertTrue(f[i,j].children[0] is X[i,j])
        A = parameter(3,4)
        f = power_pos(A,4.5332)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'power_pos')
                self.assertTrue(f[i,j].children[0] is A[i,j])
        f = power_pos(A+X,1.688)
        self.assertEqual(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'power_pos')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)
  
    def test_power_pos_dcp(self):
        x = variable()
        b = 1.688
        self.assertTrue(power_pos(x,b).is_dcp())
        self.assertFalse(power_pos(x,b).is_affine())
        self.assertFalse(power_pos(x,b).is_concave())
        self.assertTrue(power_pos(x,b).is_convex())
        self.assertFalse(power_pos(log(x),b).is_dcp())
        self.assertTrue(power_pos(x+4+2*(x+10),b).is_convex())
        self.assertFalse(power_pos(x+4+2*(x+10),b).is_concave())
        self.assertTrue(power_pos(x+5*x-3*(x-10),b).is_dcp())
        self.assertTrue(power_pos(-log(x),b).is_dcp())
        self.assertTrue(power_pos(abs(x),b).is_convex())
        self.assertFalse(power_pos(sqrt(x),b).is_dcp())
        self.assertFalse(power_pos(sqrt(x),b).is_concave())
        self.assertTrue(power_pos(exp(x),b).is_dcp())
        self.assertTrue((-4*power_pos(square(x),b)).is_concave())
        a = parameter()                  
        self.assertTrue(power_pos(a,b).is_dcp())
        self.assertTrue(power_pos(x+a,b).is_dcp())
        self.assertTrue((power_pos(x,b)+power_pos(2*x,b)).is_convex())
        self.assertFalse((power_pos(x,b)+power_pos(2*x,b)).is_concave())
        self.assertTrue(power_pos(square(a*x+1),b).is_convex())

    def test_power_pos_in_prog(self):
        x = variable()
        p = program(minimize(x),[geq(x,-10.),leq(power_pos(x,4.55),10.)])
        self.assertTrue(np.allclose(p(),
                                    -10.,
                                    self.rtol,self.atol))
        p = program(minimize(power_pos(square(x),3.3)),[geq(x,2.)])
        self.assertTrue(np.allclose(p(),
                                    2.**(3.3*2.),
                                    self.rtol,self.atol))
