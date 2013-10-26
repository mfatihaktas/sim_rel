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
from scipy.stats import norm

# Test function log_norm_cdf
class TestFunctionLogNormCDF(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_log_norm_cdf_call(self):
        self.assertRaises(TypeError,log_norm_cdf,[1])
        self.assertRaises(TypeError,log_norm_cdf,np.matrix([1,2,3]))
        self.assertTrue(np.allclose(log_norm_cdf(5),
                                    np.log(norm.cdf(5)),
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(log_norm_cdf(-5),
                                    np.log(norm.cdf(-5)),
                                    self.rtol,self.atol))
        A = matrix([[1,4,-9],[2,-5,10]])
        f = log_norm_cdf(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(2,3))
        self.assertTrue(np.allclose(np.log(norm.cdf(A)),
                                    f,self.rtol,self.atol))
        x = variable()
        t = log_norm_cdf(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log_norm_cdf')
        self.assertEqual(len(t.children),1)
        self.assertTrue(t.children[0] is x)
        a = parameter()
        t = log_norm_cdf(a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log_norm_cdf')
        self.assertTrue(t.children[0] is a)
        t = log_norm_cdf(x+a)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.name,'log_norm_cdf')
        self.assertEqual(len(t.children),1)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,
                         c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,
                         c.defs.SUMMATION)
        self.assertTrue(t.children[0].children[0] is x)
        self.assertTrue(t.children[0].children[1] is a)        
        X = variable(3,4)
        f = log_norm_cdf(X)
        self.assertTrue(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'log_norm_cdf')
                self.assertTrue(f[i,j].children[0] is X[i,j])
        A = parameter(3,4)
        f = log_norm_cdf(A)
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'log_norm_cdf')
                self.assertTrue(f[i,j].children[0] is A[i,j])
        f = log_norm_cdf(A+X)
        self.assertEqual(type(f),c.arrays.cvxpy_array)
        self.assertEqual(f.type,c.defs.ARRAY)
        self.assertEqual(f.shape,(3,4))
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f[i,j].type,c.defs.TREE)
                self.assertEqual(f[i,j].item.name,'log_norm_cdf')
                self.assertEqual(len(f[i,j].children),1)
                self.assertEqual(f[i,j].children[0].type,c.defs.TREE)
                self.assertEqual(f[i,j].children[0].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(f[i,j].children[0].item.name,
                                 c.defs.SUMMATION)
                self.assertEqual(len(f[i,j].children[0].children),2)
  
    def test_log_norm_cdf_dcp(self):
        x = variable()
        self.assertTrue(log_norm_cdf(x).is_dcp())
        self.assertFalse(log_norm_cdf(x).is_affine())
        self.assertFalse(log_norm_cdf(x).is_convex())
        self.assertTrue(log_norm_cdf(x).is_concave())
        self.assertTrue(log_norm_cdf(log(x)).is_dcp())
        self.assertTrue(log_norm_cdf(x+4+2*(x+10)).is_concave())
        self.assertTrue(log_norm_cdf(x+5*x-3*(x-10)).is_dcp())
        self.assertFalse(log_norm_cdf(-log(x)).is_dcp())
        self.assertTrue((-4*log_norm_cdf(x)).is_convex())
        a = parameter()                  
        self.assertTrue(log_norm_cdf(a).is_dcp())
        self.assertTrue(log_norm_cdf(x+a).is_dcp())
        self.assertTrue((log_norm_cdf(x)+log_norm_cdf(2*x)).is_concave())
        self.assertFalse((log_norm_cdf(x)+log_norm_cdf(2*x)).is_convex())
        self.assertTrue(log_norm_cdf(sqrt(a*x+1)).is_concave())

    def test_log_norm_cdf_in_prog(self):
        x = variable()
        p = program(minimize(x),[geq(log_norm_cdf(x+2),-10)])
        self.assertTrue(np.allclose(p(),
                                    -5.91394,
                                    self.rtol,self.atol))
        p = program(maximize(log_norm_cdf(x)),[leq(square(x),0.1)])
        self.assertTrue(np.allclose(p(),
                                    -0.47146859,
                                    self.rtol,self.atol))
