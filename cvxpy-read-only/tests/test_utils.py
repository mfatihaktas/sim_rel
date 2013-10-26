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

# Test utils
class TestUtils(unittest.TestCase):

    # hstack
    def test_hstack(self):
        self.assertRaises(TypeError,hstack,1)
        self.assertRaises(TypeError,hstack, 1)
        self.assertRaises(TypeError,hstack,variable())
        self.assertRaises(TypeError,hstack,np.matrix([1,2,3]))
        f = hstack((1,2,3))
        for i in range(0,3):
            self.assertEqual(f[0,i],i+1)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        f = hstack([1,2,3])
        for i in range(0,3):
            self.assertEqual(f[0,i],i+1)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        f = hstack([0,1,2,matrix([3,4,5])])
        for i in range(0,6):
            self.assertEqual(f[0,i],i)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertRaises(TypeError,hstack,(1,2,np.matrix([1,2,3])))
        self.assertRaises(ValueError,hstack,(1,2,matrix([1,2,3]).T))
        f = hstack((eye(3),ones((3,5))))
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(3,8))
        o = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        f = hstack((2,3,o))
        self.assertEqual(f[0,2],5)
        x = variable()
        f = hstack([x,x,2,o,ones((1,4))])
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.shape,(1,8))
        X = variable(3,4)
        A = parameter(3,4)
        f = hstack((X,A,X+A,ones((3,2))))
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.shape,(3,14))
        for i in range(0,3):
            for j in range(0,4):
                self.assertTrue(f[i,j] is X[i,j])
                self.assertTrue(f[i,j+4] is A[i,j])
                self.assertTrue(type(f[i,j+8]) is c.scalars.cvxpy_tree)
                self.assertEqual(len(f[i,j+8].children),2)
        self.assertTrue(np.allclose(f[:,12:].value,ones((3,2))))
        a = parameter()
        b = parameter()
        a.value = 1
        b.value = 2
        f = hstack((a,b))
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertTrue(np.allclose(f.value,matrix([1,2])))
        self.assertRaises(ValueError,hstack,[variable(2,3),parameter(5,2)])

    # vstack
    def test_vstack(self):
        self.assertRaises(TypeError,vstack,1)
        self.assertRaises(TypeError,vstack, 1)
        self.assertRaises(TypeError,vstack,variable())
        self.assertRaises(TypeError,vstack,np.matrix([1,2,3]))
        f = vstack((1,2,3))
        for i in range(0,3):
            self.assertEqual(f[i,0],i+1)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        f = vstack([1,2,3])
        for i in range(0,3):
            self.assertEqual(f[i,0],i+1)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        f = vstack([0,1,2,matrix([3,4,5]).T])
        for i in range(0,6):
            self.assertEqual(f[i,0],i)
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertRaises(TypeError,vstack,(1,2,np.matrix([1,2,3]).T))
        self.assertRaises(ValueError,vstack,(1,2,matrix([1,2,3])))
        f = vstack((eye(3),ones((5,3))))
        self.assertTrue(type(f) is c.arrays.cvxpy_matrix)
        self.assertEqual(f.shape,(8,3))
        o = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        f = vstack((2,3,o))
        self.assertEqual(f[2,0],5)
        x = variable()
        f = vstack([x,x,2,o,ones((4,1))])
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.shape,(8,1))
        X = variable(3,4)
        A = parameter(3,4)
        f = vstack((X,A,X+A,ones((2,4))))
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertEqual(f.shape,(11,4))
        for i in range(0,3):
            for j in range(0,4):
                self.assertTrue(f[i,j] is X[i,j])
                self.assertTrue(f[i+3,j] is A[i,j])
                self.assertTrue(type(f[i+6,j]) is c.scalars.cvxpy_tree)
                self.assertEqual(len(f[i+6,j].children),2)
        self.assertTrue(np.allclose(f[9:,:].value,ones((2,4))))
        a = parameter()
        b = parameter()
        a.value = 1
        b.value = 2
        f = vstack((a,b))
        self.assertTrue(type(f) is c.arrays.cvxpy_array)
        self.assertTrue(np.allclose(f.value,matrix([1,2]).T))
        self.assertRaises(ValueError,vstack,[variable(2,3),parameter(5,2)])

    # sum
    def test_sum(self):
        self.assertEqual(sum(1),1)
        x = variable()
        self.assertTrue(sum(x) is x)
        a = parameter()
        self.assertTrue(sum(a) is a)
        t = a+x 
        self.assertTrue(sum(t) is t)
        A = matrix([[1,2,3],[4,5,6]])
        self.assertEqual(sum(A),21)
        X = variable(3,2)
        t = sum(X)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(len(t.children),6)
        for i in range(0,3):
            for j in range(0,2):
                self.assertTrue(t.children[i*2+j] is X[i,j])
        t = sum([1,2,x,a])
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(len(t.children),3)
        self.assertEqual(t.children[0].value,3)
        self.assertEqual(t.children[0].type,c.defs.CONSTANT)
        self.assertTrue(t.children[2] is a)
        self.assertTrue(t.children[1] is x)
        t = sum([1,x,a,X])
        self.assertTrue(type(t) is c.arrays.cvxpy_array)
        self.assertTrue(type(t[0,0]) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t[0,0].children),4)
        self.assertEqual(t[0,0].children[0].type,c.defs.CONSTANT)
        self.assertTrue(t[0,0].children[3] is X[0,0])
        A = matrix([1,2])
        self.assertTrue(np.allclose(matrix([2,4]),sum((A,A))))
        b = parameter(2,1)
        t = sum((b,b,1))
        self.assertTrue(type(t) is c.arrays.cvxpy_array)
        self.assertEqual(t.shape,(2,1))
        self.assertTrue(type(t[0,0]) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t[0,0].children),3)
        self.assertTrue(type(t[0,0].children[2]) is 
                        c.scalars.cvxpy_obj)
        self.assertRaises(TypeError,sum,np.array([1,2,3]))        

    # randn
    def test_randn(self):
        a = randn(4,2)
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(4,2))
        a = randn(0,2)
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(0,2))

    # rand
    def test_rand(self):
        a = rand(4,2)
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(4,2))
        a = rand(2,0)
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(2,0))
    
    # eye
    def test_eye(self):
        a = eye(5)
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(5,5))
        self.assertTrue(np.allclose(a,np.eye(5)))
        a = eye(0)
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(0,0))

    # zeros
    def test_zeros(self):
        a = zeros((3,2))
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(3,2))
        self.assertTrue(np.allclose(a,np.zeros((3,2))))
        a = zeros((3,0))
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(3,0))

    # zeros
    def test_ones(self):
        a = ones((2,3))
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(2,3))
        self.assertTrue(np.allclose(a,np.ones((2,3))))
        a = ones((0,2))
        self.assertTrue(type(a) is c.arrays.cvxpy_matrix)
        self.assertEqual(a.shape,(0,2))

    # diag
    def test_diag(self):
        X = variable(3,3)
        s1 = diag(X)
        self.assertTrue(type(s1) is c.arrays.cvxpy_array)
        self.assertEqual(s1.shape,(3,1))
        for i in range(0,3):
            self.assertTrue(s1[i,0] is X[i,i])
        a = parameter()
        s2 = diag(X+a)
        self.assertTrue(type(s2) is c.arrays.cvxpy_array)
        self.assertEqual(s2.shape,(3,1))
        for i in range(0,3):
            self.assertTrue(type(s2[i,0]) is c.scalars.cvxpy_tree)
            self.assertTrue(s2[i,0].children[0] is X[i,i])
            self.assertTrue(s2[i,0].children[1] is a)
        A = matrix([[1,2,3],[4,5,6],[7,8,9]])
        self.assertTrue(type(diag(A)) is c.arrays.cvxpy_matrix)
        self.assertTrue(np.allclose(diag(A),matrix([1,5,9]).T))
        self.assertEqual(diag(2),2)
        x = variable()
        self.assertTrue(diag(x) is x)
        self.assertTrue(diag(a) is a)
        t = a*x
        self.assertTrue(diag(t) is t)
        A = matrix([[1,2,3],[4,5,6]])
        self.assertRaises(ValueError,diag,A)
        self.assertRaises(ValueError,diag,parameter(5,4))
        self.assertRaises(TypeError,diag,np.ones((4,40)))
        self.assertRaises(TypeError,diag,np.matrix([[1,2],[3,4]]))
        self.assertRaises(TypeError,diag,[variable(2,2),ones((2,4))])
        self.assertRaises(TypeError,diag,[variable(2,2),ones((1,4))])
        self.assertRaises(TypeError,diag,(1,2,3,4))
        self.assertRaises(TypeError,diag,[variable(),parameter(),2])
        self.assertRaises(ValueError,diag,variable(3,2)+parameter(3,2))
        t = diag(matrix([1,2,3]))
        self.assertTrue(type(t) is c.arrays.cvxpy_matrix)
        self.assertTrue(np.allclose(t,matrix([[1,0,0],[0,2,0],[0,0,3]])))
        t = diag(matrix([1,2,3]).T)
        self.assertTrue(type(t) is c.arrays.cvxpy_matrix)
        self.assertTrue(np.allclose(t,matrix([[1,0,0],[0,2,0],[0,0,3]])))
        x = variable(1,4)
        t = diag(x)
        self.assertTrue(type(t) is c.arrays.cvxpy_array)
        self.assertEqual(t.shape,(4,4))
        for i in range(0,4):
            self.assertTrue(t[i,i] is x[0,i])
            for j in range(0,4):
                if j!=i:
                    self.assertEqual(t[i,j],0)
        x = variable(4,1)
        t = diag(x)
        self.assertTrue(type(t) is c.arrays.cvxpy_array)
        self.assertEqual(t.shape,(4,4))
        for i in range(0,4):
            self.assertTrue(t[i,i] is x[i,0])
            for j in range(0,4):
                if j!=i:
                    self.assertEqual(t[i,j],0)

    # sqrtm
    def test_sqrtm(self):
        A = matrix([[4,0,0],[0,9,0],[0,0,25]])
        t = sqrtm(A)
        self.assertTrue(type(t) is c.arrays.cvxpy_matrix)
        self.assertTrue(np.allclose(t,matrix([[2,0,0],[0,3,0],[0,0,5]])))

    # trace
    def test_trace(self):
        seed(1)
        self.assertRaises(TypeError,trace,np.matrix([[1,2],[3,4]]))
        self.assertRaises(TypeError,trace,[1,2,3])
        self.assertRaises(TypeError,trace,np.ones((4,4)))
        self.assertEqual(trace(5),5)
        x = variable()
        self.assertTrue(trace(x) is x)
        a = parameter()
        self.assertTrue(trace(a) is a)
        t = abs(x) + a
        self.assertTrue(trace(t) is t)
        self.assertRaises(ValueError,trace,ones((4,5)))
        self.assertRaises(ValueError,trace,variable(2,3))
        self.assertRaises(ValueError,trace,parameter(1,7))
        self.assertRaises(ValueError,trace,parameter(4,2)+variable(4,2))
        seed(1)
        A = randn(10,10)
        self.assertEqual(trace(A),np.trace(A))
        A = parameter(2,2)
        t = trace(A)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.SUMMATION)
        self.assertTrue(t.children[0] is A[0,0])
        self.assertTrue(t.children[1] is A[1,1])
        X = variable(3,3)
        B = parameter(3,3)
        t = trace(X+B+1)
        self.assertTrue(type(t) is c.scalars.cvxpy_tree)
        self.assertEqual(len(t.children),9)
        self.assertTrue(t.children[0] is X[0,0])
        self.assertTrue(t.children[1] is B[0,0])
        self.assertEqual(t.children[2].type, c.defs.CONSTANT)
        self.assertTrue(t.children[3] is X[1,1])

    # reshape
    def test_reshape(self):
        X = variable(2,3)
        s1 = reshape(X, (3, 2))
        self.assertTrue(type(s1) is c.arrays.cvxpy_array)
        self.assertEqual(s1.shape,(3,2))
        self.assertTrue(X[0,0] is s1[0,0])
        self.assertTrue(X[1,0] is s1[1,0])
        self.assertTrue(X[0,1] is s1[2,0])
        self.assertTrue(X[1,1] is s1[0,1])
        self.assertTrue(X[0,2] is s1[1,1])
        self.assertTrue(X[1,2] is s1[2,1])

        a = parameter()
        Xa = X + a
        s2 = reshape(Xa, (3, 2))
        self.assertTrue(type(s2) is c.arrays.cvxpy_array)
        self.assertTrue(Xa[0,0] is s2[0,0])
        self.assertTrue(Xa[1,0] is s2[1,0])
        self.assertTrue(Xa[0,1] is s2[2,0])
        self.assertTrue(Xa[1,1] is s2[0,1])
        self.assertTrue(Xa[0,2] is s2[1,1])
        self.assertTrue(Xa[1,2] is s2[2,1])


        A = matrix([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
        self.assertTrue(type(reshape(A, (3, 4))) is c.arrays.cvxpy_matrix)
        self.assertTrue((np.reshape(A, (3,4), order='F') == reshape(A, (3, 4))).all())

        self.assertRaises(TypeError,reshape,1.0,(3,4))
        self.assertRaises(TypeError,reshape,A,2)
        self.assertRaises(TypeError,reshape,np.ones((4,40)), (2, 3))
        self.assertRaises(ValueError,reshape,variable(2, 2), (3, 3))
