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

# Test function nuclear norm
class TestFunctionNuclearNorm(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_nuclear_norm_call(self):
        self.assertRaises(TypeError,nuclear_norm,[1,2,3])
        self.assertRaises(TypeError,nuclear_norm,np.array([1,2,3]))
        self.assertRaises(TypeError,nuclear_norm,np.matrix(np.zeros((2,3))))
        self.assertRaises(TypeError,nuclear_norm,{1:2})
        x = variable(2,4)
        t = nuclear_norm(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),8)
        self.assertTrue(t.children[7] is x[1,3])
        a = parameter(10,2)
        t = nuclear_norm(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),20)
        self.assertTrue(t.children[0] is a[0,0])
        t = nuclear_norm(a*4+variable(10,2))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),20)
        seed(1)
        A = randn(4,6)
        self.assertTrue(np.allclose(nuclear_norm(A),
                                    np.sum(np.linalg.svd(A)[1]),
                                    self.rtol,self.atol))
        A = 10*randn(1,5)
        self.assertTrue(np.allclose(nuclear_norm(A),
                                    np.sum(np.linalg.svd(A)[1]),
                                    self.rtol,self.atol))
        A = 4*randn(5,1)
        self.assertTrue(np.allclose(nuclear_norm(A),
                                    np.sum(np.linalg.svd(A)[1]),
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(nuclear_norm(2),2,self.rtol,self.atol))
        self.assertTrue(np.allclose(nuclear_norm(-2),2,self.rtol,self.atol))
        x = variable()
        t = nuclear_norm(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertTrue(t.children[0] is x)
        a = parameter()
        t = nuclear_norm(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertTrue(t.children[0] is a)
        t = nuclear_norm(a+x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertTrue(type(t.children[0]) is c.scalars.cvxpy_tree)

    def test_nuclear_norm_dcp(self):
        x = variable(2,5)
        self.assertTrue(nuclear_norm(x).is_dcp())
        self.assertTrue(nuclear_norm(x).is_convex())
        self.assertFalse(nuclear_norm(x).is_concave())
        self.assertFalse(nuclear_norm(x).is_affine())
        a = parameter()
        self.assertTrue(nuclear_norm(2*x+a).is_dcp())
        self.assertTrue(nuclear_norm(a*2*x+a).is_dcp())
        self.assertTrue(nuclear_norm(3*x+a).is_convex())
        self.assertFalse(nuclear_norm(4*x+a).is_concave())
        self.assertFalse(nuclear_norm(a*x-10).is_affine())
        self.assertFalse(nuclear_norm(square(x)).is_dcp())
        self.assertFalse(nuclear_norm(square(x)).is_dcp())

    def test_nuclear_norm_in_prog(self):
        x = variable(5,3)
        p =  program(minimize(nuclear_norm(2*x-1)),
                     [geq(x,1)])
        self.assertTrue(np.allclose(p(),3.87298,self.rtol,self.atol))
        p = program(maximize(sum(sqrt(x))),
                    [leq(nuclear_norm(x),4)])
        self.assertTrue(np.allclose(p(),15.243982,self.rtol,self.atol))
