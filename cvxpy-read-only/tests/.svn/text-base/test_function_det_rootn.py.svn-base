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

# Test function det_rootn
class TestFunctionDetRootn(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_det_rootn_call(self):
        self.assertRaises(TypeError,det_rootn,[1])
        self.assertRaises(TypeError,det_rootn,np.matrix([[1,2],[4,5]]))
        self.assertRaises(ValueError,det_rootn,matrix([[1,2,3],[4,5,6]]))
        self.assertRaises(ValueError,det_rootn,variable(4,3))
        self.assertTrue(np.allclose(det_rootn(4),4,self.rtol,self.atol))
        self.assertEqual(det_rootn(-5),-np.inf)
        x = variable()
        t = det_rootn(x)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertTrue(t.children[0] is x)
        A = matrix([[1,0],[0,-2]])
        self.assertEqual(det_rootn(A),-np.inf)
        A = matrix([[1,2],[3,4]])
        self.assertEqual(det_rootn(A),-np.inf)
        X = variable(3,3)
        f = det_rootn(X)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertTrue(f.children[i*3+j] is X[i,j])
        self.assertEqual(f.item.name,'det_rootn')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A = parameter(3,3)
        f = det_rootn(A)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertTrue(f.children[i*3+j] is A[i,j])
        self.assertEqual(f.item.name,'det_rootn')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        A.value = eye(3)
        self.assertTrue(np.allclose(f.value,1,self.rtol,self.atol))
        f = det_rootn(A+X)
        self.assertEqual(f.type,c.defs.TREE)
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertEqual(f.children[i*3+j].type,c.defs.TREE)
                self.assertTrue(f.children[i*3+j].children[0] is A[i,j])
                self.assertTrue(f.children[i*3+j].children[1] is X[i,j])
        self.assertEqual(f.item.name,'det_rootn')
        self.assertEqual(f.item.type,c.defs.FUNCTION)
        X = matrix([[1,2,3],[4,5,6],[7,8,9]])
        X = X.T*X+0.1*eye(3)
        self.assertTrue(np.allclose(det_rootn(X),
                                    np.linalg.det(X)**(1./3.),
                                    self.rtol,self.atol))
        seed(1)
        X = randn(3,3)
        X = X*X.T
        self.assertTrue(np.allclose(det_rootn(X),
                                    np.linalg.det(X)**(1./3.),
                                    self.rtol,self.atol))
           
    def test_det_rootn_dcp(self):
        X = variable(4,4)
        self.assertTrue(det_rootn(X).is_concave())
        self.assertFalse(det_rootn(X).is_convex())
        self.assertTrue(det_rootn(X).is_dcp())
        self.assertFalse(det_rootn(X).is_affine())
        A = matrix([[1,2,3,4],[5,6,7,8]])
        A = vstack((A,A))
        b = eye(4)
        self.assertTrue(det_rootn(A*X+b).is_concave())
        self.assertFalse(det_rootn(A*X+b).is_convex())
        self.assertTrue(det_rootn(A*X+b).is_dcp())
        self.assertFalse(det_rootn(A*X+b).is_affine())
        self.assertFalse(det_rootn(square(X)).is_concave())
        self.assertFalse(det_rootn(square(X)).is_convex())
        self.assertFalse(det_rootn(square(X)).is_dcp())
        self.assertFalse(det_rootn(sqrt(X)).is_dcp())
        A = parameter(4,4)
        self.assertTrue(det_rootn(X+A).is_concave())
        self.assertFalse(det_rootn(X+A).is_convex())
        self.assertTrue(det_rootn(X+A).is_dcp())
        self.assertTrue((-10*det_rootn(-X+1)).is_convex())
        self.assertFalse((-10*det_rootn(-X+1)).is_concave())
        self.assertTrue((-10*det_rootn(-X+1)).is_dcp())
        x = variable()
        self.assertTrue(geo_mean(x+1).is_dcp())
        
    def test_det_rootn_in_prog(self):
        x = variable(3,3,'lower_triangular')
        p = program(maximize(det_rootn(x)),[less_equals(lambda_max(x),2)])
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))
        self.assertTrue(p.is_dcp())
        self.assertTrue(np.allclose(x.value,2*eye(3),
                                    self.rtol,self.atol))
        x = variable()
        p = program(minimize(x),[geq(x,2),geq(det_rootn(x),3)])
        self.assertTrue(np.allclose(p(),3,self.rtol,self.atol))
        p = program(minimize(x),[geq(x,-2),geq(det_rootn(x),-2)])
        self.assertTrue(np.allclose(p(),0,self.rtol,self.atol))
        
