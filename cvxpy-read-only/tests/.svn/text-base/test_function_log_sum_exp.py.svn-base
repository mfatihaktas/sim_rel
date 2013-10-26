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

# Test function log_sum_exp
class TestFunctionLogSumExp(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_log_sum_exp_call(self):
        self.assertTrue(log_sum_exp(1) is 1)
        x = variable()
        self.assertTrue(log_sum_exp(x) is x)
        self.assertTrue(log_sum_exp(vstack([x])) is x)
        self.assertRaises(TypeError,log_sum_exp,np.matrix([1,2,3]))
        self.assertRaises(ValueError,log_sum_exp,parameter(4,4))
        self.assertRaises(ValueError,log_sum_exp,variable(2,3))
        self.assertRaises(ValueError,log_sum_exp,ones((4,4)))
        self.assertRaises(TypeError,log_sum_exp,(1,2,3))
        self.assertRaises(TypeError,log_sum_exp,[1,2,variable()])
        self.assertRaises(ValueError,log_sum_exp,variable(1,4))
        self.assertRaises(ValueError,log_sum_exp,matrix([1,3,4]))
        self.assertRaises(ValueError,log_sum_exp,
                          hstack([x,parameter()]))
        self.assertTrue(np.allclose(log_sum_exp(matrix([1,2,3]).T),
                                    np.log(np.sum(np.exp(matrix([1,2,3])))),
                                    self.rtol,self.atol))
        A = matrix([[1,-2,3]]).T
        f = log_sum_exp(A)
        self.assertTrue(np.allclose(np.log(np.sum(np.exp(A))),
                                    f,self.rtol,self.atol))
        a = parameter()
        t = log_sum_exp(vstack([a,x]))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log_sum_exp')
        self.assertEqual(len(t.children),2)
        t = log_sum_exp(vstack([x,a,2]))
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log_sum_exp')
        self.assertEqual(len(t.children),3)
        self.assertEqual(t.children[2].type,c.defs.CONSTANT)
        self.assertEqual(t.children[2].value,2)
        X = variable(3,1)
        f = log_sum_exp(X)
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'log_sum_exp')
        self.assertEqual(len(f.children),3)
        A = parameter(1,3)
        f = log_sum_exp(A.T)
        self.assertTrue(type(f),c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'log_sum_exp')
        self.assertEqual(len(f.children),3)
        f = log_sum_exp(vstack((A.T,X)))
        self.assertTrue(type(f) is c.scalars.cvxpy_tree)
        self.assertEqual(f.type,c.defs.TREE)
        self.assertEqual(f.shape,(1,1))
        self.assertEqual(f.item.name,'log_sum_exp')
        self.assertEqual(len(f.children),6)

    def test_log_sum_exp_dcp(self):
        x = variable()
        self.assertTrue(log_sum_exp(hstack([x])).is_dcp())
        self.assertTrue(log_sum_exp(vstack([x])).is_affine())
        self.assertTrue(log_sum_exp(variable(4,1)).is_convex())
        self.assertFalse(log_sum_exp(variable(1,3).T).is_concave())
        self.assertTrue(log_sum_exp(vstack((square(x),10,
                                            -sqrt(x+1)))).is_dcp())
        self.assertFalse(log_sum_exp(vstack((square(x),10,
                                             sqrt(x+1)))).is_dcp())
        self.assertTrue(log_sum_exp(vstack([x,x+10,abs(x+10)])).is_dcp())
        self.assertFalse(log_sum_exp(vstack([sqrt(x),x])).is_dcp())
        a = parameter()
        self.assertTrue(log_sum_exp(a).is_dcp())
        self.assertTrue(log_sum_exp(vstack((x,a))).is_dcp())
        self.assertTrue((log_sum_exp(vstack([x,square(x)]))+
                         log_sum_exp(vstack((x,x+1)))).is_convex())
        self.assertFalse((log_sum_exp(vstack([x,square(x)]))+
                          log_sum_exp(vstack((x,x+1)))).is_affine())
        self.assertFalse((log_sum_exp(vstack([x,abs(x)]))+
                          log_sum_exp(vstack((x,x+1)))).is_concave())

    def test_log_sum_exp_in_prog(self):
        x = variable()
        y = variable()
        p = program(maximize(x+y),
                    [less_equals(log_sum_exp(vstack([x,y])),4)])
        self.assertTrue(np.allclose(p(),6.613705,self.rtol,self.atol))
        p = program(minimize(log_sum_exp(vstack((x,y)))),
                          [greater_equals(hstack((x,y)),matrix([1,2]))])
        self.assertTrue(np.allclose(p(),
                                    np.log(np.sum(np.exp(matrix([1,2])))),
                                    self.rtol,self.atol))
        z = variable()
        p = program(minimize(log_sum_exp(vstack((x,3,4,y,z)))),
                 [less_equals(abs(vstack((x,y,z,1))),2)])
        self.assertTrue(np.allclose(p(),4.318683329,self.rtol,self.atol))
