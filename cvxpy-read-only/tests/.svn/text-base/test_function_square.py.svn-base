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

# Test function square
class TestFunctionSquare(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_square_call(self):
        self.assertRaises(TypeError,square,[1])
        self.assertRaises(TypeError,square,np.matrix([1,2,3]))
        self.assertRaises(TypeError,square,
                          c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5)))
        self.assertTrue(np.allclose(square(-5),25,self.rtol,self.atol))
        self.assertTrue(np.allclose(square(5),25,self.rtol,self.atol))
        A = matrix([[1,-2,3],[-3,-4,5]])
        f = square(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        self.assertTrue(np.allclose(np.square(A),f,self.rtol,self.atol))
        x = variable()
        t = square(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'square')
        self.assertEqual(len(t.children),1)
        a = parameter()
        t = square(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'square')
        self.assertEqual(len(t.children),1)
        t = square(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'square')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,
                         c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,
                         c.defs.SUMMATION)
        self.assertEqual(len(t.children[0].children),2)
        X = variable(3,4)
        f = square(X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'square')
                self.assertEqual(len(f[i,j].children),1)
        A = parameter(3,4)
        f = square(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'square')
                self.assertEqual(len(f[i,j].children),1)
        f = square(A+X)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'square')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)
    
    def test_square_dcp(self):
        x = variable()
        self.assertTrue(square(x).is_dcp())
        self.assertFalse(square(x).is_affine())
        self.assertTrue(square(x).is_convex())
        self.assertFalse(square(x).is_concave())
        self.assertFalse(square(square(x)).is_dcp())
        self.assertTrue(square(x+4+2*(x+10)).is_convex())
        self.assertTrue(square(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse(square(sqrt(x)).is_dcp())
        a = parameter()
        self.assertTrue(square(a).is_dcp())
        self.assertTrue(square(x+a).is_dcp())
        self.assertTrue((square(x)+ square(2*x)-3*(x+10)).is_convex())
        self.assertFalse((square(x)+ square(2*x)-3*(x+10)).is_concave())
        self.assertFalse((square(x)+ square(2*x)-3*(x+10)).is_affine())

    def test_square_in_prog(self):
        x = variable()
        p = program(minimize(x),[less_equals(square(x+10),4)])
        self.assertTrue(np.allclose(p(),-12,self.rtol,self.atol))
        p = program(maximize(x),[less_equals(square(x+10),4)])
        self.assertTrue(np.allclose(p(),-8,self.rtol,self.atol))
