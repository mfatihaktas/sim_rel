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

# Test function quad_form
class TestFunctionQuadForm(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_quad_form_call(self):
        A = randn(4,4)
        A = A.T*A
        self.assertRaises(ValueError,quad_form,1,A)
        self.assertRaises(ValueError,quad_form,variable(),A)
        self.assertRaises(ValueError,quad_form,parameter(),A)
        self.assertRaises(TypeError,quad_form,[1,2,variable()],A)
        self.assertRaises(TypeError,quad_form,parameter(3,1),
                          np.array(np.eye(3)))
        self.assertRaises(TypeError,quad_form,variable(4,1),
                          np.matrix(np.ones((3,3))))
        self.assertRaises(ValueError,quad_form,variable(2,1),
                          matrix([[1,2],[4,5]]))
        self.assertRaises(ValueError,quad_form,variable(2,1),
                          matrix([[1,0],[0,-2]]))
        self.assertRaises(ValueError,quad_form,variable(3,1),
                          matrix([[1,2,3],[4,5,6]]))
        self.assertRaises(ValueError,quad_form,variable(3,1),
                          matrix([[1,0],[0,2]]))
        self.assertRaises(ValueError,quad_form,variable(1,3),eye(3))
        self.assertRaises(ValueError,quad_form,ones((1,4)),eye(4))
        self.assertRaises(ValueError,quad_form,4,-10)
        self.assertTrue(np.allclose(quad_form(2,4),16,self.rtol,self.atol))
        self.assertTrue(np.allclose(quad_form(matrix([1,2,3]).T,2),
                                    28,self.rtol,self.atol))
        x = variable()
        t = quad_form(x,10)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        x = variable(4,1)
        t = quad_form(x,10)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        seed(1)
        x = rand(5,1)
        A = rand(10,5)
        A = A.T*A
        self.assertTrue(np.allclose(quad_form(x,A),
                                    float(x.T*A*x),
                                    self.rtol,self.atol))
        x = randn(3,1)
        A = randn(3,3)
        A = A.T*A
        self.assertTrue(np.allclose(quad_form(x,A),
                                    float(x.T*A*x),
                                    self.rtol,self.atol))
        x = variable(3,1)
        f = quad_form(x,A)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        a = parameter(3,1)
        f = quad_form(a,A)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        f = quad_form(2*x+a,A)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        self.assertRaises(TypeError,quad_form,x,parameter(3,3))

    def test_quad_form_dcp(self):
        x = variable(5,1)
        A = eye(5)
        self.assertTrue(quad_form(x,A).is_dcp())
        self.assertTrue(quad_form(x,A).is_convex())
        self.assertFalse(quad_form(x,A).is_concave())
        self.assertFalse(quad_form(x,A).is_affine())
        self.assertFalse(quad_form(huber(x),A).is_dcp())
        self.assertFalse(quad_form(huber(x),A).is_convex())
        self.assertFalse(quad_form(huber(x),A).is_concave())
        self.assertFalse(quad_form(huber(x),A).is_affine())
        self.assertFalse(quad_form(log(x),A).is_dcp())
        self.assertFalse(quad_form(log(x),A).is_convex())
        self.assertFalse(quad_form(log(x),A).is_concave())
        self.assertFalse(quad_form(log(x),A).is_affine())
        self.assertTrue(quad_form(3*x+2,A).is_dcp())
        self.assertTrue(quad_form(3*x+2,A).is_convex())
        self.assertFalse(quad_form(3*x+2,A).is_concave())
        self.assertFalse(quad_form(3*x+2,A).is_affine())
        self.assertTrue((quad_form(3*x+2,A)+norm2(x)-min(x)).is_convex())
        self.assertTrue(quad_form(parameter(5,1)+x,A).is_convex())

    def test_quad_form_in_prog(self):
        x = variable(4,1)
        A = matrix([[1,2,3,4],
                    [-4,-2,5,1]])
        A = A.T*A
        p = program(minimize(quad_form(x,A)),[greater_equals(sqrt(x),2)])
        self.assertTrue(np.allclose(p(),1600,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,4*ones((4,1)),
                                    self.rtol,self.atol))
        self.assertTrue(p.is_dcp())
        A = matrix([[1,2,3,4],
                    [-4,-2,5,1],
                    [0,0,3,7],
                    [3,3,3,2]])
        A = A.T*A
        p = program(maximize(sum(x)),[less_equals(quad_form(x,A),10)])
        self.assertTrue(np.allclose(p(),
                                    0.9321568,self.rtol,self.atol))
        f = matrix([1.609617,-1.2012819,0.816406,-0.2918377]).T
        self.assertTrue(np.allclose(x.value,f,1e-3,1e-4))
        self.assertTrue(p.is_dcp())
        x = variable()
        p = program(minimize(x),[leq(quad_form(x,10),40)])
        self.assertTrue(np.allclose(p(),-2,self.atol,self.atol))
        x = variable(2,1)
        p = program(minimize(sum(x)),[leq(quad_form(x,10),2)])
        self.assertTrue(np.allclose(p(),-0.632456,self.rtol,self.atol))
