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

# Test function kl_div
class TestFunctionKlDiv(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7
    
    def kl_numeric(self,x,y):
        temp = 0.
        for i in range(0,x.shape[0],1):
            temp += x[i,0]*np.log(x[i,0]/y[i,0])-x[i,0]+y[i,0]
        return temp
    
    def test_kl_div_call(self):
        x = np.matrix([1,2,3]).T
        y = variable(3,1)
        self.assertRaises(TypeError,kl_div,x,y)
        x = [1,2,3]
        self.assertRaises(TypeError,kl_div,x,y)
        x = variable(3,2)
        self.assertRaises(ValueError,kl_div,x,y)
        x = variable(3,1)
        y = np.matrix([1,2,3]).T
        self.assertRaises(TypeError,kl_div,x,y)
        y = [1,2,3]
        self.assertRaises(TypeError,kl_div,x,y)
        y = variable(3,2)
        self.assertRaises(ValueError,kl_div,x,y)
        x = parameter(3,1)
        y = parameter(4,1)
        self.assertRaises(ValueError,kl_div,x,y)
        x = vstack((variable(3,1),-5,variable(2,1)))
        y = vstack((4,variable(3,1),1,9))
        self.assertEqual(kl_div(x,y),np.inf)
        x = vstack((variable(3,1),5,variable(2,1)))
        y = vstack((4,variable(3,1),1,-9))
        self.assertEqual(kl_div(x,y),np.inf)
        self.assertEqual(kl_div(0,3),np.inf)
        x = variable(name='x')
        y = variable(name='y')
        f = kl_div(x,y)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertEqual(len(f.children),2)
        self.assertTrue(f.children[0] is x)
        self.assertTrue(f.children[1] is y)
        a = parameter(3,1)
        b = parameter(3,1)
        f = kl_div(a+1,b)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertEqual(len(f.children),6)
        self.assertTrue(f.children[0].children[0] is a[0,0])
        self.assertEqual(f.children[0].children[1].type,c.defs.CONSTANT)
        self.assertEqual(f.children[0].children[1].value,1)
        self.assertTrue(f.children[3] is b[0,0])
        x = matrix([1,2,3]).T
        y = matrix([4,5,6]).T
        self.assertTrue(np.allclose(kl_div(x,y),self.kl_numeric(x,y),
                                    self.rtol,self.atol))
        seed(1)
        x1 = rand(10,1)
        y1 = rand(10,1)
        self.assertTrue(np.allclose(kl_div(x1,y1),
                                    self.kl_numeric(x1,y1),
                                    self.rtol,self.atol))    
        x2 = rand(1,1)
        y2 = rand(1,1)
        self.assertTrue(np.allclose(kl_div(x2,y2),
                                    self.kl_numeric(vstack([x2]),
                                                    vstack([y2])),
                                    self.rtol,self.atol))    
        x1 = variable()
        x = vstack((x1,10))
        y1 = variable()
        y = vstack((20,y1))
        f = kl_div(x,y)
        self.assertEqual(f.type,c.defs.TREE)
        y = vstack((-20,y1))
        f = kl_div(x,y)
        self.assertEqual(f,np.inf)

    def test_kl_div_dcp(self):
        x = variable(3,1)
        y = variable(3,1)
        f = kl_div(2*x,y+10)
        self.assertTrue(f.is_dcp())
        self.assertTrue(f.is_convex())
        self.assertFalse(f.is_concave())
        self.assertFalse(f.is_affine())
        a = parameter(attribute='nonpositive')
        f = a*kl_div(10*x+y,y)
        self.assertTrue(f.is_dcp())
        self.assertFalse(f.is_convex())
        self.assertTrue(f.is_concave())
        self.assertFalse(f.is_affine())
        f = kl_div(square(x),y)
        self.assertFalse(f.is_dcp())
        f = kl_div(x,sqrt(y))
        self.assertFalse(f.is_dcp())
        f = kl_div(log_norm_cdf(x),y)
        self.assertFalse(f.is_dcp())

    def test_kl_div_in_prog(self):
        x = variable(4,1)
        y = variable(4,1)
        p = program(minimize(kl_div(x,y)),
                    [eq(sum(x),1),eq(sum(y),1),
                     leq(x[2,0],0.3),
                     geq(y[2,0],0.8)])
        self.assertTrue(np.allclose(p(),0.5826853017,self.rtol,self.atol))
        p = program(minimize(kl_div(vstack((1,x)),
                                           vstack((y,4)))),
                    [leq(norm2(x),0.4),
                     geq(y,0.7)])
        self.assertTrue(np.allclose(p(),3.8646264856,self.rtol,self.atol))
