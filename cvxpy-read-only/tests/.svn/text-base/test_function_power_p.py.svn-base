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

# Test function power_p
class TestFunctionPowerP(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_power_p_call(self):
        self.assertRaises(TypeError,power_p,[1],2.)
        self.assertRaises(TypeError,power_p,np.matrix([1,2,3]),3.)
        self.assertRaises(TypeError,power_p,variable(),[1.])
        self.assertRaises(TypeError,power_p,variable(),variable())
        self.assertRaises(ValueError,power_p,variable(),0.9999)
        self.assertRaises(ValueError,power_p,variable(),0.5)
        self.assertTrue(np.allclose(power_p(3.,5.55),3.**5.55,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_p(3.,1.),3.,self.rtol,self.atol))
        self.assertTrue(np.isinf(power_p(-3.,1.)))
        self.assertTrue(np.isinf(power_p(-3.,5.5551)))
        self.assertTrue(np.allclose(power_p(3.,2.),3.**2.,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_p(10.,7.8829),10.**7.8829,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_p(1000.,2.32),1000.**2.32,self.rtol,self.atol))
        self.assertTrue(np.allclose(power_p(10.,15.2),10.**15.2,self.rtol,self.atol))
        A = matrix([[1,4,-9],[2,-5,10]])
        f = power_p(A,5.68912)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        b = 5.68912
        B = matrix([[1.,4.**b,np.inf],[2.**b,np.inf,10.**b]])
        self.assertTrue(np.allclose(B,f,self.rtol,self.atol))
        x = variable()
        t = power_p(x,1.688)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'power_p')
        self.assertEqual(len(t.children),1)
        self.assertTrue(t.children[0] is x)
        a = parameter()
        t = power_p(a,3.333)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'power_p')
        self.assertTrue(t.children[0] is a)
        t = power_p(x+a,4.3)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'power_p')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,
                         c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,
                         c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)        
        X = variable(3,4)
        f = power_p(X,7.2)
        self.assertTrue(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'power_p')
                self.assertTrue(f[i,j].children[0] is X[i,j])
        A = parameter(3,4)
        f = power_p(A,4.5332)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'power_p')
                self.assertTrue(f[i,j].children[0] is A[i,j])
        f = power_p(A+X,1.688)
        self.assertEqual(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'power_p')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)
  
    def test_power_p_dcp(self):
        x = variable()
        b = 1.688
        self.assertTrue(power_p(x,b).is_dcp())
        self.assertFalse(power_p(x,b).is_affine())
        self.assertFalse(power_p(x,b).is_concave())
        self.assertTrue(power_p(x,b).is_convex())
        self.assertFalse(power_p(log(x),b).is_dcp())
        self.assertTrue(power_p(x+4+2*(x+10),b).is_convex())
        self.assertFalse(power_p(x+4+2*(x+10),b).is_concave())
        self.assertTrue(power_p(x+5*x-3*(x-10),b).is_dcp())
        self.assertFalse(power_p(-log(x),b).is_dcp())
        self.assertFalse(power_p(abs(x),b).is_convex())
        self.assertFalse(power_p(square(x),b).is_concave())
        self.assertFalse(power_p(sqrt(x),b).is_dcp())
        self.assertFalse(power_p(sqrt(x),b).is_concave())
        self.assertFalse(power_p(exp(x),b).is_dcp())
        self.assertFalse((-4*power_p(square(x),b)).is_concave())
        self.assertTrue((-4*power_p(2*x+10,b)).is_concave())
        a = parameter()                  
        self.assertTrue(power_p(a,b).is_dcp())
        self.assertTrue(power_p(x+a,b).is_dcp())
        self.assertTrue((power_p(x,b)+power_p(2*x,b)).is_convex())
        self.assertFalse((power_p(x,b)+power_p(2*x,b)).is_concave())
        self.assertFalse(power_p(square(a*x+1),b).is_convex())
        self.assertTrue(power_p(a*(a*x+1),b).is_convex())
        
    def test_power_p_in_prog(self):
        x = variable()
        p = program(minimize(x),[geq(x,-10.),leq(power_p(x,4.55),10.)])
        self.assertTrue(np.allclose(p(),0.,
                                    self.rtol,self.atol))
        p = program(minimize(power_p(x+1.,3.3)),[geq(x,2.)])
        self.assertTrue(np.allclose(p(),(2.+1.)**(3.3),
                                    self.rtol,self.atol))
        x = variable(10)
        p = program(maximize(sum(x)),[leq(power_p(x,1.688),10)])
        a = 10.**(1./1.688)
        aa = np.ones((10,1))*a
        p.solve(quiet=True)
        self.assertTrue(np.allclose(x.value,aa,
                                    self.rtol,self.atol))
        x = variable()
        p = program(minimize(power_p(x,1.688)),[geq(x,-4),leq(x,-3)])
        self.assertRaises(ValueError,p)
        
