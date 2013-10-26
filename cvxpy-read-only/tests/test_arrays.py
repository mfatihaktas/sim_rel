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
import cvxpy as c
import numpy as np
from cvxpy import *
import scipy.sparse as sp

# Test arrays
class TestArrays(unittest.TestCase):

    # cvxpy_array
    def test_cvxpy_array_init(self):
        f = c.arrays.cvxpy_array(4,3)
        self.assertEqual(f.shape,(4,3))
        self.assertEqual(f.type,c.defs.ARRAY)
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                self.assertEqual(f.data[i][j],0.0)
                
    def test_cvxpy_array_getattribute(self):
        f = c.arrays.cvxpy_array(4,3)
        self.assertEqual(f.T.shape,(3,4))
        x = c.arrays.cvxpy_var(4,3)
        self.assertEqual(x.shape,(4,3))
        self.assertEqual(x.T.shape,(3,4))
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(x[i,j],x.T[j,i])
        a = parameter(3,5)
        self.assertEqual(a.shape,(3,5))
        self.assertEqual(a.T.shape,(5,3))
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(a[i,j],a.T[j,i])
        y = c.scalars.cvxpy_scalar_var()
        b = c.scalars.cvxpy_scalar_param()
        f = vstack((y,b,10))
        self.assertEqual([y],f.variables)
        self.assertEqual([b],f.parameters)
        self.assertTrue(type(f.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(f.parameters) is c.constraints.cvxpy_list)
        self.assertTrue(type(x.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(x.parameters) is c.constraints.cvxpy_list)
        self.assertTrue(type(a.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(a.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(12,len(x.variables))
        for i in range(0,4,1):
            for j in range(0,3,1):
                self.assertTrue(x[i,j] in x.variables)
        self.assertEqual(x.parameters,[])
        self.assertEqual(a.variables,[])
        self.assertEqual(15,len(a.parameters))
        for i in range(0,3,1):
            for j in range(0,4,1):
                self.assertTrue(a[i,j] in a.parameters)        
        A = matrix([[1,2,3],[4,5,6],[7,8,9]])
        f = c.arrays.cvxpy_array(A.shape[0],A.shape[1])
        for i in range(0,f.shape[0],1):
            for j in range(0,f.shape[1],1):
                f[i,j] = A[i,j]
        self.assertTrue(np.allclose(A,f.value))
        self.assertTrue(type(f.value) is c.arrays.cvxpy_matrix)
        X = variable(4,3)
        B = zeros((X.shape[0],X.shape[1]))
        for i in range(0,X.shape[0],1):
            for j in range(0,X.shape[1],1):
                X[i,j].value = i+2.0*j
                B[i,j] = i+2.0*j
        self.assertTrue(np.allclose(X.value,B))
        self.assertTrue(type(X.value) is c.arrays.cvxpy_matrix)
        A = parameter(3,5)
        for i in range(0,3,1):
            for j in range(0,5,1):
                A[i,j].value = 1.0
        self.assertTrue(np.allclose(A.value,ones((3,5))))
        self.assertTrue(type(A.value) is c.arrays.cvxpy_matrix)
        
    def test_cvxpy_array_setitem(self):
        f = c.arrays.cvxpy_array(3,7)
        self.assertRaises(TypeError,f.__setitem__,5,10)
        self.assertRaises(TypeError,f.__setitem__,[1,2],20)
        self.assertRaises(TypeError,f.__setitem__,(1,2,3),10)
        self.assertRaises(TypeError,f.__setitem__,([1,2,3],2),10)
        self.assertRaises(TypeError,f.__setitem__,(2,[1,2,3]),10)
        self.assertRaises(TypeError,f.__setitem__,(slice(0,2,1),1),1)
        self.assertRaises(TypeError,f.__setitem__,(1,slice(0,2,1)),1)
        self.assertRaises(TypeError,f.__setitem__,(slice(0,2,1),slice(0,2,1)),1)
        x = c.scalars.cvxpy_scalar_var()
        f.__setitem__((1,2),x)
        self.assertTrue(f[1,2] is x)
        self.assertRaises(ValueError,f.__setitem__,(-1,3),1)
        self.assertRaises(ValueError,f.__setitem__,(0,-1),1)
        self.assertRaises(ValueError,f.__setitem__,(3,0),1)
        self.assertRaises(ValueError,f.__setitem__,(0,7),1)
        a = parameter()
        f.__setitem__((np.int64(2),np.int64(6)),a)
        self.assertTrue(f[2,6] is a)
        self.assertRaises(TypeError,f.__setitem__,(3.3,2),10)
        self.assertRaises(TypeError,f.__setitem__,(3,2.2),10)
        b = parameter()
        f.__setitem__((np.int8(2),np.int16(6)),b)
        self.assertTrue(f[np.uint(2),np.int64(6)] is b)

    def test_cvxpy_array_getitem(self):
        f = c.arrays.cvxpy_array(4,3)
        self.assertRaises(TypeError,f.__getitem__,4)
        self.assertRaises(TypeError,f.__getitem__,(1,2,3))
        self.assertRaises(TypeError,f.__getitem__,(2.3,0))
        self.assertRaises(TypeError,f.__getitem__,(0,1.3))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,1),slice(0,2,float(1))))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,1),slice(0,float(2),1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,1),slice(np.float64(0),2,1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,np.float(1)),slice(0,2,1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(float(0),2,1),slice(0,2,1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,np.float64(2),1),slice(0,2,1)))
        A = matrix([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
        for i in range(0,A.shape[0],1):
            for j in range(0,A.shape[1],1):
                f[i,j] = A[i,j]
                self.assertEqual(f[i,j],A[i,j])
        f1 = f[1:np.int64(3):1,np.uint(1):3:np.int8(1)]
        A1 = A[1:3:1,1:3:1]
        for i in range(0,A1.shape[0],1):
            for j in range(0,A1.shape[1],1):
                self.assertEqual(f1[i,j],A1[i,j])
        f2 = f[1:3,1:np.int64(3)]
        A2 = A[1:3,1:3]
        for i in range(0,A2.shape[0],1):
            for j in range(0,A2.shape[1],1):
                self.assertEqual(f2[i,j],A2[i,j])
        f3 = f[1:,1:]
        A3 = A[1:,1:]
        for i in range(0,A3.shape[0],1):
            for j in range(0,A3.shape[1],1):
                self.assertEqual(f3[i,j],A3[i,j])
        f4 = f[:3,:3]
        A4 = A[:3,:3]
        for i in range(0,A4.shape[0],1):
            for j in range(0,A4.shape[1],1):
                self.assertEqual(f4[i,j],A4[i,j])
        f5 = f[:,:]
        A5 = A[:,:]
        for i in range(0,A5.shape[0],1):
            for j in range(0,A5.shape[1],1):
                self.assertEqual(f5[i,j],A5[i,j])
        f6 = f.__getitem__((slice(1,None,None),slice(1,None,None))) #f[1:,1:]
        A6 = A[1:,1:]
        for i in range(0,A6.shape[0],1):
            for j in range(0,A6.shape[1],1):
                self.assertEqual(f6[i,j],A6[i,j])
        self.assertRaises(ValueError,f.__getitem__,(-1,2))
        self.assertRaises(ValueError,f.__getitem__,(4,2))
        self.assertRaises(ValueError,f.__getitem__,(1,-1))
        self.assertRaises(ValueError,f.__getitem__,(1,3))
        self.assertRaises(ValueError,f.__getitem__,(slice(-1,2,1),0))
        self.assertRaises(ValueError,f.__getitem__,(0,slice(-1,2,1)))
        self.assertRaises(ValueError,f.__getitem__,(slice(0,5,1),0))
        self.assertRaises(ValueError,f.__getitem__,(0,slice(0,4,1)))
        self.assertRaises(TypeError,f.__getitem__,(0,slice(0,4,1.1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0.1,4,1),2))

    def test_cvxpy_array_arith(self):
        
        # cvxpy_array with scalar
        x = variable(4,3)
        s1 = x + 1
        self.assertEqual(s1.type,c.defs.ARRAY)
        self.assertEqual(s1.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertNotEqual(x[i,j],s1[i,j])
                self.assertEqual(s1[i,j].type,c.defs.TREE)
                self.assertEqual(s1[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s1[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s1[i,j].children[0],x[i,j])
                self.assertEqual(s1[i,j].children[1].type,c.defs.CONSTANT)
                self.assertEqual(s1[i,j].children[1].value,1)
        s2 = 1 + x
        self.assertEqual(s2.type,c.defs.ARRAY)
        self.assertEqual(s2.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s2[i,j].type,c.defs.TREE)
                self.assertEqual(s2[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s2[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s2[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(s2[i,j].children[0].value,1)
                self.assertEqual(s2[i,j].children[1],x[i,j])
        s3 = x - 1
        self.assertEqual(s3.type,c.defs.ARRAY)
        self.assertEqual(s3.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s3[i,j].type,c.defs.TREE)
                self.assertEqual(s3[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s3[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s3[i,j].children[1].value,-1)
                self.assertEqual(s3[i,j].children[1].type,c.defs.CONSTANT)
                self.assertEqual(s3[i,j].children[0],x[i,j])
        s4 = 1 - x
        self.assertEqual(s4.type,c.defs.ARRAY)
        self.assertEqual(s4.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s4[i,j].type,c.defs.TREE)
                self.assertEqual(s4[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s4[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s4[i,j].children[0].value,1)
                self.assertEqual(s4[i,j].children[1].type,c.defs.TREE)
                self.assertEqual(s4[i,j].children[1].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(s4[i,j].children[1].item.name,
                                 c.defs.MULTIPLICATION)
                self.assertEqual(s4[i,j].children[1].children[0].value,-1)
                self.assertEqual(s4[i,j].children[1].children[1],x[i,j])
        
        # cvxpy_array with cvxpy_matrix
        B = ones((3,4))
        self.assertRaises(ValueError,x.__add__,B)
        self.assertRaises(ValueError,x.__sub__,B)
        self.assertRaises(ValueError,x.__radd__,B)
        self.assertRaises(ValueError,x.__rsub__,B)
        A = matrix([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
        s5 = x + A
        self.assertEqual(s5.type,c.defs.ARRAY)
        self.assertEqual(s5.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertNotEqual(x[i,j],s5[i,j])
                self.assertEqual(s5[i,j].type,c.defs.TREE)
                self.assertEqual(s5[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s5[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s5[i,j].children[0],x[i,j])
                self.assertEqual(s5[i,j].children[1].value,A[i,j])
                self.assertEqual(s5[i,j].children[1].type,c.defs.CONSTANT)
        s6 = A + x
        self.assertEqual(s6.type,c.defs.ARRAY)
        self.assertEqual(s6.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s6[i,j].type,c.defs.TREE)
                self.assertEqual(s6[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s6[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s6[i,j].children[0].value,A[i,j])
                self.assertEqual(s6[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(s6[i,j].children[1],x[i,j])
        s7 = x - A
        self.assertEqual(s7.type,c.defs.ARRAY)
        self.assertEqual(s7.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s7[i,j].type,c.defs.TREE)
                self.assertEqual(s7[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s7[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s7[i,j].children[1].value,-A[i,j])
                self.assertEqual(s7[i,j].children[1].type,c.defs.CONSTANT)
                self.assertEqual(s7[i,j].children[0],x[i,j])
        s8 = A - x
        self.assertEqual(s8.type,c.defs.ARRAY)
        self.assertEqual(s8.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s8[i,j].type,c.defs.TREE)
                self.assertEqual(s8[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s8[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s8[i,j].children[0].value,A[i,j])
                self.assertEqual(s8[i,j].children[1].type,c.defs.TREE)
                self.assertEqual(s8[i,j].children[1].item.type,
                                 c.defs.OPERATOR)
                self.assertEqual(s8[i,j].children[1].item.name,
                                 c.defs.MULTIPLICATION)
                self.assertEqual(s8[i,j].children[1].children[0].value,-1)
                self.assertEqual(s8[i,j].children[1].children[1],x[i,j])

        # cvxpy_array with cvxpy_array
        z = parameter(3,4)
        self.assertRaises(ValueError,x.__add__,z)
        self.assertRaises(ValueError,x.__sub__,z)
        self.assertRaises(ValueError,x.__radd__,z)
        self.assertRaises(ValueError,x.__rsub__,z)
        y = parameter(4,3)
        s9 = x + y
        self.assertEqual(s9.type,c.defs.ARRAY)
        self.assertEqual(s9.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertNotEqual(x[i,j],s9[i,j])
                self.assertEqual(s9[i,j].type,c.defs.TREE)
                self.assertEqual(s9[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s9[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s9[i,j].children[0],x[i,j])
                self.assertEqual(s9[i,j].children[1],y[i,j])
        s10 = y + x
        self.assertEqual(s10.type,c.defs.ARRAY)
        self.assertEqual(s10.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s10[i,j].type,c.defs.TREE)
                self.assertEqual(s10[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s10[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s10[i,j].children[0],y[i,j])
                self.assertEqual(s10[i,j].children[1],x[i,j])
        s11 = x - y
        self.assertEqual(s11.type,c.defs.ARRAY)
        self.assertEqual(s11.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s11[i,j].type,c.defs.TREE)
                self.assertEqual(s11[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s11[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s11[i,j].children[1].item.type,c.defs.OPERATOR)
                self.assertEqual(s11[i,j].children[1].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(s11[i,j].children[1].children[0].value,-1)
                self.assertEqual(s11[i,j].children[1].children[1],y[i,j])
                self.assertEqual(s11[i,j].children[0],x[i,j])
        s12 = y - x
        self.assertEqual(s12.type,c.defs.ARRAY)
        self.assertEqual(s12.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(s12[i,j].type,c.defs.TREE)
                self.assertEqual(s12[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s12[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s12[i,j].children[0],y[i,j])
                self.assertEqual(s12[i,j].children[1].type,c.defs.TREE)
                self.assertEqual(s12[i,j].children[1].item.type,c.defs.OPERATOR)
                self.assertEqual(s12[i,j].children[1].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(s12[i,j].children[1].children[0].value,-1)
                self.assertEqual(s12[i,j].children[1].children[1],x[i,j])

        # cvxpy_array with cvxpy_spmatrix
        x = parameter(10,20)
        A = spmatrix(sp.rand(10,20,density=0.5))
        self.assertRaises(ValueError,x.__add__,A.T)
        self.assertRaises(ValueError,x.__sub__,A.T)
        self.assertRaises(ValueError,x.__radd__,A.T)
        self.assertRaises(ValueError,x.__rsub__,A.T)
        s13 = x + A
        s14 = A + x
        s15 = x - A
        s16 = A - x
        self.assertTrue(type(s13) is c.arrays.cvxpy_array)
        self.assertTrue(type(s14) is c.arrays.cvxpy_array)
        self.assertTrue(type(s15) is c.arrays.cvxpy_array)
        self.assertTrue(type(s16) is c.arrays.cvxpy_array)
        self.assertEqual(s13.type,c.defs.ARRAY)
        self.assertEqual(s13.shape,x.shape)
        self.assertEqual(s14.type,c.defs.ARRAY)
        self.assertEqual(s14.shape,x.shape)
        self.assertEqual(s15.type,c.defs.ARRAY)
        self.assertEqual(s15.shape,x.shape)
        self.assertEqual(s16.type,c.defs.ARRAY)
        self.assertEqual(s16.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                if A[i,j] == 0.:
                    self.assertEqual(s13[i,j].type,c.defs.PARAMETER)
                else:
                    self.assertEqual(s13[i,j].type,c.defs.TREE)
                    self.assertEqual(s13[i,j].item.type,c.defs.OPERATOR)
                    self.assertEqual(s13[i,j].item.name,c.defs.SUMMATION)
                    self.assertEqual(s13[i,j].children[0],x[i,j])
                    self.assertEqual(s13[i,j].children[1].value,A[i,j])        
                    self.assertEqual(s14[i,j].children[0].value,A[i,j])
                    self.assertEqual(s14[i,j].children[1],x[i,j])        
                    self.assertEqual(s15[i,j].children[1].value,-A[i,j])
                    self.assertEqual(s16[i,j].children[0].value,A[i,j])        
                    self.assertEqual(s16[i,j].children[1].type,c.defs.TREE)
                    self.assertEqual(s16[i,j].children[1].item.type,c.defs.OPERATOR)
                    self.assertEqual(s16[i,j].children[1].children[0].value,-1)
                    self.assertEqual(s16[i,j].children[1].children[1],x[i,j])

        # cvxpy_array with cvxpy_sparray
        x = variable(10,20)
        Anum = sp.rand(10,20,density=0.5).tolil()
        A = c.arrays.cvxpy_sparray(10,20)
        for i in range(0,Anum.shape[0]):
            for j in Anum.rows[i]:
                A[i,j] = variable()
        self.assertEqual(A.nnz,Anum.nnz)
        self.assertRaises(ValueError,x.__add__,A.T)
        self.assertRaises(ValueError,x.__sub__,A.T)
        self.assertRaises(ValueError,x.__radd__,A.T)
        self.assertRaises(ValueError,x.__rsub__,A.T)
        s17 = x + A
        s18 = A + x
        s19 = x - A
        s20 = A - x
        self.assertTrue(type(s17) is c.arrays.cvxpy_array)
        self.assertTrue(type(s18) is c.arrays.cvxpy_array)
        self.assertTrue(type(s19) is c.arrays.cvxpy_array)
        self.assertTrue(type(s20) is c.arrays.cvxpy_array)
        self.assertEqual(s17.type,c.defs.ARRAY)
        self.assertEqual(s17.shape,x.shape)
        self.assertEqual(s18.type,c.defs.ARRAY)
        self.assertEqual(s18.shape,x.shape)
        self.assertEqual(s19.type,c.defs.ARRAY)
        self.assertEqual(s19.shape,x.shape)
        self.assertEqual(s20.type,c.defs.ARRAY)
        self.assertEqual(s20.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                if A[i,j] == 0.:
                    self.assertEqual(s17[i,j].type,c.defs.VARIABLE)
                else:
                    self.assertEqual(s17[i,j].type,c.defs.TREE)
                    self.assertEqual(s17[i,j].item.type,c.defs.OPERATOR)
                    self.assertEqual(s17[i,j].item.name,c.defs.SUMMATION)
                    self.assertEqual(s17[i,j].children[0],x[i,j])
                    self.assertEqual(s17[i,j].children[1],A[i,j])        
                    self.assertEqual(s18[i,j].children[0],A[i,j])
                    self.assertEqual(s18[i,j].children[1],x[i,j])        
                    self.assertEqual(s19[i,j].children[0],x[i,j])
                    self.assertEqual(s19[i,j].children[1].type,c.defs.TREE)
                    self.assertEqual(s19[i,j].children[1].item.type,c.defs.OPERATOR)
                    self.assertEqual(s19[i,j].children[1].children[0].value,-1)
                    self.assertEqual(s19[i,j].children[1].children[1],A[i,j])
                    self.assertEqual(s20[i,j].children[0],A[i,j])        
                    self.assertEqual(s20[i,j].children[1].type,c.defs.TREE)
                    self.assertEqual(s20[i,j].children[1].item.type,c.defs.OPERATOR)
                    self.assertEqual(s20[i,j].children[1].children[0].value,-1)
                    self.assertEqual(s20[i,j].children[1].children[1],x[i,j])

    def test_cvxpy_array_mul(self):
        
        # cvxpy_array and scalar
        a = parameter(4,3)
        m1 = a*4
        self.assertEqual(m1.shape,a.shape)
        self.assertEqual(m1.type,c.defs.ARRAY)
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(m1[i,j].type,c.defs.TREE)
                self.assertEqual(m1[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m1[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(m1[i,j].children[0].value,4)
                self.assertEqual(m1[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(m1[i,j].children[1],a[i,j])
        m2 = 4*a
        self.assertEqual(m2.shape,a.shape)
        self.assertEqual(m2.type,c.defs.ARRAY)
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(m2[i,j].type,c.defs.TREE)
                self.assertEqual(m2[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m2[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(m2[i,j].children[1],a[i,j])
                self.assertEqual(m2[i,j].children[0].value,4)
                self.assertEqual(m2[i,j].children[0].type,c.defs.CONSTANT)
        x = c.scalars.cvxpy_scalar_var()
        m3 = x*a
        self.assertEqual(m3.shape,a.shape)
        self.assertEqual(m3.type,c.defs.ARRAY)
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(m3[i,j].type,c.defs.TREE)
                self.assertEqual(m3[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m3[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(m3[i,j].children[1],x)
                self.assertEqual(m3[i,j].children[0],a[i,j])
        m4 = a*x
        self.assertEqual(m4.shape,a.shape)
        self.assertEqual(m4.type,c.defs.ARRAY)
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(m4[i,j].type,c.defs.TREE)
                self.assertEqual(m4[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m4[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(m4[i,j].children[1],x)
                self.assertEqual(m4[i,j].children[0],a[i,j])
        
        # cvxpy_array and cvxpy_matrix
        A = matrix([[2,3,4],[5,6,7]])
        x = variable(3,2)
        m5 = A*x
        self.assertEqual(m5.type,c.defs.ARRAY)
        self.assertEqual(m5.shape,(2,2))
        for i in range(0,m5.shape[0],1):
            for j in range(0,m5.shape[1],1):
                self.assertEqual(m5[i,j].type,c.defs.TREE)
                self.assertEqual(m5[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m5[i,j].item.name,c.defs.SUMMATION)
                children = m5[i,j].children
                for k in range(0,len(children),1):
                    self.assertEqual(children[k].type,c.defs.TREE)
                    self.assertEqual(children[k].item.type,c.defs.OPERATOR)
                    self.assertEqual(children[k].item.name,
                                     c.defs.MULTIPLICATION)
                    self.assertEqual(children[k].children[0].value,A[i,k])
                    self.assertEqual(children[k].children[0].type,
                                     c.defs.CONSTANT)
                    self.assertEqual(children[k].children[1],x[k,j])
        B = ones((3,3))
        self.assertRaises(ValueError,x.__mul__,B) #x*B
        self.assertRaises(ValueError,x.T.__rmul__,B) #B*x.T
        m6 = x*A
        self.assertEqual(m6.type,c.defs.ARRAY)
        self.assertEqual(m6.shape,(3,3))
        for i in range(0,m6.shape[0],1):
            for j in range(0,m6.shape[1],1):
                self.assertEqual(m6[i,j].type,c.defs.TREE)
                self.assertEqual(m6[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m6[i,j].item.name,c.defs.SUMMATION)
                children = m6[i,j].children
                for k in range(0,len(children),1):
                    self.assertEqual(children[k].type,c.defs.TREE)
                    self.assertEqual(children[k].item.type,c.defs.OPERATOR)
                    self.assertEqual(children[k].item.name,
                                     c.defs.MULTIPLICATION)
                    self.assertEqual(children[k].children[0].value,A[k,j])
                    self.assertEqual(children[k].children[0].type,
                                     c.defs.CONSTANT)
                    self.assertEqual(children[k].children[1],x[i,k])
        A = matrix([2,3,4])
        a = parameter(3,1)
        m7 = A*a
        self.assertEqual(m7.type,c.defs.TREE)
        self.assertEqual(m7.item.type,c.defs.OPERATOR)
        self.assertEqual(m7.item.name,c.defs.SUMMATION)
        for k in range(0,len(m7.children),1):
            self.assertEqual(m7.children[k].type,c.defs.TREE)
            self.assertEqual(m7.children[k].item.type,c.defs.OPERATOR)
            self.assertEqual(m7.children[k].item.name,
                             c.defs.MULTIPLICATION)
            self.assertEqual(m7.children[k].children[0].value,A[0,k])
            self.assertEqual(m7.children[k].children[0].type,
                             c.defs.CONSTANT)
            self.assertEqual(m7.children[k].children[1],a[k,0])
        m8 = a.T*A.T
        self.assertEqual(m8.type,c.defs.TREE)
        self.assertEqual(m8.item.type,c.defs.OPERATOR)
        self.assertEqual(m8.item.name,c.defs.SUMMATION)
        for k in range(0,len(m8.children),1):
            self.assertEqual(m8.children[k].type,c.defs.TREE)
            self.assertEqual(m8.children[k].item.type,c.defs.OPERATOR)
            self.assertEqual(m8.children[k].item.name,
                             c.defs.MULTIPLICATION)
            self.assertEqual(m8.children[k].children[0].value,A.T[k,0])
            self.assertEqual(m8.children[k].children[0].type,
                             c.defs.CONSTANT)
            self.assertEqual(m8.children[k].children[1],a.T[0,k])
        
        # cvxpy_array and cvxpy_array
        a = parameter(2,3)
        x = variable(3,2)
        m9 = a*x
        self.assertEqual(m9.type,c.defs.ARRAY)
        self.assertEqual(m9.shape,(2,2))
        for i in range(0,m9.shape[0],1):
            for j in range(0,m9.shape[1],1):
                self.assertEqual(m9[i,j].type,c.defs.TREE)
                self.assertEqual(m9[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m9[i,j].item.name,c.defs.SUMMATION)
                children = m9[i,j].children
                for k in range(0,len(children),1):
                    self.assertEqual(children[k].type,c.defs.TREE)
                    self.assertEqual(children[k].item.type,c.defs.OPERATOR)
                    self.assertEqual(children[k].item.name,
                                     c.defs.MULTIPLICATION)
                    self.assertEqual(children[k].children[0],a[i,k])
                    self.assertEqual(children[k].children[1],x[k,j])
        b = parameter(3,3)
        self.assertRaises(ValueError,x.__mul__,b) #x*b
        self.assertRaises(ValueError,x.T.__rmul__,b) #b*x.T
        m10 = x*a
        self.assertEqual(m10.type,c.defs.ARRAY)
        self.assertEqual(m10.shape,(3,3))
        for i in range(0,m10.shape[0],1):
            for j in range(0,m10.shape[1],1):
                self.assertEqual(m10[i,j].type,c.defs.TREE)
                self.assertEqual(m10[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(m10[i,j].item.name,c.defs.SUMMATION)
                children = m10[i,j].children
                for k in range(0,len(children),1):
                    self.assertEqual(children[k].type,c.defs.TREE)
                    self.assertEqual(children[k].item.type,c.defs.OPERATOR)
                    self.assertEqual(children[k].item.name,
                                     c.defs.MULTIPLICATION)
                    self.assertEqual(children[k].children[1],x[i,k])
                    self.assertEqual(children[k].children[0],a[k,j])
        a = parameter(1,3)
        x = variable(3,1)
        m11 = a*x
        self.assertEqual(m11.type,c.defs.TREE)
        self.assertEqual(m11.item.type,c.defs.OPERATOR)
        self.assertEqual(m11.item.name,c.defs.SUMMATION)
        for k in range(0,len(m11.children),1):
            self.assertEqual(m11.children[k].type,c.defs.TREE)
            self.assertEqual(m11.children[k].item.type,c.defs.OPERATOR)
            self.assertEqual(m11.children[k].item.name,
                             c.defs.MULTIPLICATION)
            self.assertEqual(m11.children[k].children[0],a[0,k])
            self.assertEqual(m11.children[k].children[1],x[k,0])
        m12 = x.T*a.T
        self.assertEqual(m12.type,c.defs.TREE)
        self.assertEqual(m12.item.type,c.defs.OPERATOR)
        self.assertEqual(m12.item.name,c.defs.SUMMATION)
        for k in range(0,len(m12.children),1):
            self.assertEqual(m12.children[k].type,c.defs.TREE)
            self.assertEqual(m12.children[k].item.type,c.defs.OPERATOR)
            self.assertEqual(m12.children[k].item.name,
                             c.defs.MULTIPLICATION)
            self.assertEqual(m12.children[k].children[1],x.T[0,k])
            self.assertEqual(m12.children[k].children[0],a.T[k,0])

        # cvxpy_array and cvxpy_spmatrix
        x = variable(30,20)
        As = spmatrix(sp.rand(20,40,density=0.3))
        for k in range(0,20):
            As[k,4] = 0.
        As[5,4] = 10.
        t1 = x*As
        self.assertTrue(type(t1) is c.arrays.cvxpy_array)
        self.assertEqual(t1.shape,(30,40))
        self.assertEqual(t1.type,c.defs.ARRAY)
        for i in range(0,30):
            for j in range(0,40):
                e = t1[i,j]
                num = 0
                for k in range(0,20):
                    if As[k,j] != 0.:
                        num += 1
                if num == 0:
                    self.assertEqual(e,0.)
                elif num == 1:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.MULTIPLICATION)
                    for k in range(0,20):
                        if As[k,j] != 0.:
                            self.assertTrue(e.children[1] is x[i,k])
                            self.assertEqual(e.children[0].type,c.defs.CONSTANT)
                            self.assertEqual(e.children[0].value,As[k,j])
                else:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.SUMMATION)
                    kk = 0
                    for k in range(0,20):
                        if As[k,j] == 0.:
                            continue
                        else:
                            self.assertTrue(type(e.children[kk]) is c.scalars.cvxpy_tree)
                            self.assertEqual(e.children[kk].item.type,c.defs.OPERATOR)
                            self.assertEqual(e.children[kk].item.name,c.defs.MULTIPLICATION)
                            self.assertEqual(e.children[kk].children[0].type,c.defs.CONSTANT)
                            self.assertTrue(e.children[kk].children[1] is x[i,k])
                            self.assertEqual(e.children[kk].children[0].value,As[k,j])
                            kk += 1
        y = variable(10,1)
        Bs = spmatrix(sp.rand(10,1,density=0.5))
        t2 = y.T*Bs
        self.assertTrue(type(t2) is c.scalars.cvxpy_tree)
        self.assertEqual(t2.item.type,c.defs.OPERATOR)
        self.assertEqual(t2.item.name,c.defs.SUMMATION)
        kk = 0
        for k in range(0,10):
            if Bs[k,0] == 0.:
                continue
            else:
                self.assertTrue(type(t2.children[kk]) is c.scalars.cvxpy_tree)
                self.assertTrue(t2.children[kk].children[1] is y[k,0])
                self.assertEqual(t2.children[kk].children[0].type,c.defs.CONSTANT)
                self.assertEqual(t2.children[kk].children[0].value,Bs[k,0])
                kk += 1
        Cs = spmatrix(sp.rand(30,20,density=0.3))
        z = variable(20,40)
        for k in range(0,20):
            Cs[4,k] = 0.
        Cs[4,5] = 10.
        t3 = Cs*z
        self.assertTrue(type(t3) is c.arrays.cvxpy_array)
        self.assertEqual(t3.shape,(30,40))
        self.assertEqual(t3.type,c.defs.ARRAY)
        for i in range(0,30):
            for j in range(0,40):
                e = t3[i,j]
                num = 0
                for k in range(0,20):
                    if Cs[i,k] != 0.:
                        num += 1
                if num == 0:
                    self.assertEqual(e,0.)
                elif num == 1:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.MULTIPLICATION)
                    for k in range(0,20):
                        if Cs[i,k] != 0.:
                            self.assertTrue(e.children[1] is z[k,j])
                            self.assertEqual(e.children[0].type,c.defs.CONSTANT)
                            self.assertEqual(e.children[0].value,Cs[i,k])
                else:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.SUMMATION)
                    kk = 0
                    for k in range(0,20):
                        if Cs[i,k] == 0.:
                            continue
                        else:
                            self.assertTrue(type(e.children[kk]) is c.scalars.cvxpy_tree)
                            self.assertEqual(e.children[kk].item.type,c.defs.OPERATOR)
                            self.assertEqual(e.children[kk].item.name,c.defs.MULTIPLICATION)
                            self.assertEqual(e.children[kk].children[0].type,c.defs.CONSTANT)
                            self.assertTrue(e.children[kk].children[1] is z[k,j])
                            self.assertEqual(e.children[kk].children[0].value,Cs[i,k])
                            kk += 1
        w = variable(10,1)
        Ds = spmatrix(sp.rand(10,1,density=0.5))
        t4 = Ds.T*w
        self.assertTrue(type(t4) is c.scalars.cvxpy_tree)
        self.assertEqual(t4.item.type,c.defs.OPERATOR)
        self.assertEqual(t4.item.name,c.defs.SUMMATION)
        kk = 0
        for k in range(0,10):
            if Ds[k,0] == 0.:
                continue
            else:
                self.assertTrue(type(t4.children[kk]) is c.scalars.cvxpy_tree)
                self.assertTrue(t4.children[kk].children[1] is w[k,0])
                self.assertEqual(t4.children[kk].children[0].type,c.defs.CONSTANT)
                self.assertEqual(t4.children[kk].children[0].value,Ds[k,0])
                kk += 1

        # cvxpy_array and cvxpy_sparray
        a1 = parameter(40,20)
        A1m = spmatrix(sp.rand(20,50,density=0.3))
        for k in range(0,20):
            A1m[k,4] = 0.
        A1m[5,4] = 10.
        A1 = c.arrays.cvxpy_sparray(20,50)
        for i in range(0,20):
            for j in A1m.rows[i]:
                A1[i,j] = variable()
        self.assertEqual(A1.nnz,A1m.nnz)
        t5 = a1*A1
        self.assertTrue(type(t5) is c.arrays.cvxpy_array)
        self.assertEqual(t5.shape,(40,50))
        self.assertEqual(t5.type,c.defs.ARRAY)
        for i in range(0,40):
            for j in range(0,50):
                e = t5[i,j]
                num = 0
                for k in range(0,20):
                    if A1[k,j] != 0.:
                        num += 1
                if num == 0:
                    self.assertEqual(e,0.)
                elif num == 1:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.MULTIPLICATION)
                    for k in range(0,20):
                        if A1[k,j] != 0.:
                            self.assertTrue(e.children[0] is a1[i,k])
                            self.assertTrue(e.children[1] is A1[k,j])
                else:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.SUMMATION)
                    kk = 0
                    for k in range(0,20):
                        if A1[k,j] == 0.:
                            continue
                        else:
                            self.assertTrue(type(e.children[kk]) is c.scalars.cvxpy_tree)
                            self.assertEqual(e.children[kk].item.type,c.defs.OPERATOR)
                            self.assertEqual(e.children[kk].item.name,c.defs.MULTIPLICATION)
                            self.assertTrue(e.children[kk].children[0] is a1[i,k])
                            self.assertTrue(e.children[kk].children[1] is A1[k,j])
                            kk += 1
        a2 = variable(10,1)
        A2m = spmatrix(sp.rand(10,1,density=0.5))
        A2 = c.arrays.cvxpy_sparray(10,1)
        for i in range(0,10):
            for j in A2m.rows[i]:
                A2[i,j] = parameter()
        t6 = a2.T*A2
        self.assertTrue(type(t6) is c.scalars.cvxpy_tree)
        self.assertEqual(t6.item.type,c.defs.OPERATOR)
        self.assertEqual(t6.item.name,c.defs.SUMMATION)
        kk = 0
        for k in range(0,10):
            if A2[k,0] == 0.:
                continue
            else:
                self.assertTrue(type(t6.children[kk]) is c.scalars.cvxpy_tree)
                self.assertTrue(t6.children[kk].children[1] is a2[k,0])
                self.assertTrue(t6.children[kk].children[0] is A2[k,0])
                kk += 1
        A3m = spmatrix(sp.rand(30,20,density=0.3))
        a3 = variable(20,40)
        for k in range(0,20):
            A3m[4,k] = 0.
        A3m[4,5] = 10.
        A3 = c.arrays.cvxpy_sparray(30,20)
        for i in range(0,30):
            for j in A3m.rows[i]:
                A3[i,j] = parameter()
        t7 = A3*a3
        self.assertTrue(type(t7) is c.arrays.cvxpy_array)
        self.assertEqual(t7.shape,(30,40))
        self.assertEqual(t7.type,c.defs.ARRAY)
        for i in range(0,30):
            for j in range(0,40):
                e = t7[i,j]
                num = 0
                for k in range(0,20):
                    if A3[i,k] != 0.:
                        num += 1
                if num == 0:
                    self.assertEqual(e,0.)
                elif num == 1:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.MULTIPLICATION)
                    for k in range(0,20):
                        if A3[i,k] != 0.:
                            self.assertTrue(e.children[1] is a3[k,j])
                            self.assertTrue(e.children[0] is A3[i,k])
                else:
                    self.assertTrue(type(e) is c.scalars.cvxpy_tree)
                    self.assertEqual(e.item.type,c.defs.OPERATOR)
                    self.assertEqual(e.item.name,c.defs.SUMMATION)
                    kk = 0
                    for k in range(0,20):
                        if A3[i,k] == 0.:
                            continue
                        else:
                            self.assertTrue(type(e.children[kk]) is c.scalars.cvxpy_tree)
                            self.assertEqual(e.children[kk].item.type,c.defs.OPERATOR)
                            self.assertEqual(e.children[kk].item.name,c.defs.MULTIPLICATION)
                            self.assertTrue(e.children[kk].children[1] is a3[k,j])
                            self.assertTrue(e.children[kk].children[0] is A3[i,k])
                            kk += 1
        a4 = parameter(10,1)
        A4m = spmatrix(sp.rand(10,1,density=0.5))
        A4 = c.arrays.cvxpy_sparray(10,1)
        for i in range(0,10):
            for j in A4m.rows[i]:
                A4[i,j] = variable()
        t8 = A4.T*a4
        self.assertTrue(type(t8) is c.scalars.cvxpy_tree)
        self.assertEqual(t8.item.type,c.defs.OPERATOR)
        self.assertEqual(t8.item.name,c.defs.SUMMATION)
        kk = 0
        for k in range(0,10):
            if A4[k,0] == 0.:
                continue
            else:
                self.assertTrue(type(t8.children[kk]) is c.scalars.cvxpy_tree)
                self.assertTrue(t8.children[kk].children[0] is a4[k,0])
                self.assertTrue(t8.children[kk].children[1] is A4[k,0])
                kk += 1
        print 'VAMOS'

    def test_cvxpy_array_neg(self):
        x = variable(3,4)
        n1 = -x
        self.assertEqual(n1.type,c.defs.ARRAY)
        self.assertEqual(n1.shape,x.shape)
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(n1[i,j].type,c.defs.TREE)
                self.assertEqual(n1[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(n1[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(n1[i,j].children[0].value,-1)
                self.assertEqual(n1[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(n1[i,j].children[0].name,'-1.0')
                self.assertEqual(n1[i,j].children[1],x[i,j])

    def test_cvxpy_array_is_affine(self):
        x = variable(3,3)
        self.assertTrue(x.is_affine())
        a = parameter(3,3)
        self.assertTrue(a.is_affine())
        self.assertTrue((x+1).is_affine())
        y = variable(3,3)
        self.assertTrue((4*x+y).is_affine())
        A = matrix([[1,2,3],[3,4,5]])
        self.assertTrue((A*x).is_affine())
        x = variable()
        y = variable()
        f = vstack((1,2,x,y,x,2*x,3*y+x+2))
        self.assertTrue(f.is_affine())
        f = vstack((1,2,x,y,abs(x),2*x,3*y+x+2))
        self.assertFalse(f.is_affine())

    # cvxpy_var
    def test_cvxpy_var_init(self):
        x = c.arrays.cvxpy_var(5,3,name='x')
        self.assertEqual(x.shape,(5,3))
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertEqual(x[i,j].type,c.defs.VARIABLE)
                self.assertEqual(x[i,j].name,'x['+str(i)+','+str(j)+']')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,5,3,'lower triangular','x')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,5,3,'lower_triangular','x')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,5,3,'upper triangular','x')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,5,3,'upper_triangular','x')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,5,3,'badness','x')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,5,5,['something'],'x')
        self.assertRaises(ValueError,c.arrays.cvxpy_var,4,2,'symmetric','z')
        x = c.arrays.cvxpy_var(3,3,'lower_triangular','x')
        y = c.arrays.cvxpy_var(3,3,'upper_triangular','y')
        z = c.arrays.cvxpy_var(3,3,'symmetric','z')
        for i in range(0,x.shape[0],1):
            for j in range(0,i,1):
                self.assertEqual(x[i,j].type,c.defs.VARIABLE)
                self.assertEqual(x[i,j].name,'x['+str(i)+','+str(j)+']')
                self.assertEqual(y[i,j],0.0)
                self.assertEqual(z[i,j],z[j,i])
                self.assertEqual(z[i,j].type,c.defs.VARIABLE)
                self.assertEqual(z[i,j].name,'z['+str(i)+','+str(j)+']')
        for i in range(0,x.shape[0],1):
            self.assertEqual(x[i,i].type,c.defs.VARIABLE)
            self.assertEqual(x[i,i].name,'x['+str(i)+','+str(i)+']')
            self.assertEqual(y[i,i].type,c.defs.VARIABLE)
            self.assertEqual(y[i,i].name,'y['+str(i)+','+str(i)+']')
            self.assertEqual(z[i,i].type,c.defs.VARIABLE)
            self.assertEqual(z[i,i].name,'z['+str(i)+','+str(i)+']')
        for i in range(0,x.shape[0],1):
            for j in range(i+1,x.shape[1],1):
                self.assertEqual(y[i,j].type,c.defs.VARIABLE)
                self.assertEqual(y[i,j].name,'y['+str(i)+','+str(j)+']')
                self.assertEqual(x[i,j],0.0)
        
    # cvxpy_param
    def test_cvxpy_param_init(self):
        a = c.arrays.cvxpy_param(5,3,name='a')
        self.assertEqual(a.shape,(5,3))
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(a[i,j].type,c.defs.PARAMETER)
                self.assertEqual(a[i,j].name,'a['+str(i)+','+str(j)+']')
                self.assertEqual(a[i,j].attribute,None)
        a = c.arrays.cvxpy_param(2,10,'nonnegative','a')
        self.assertEqual(a.shape,(2,10))
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(a[i,j].type,c.defs.PARAMETER)
                self.assertEqual(a[i,j].name,'a['+str(i)+','+str(j)+']')
                self.assertEqual(a[i,j].attribute,c.defs.NONNEGATIVE)
        self.assertRaises(ValueError,c.arrays.cvxpy_param,3,4,'badness','a')
        self.assertRaises(ValueError,c.arrays.cvxpy_param,3,4,10,'a')
       
    def test_cvxpy_param_setattr(self):
        a = c.arrays.cvxpy_param(4,3)
        self.assertRaises(TypeError,a.__setattr__,'value',np.ones((4,3)))
        self.assertRaises(ValueError,a.__setattr__,'value',ones((4,4)))
        a = c.arrays.cvxpy_param(2,3)
        A = matrix([[1,2,3],[4,5,6]])
        a.value = A
        self.assertTrue(type(a.value) is c.arrays.cvxpy_matrix)
        self.assertTrue(np.allclose(A,a.value))
        
    # cvxpy_matrix
    def test_cvxpy_matrix_init(self):
        B = np.matrix([[1,2,3],[4,5,6]])
        A = c.arrays.cvxpy_matrix([[1,2,3],[4,5,6]],np.float64)
        self.assertEqual(A.dtype,np.float64)
        for i in range(0,A.shape[0],1):
            for j in range(0,A.shape[1],1):
                self.assertEqual(A[i,j],B[i,j])
        self.assertTrue(type(A.T) is c.arrays.cvxpy_matrix)
        self.assertTrue(type(A) is c.arrays.cvxpy_matrix)
        self.assertTrue(type(A[0:1,:]) is c.arrays.cvxpy_matrix)

    def test_cvxpy_matrix_getattribute(self):
        C = c.arrays.cvxpy_matrix([[2.0,0,0],[0,2.0,0],[0,0,2.0]],np.float64)
        D = np.matrix([[0.5,0,0],[0,0.5,0],[0,0,.5]])
        self.assertTrue(np.allclose(C.I,D))
        self.assertTrue(type(C.I) is c.arrays.cvxpy_matrix)
        C = c.arrays.cvxpy_matrix([[3,0],[0,3]],np.float64)
        D = np.matrix([[1./3.,0],[0,1./3.]])
        self.assertTrue(np.allclose(C.I,D))
        self.assertTrue(type(C.I) is c.arrays.cvxpy_matrix)
        self.assertEqual(C.I.dtype,np.float64)

    def test_cvxpy_matrix_add(self):
        A = c.arrays.cvxpy_matrix([[1.,2.],[3.,4.]],np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__add__(x),NotImplemented)
        self.assertEqual(A.__add__(a),NotImplemented)
        self.assertEqual(A.__add__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__add__(x),NotImplemented)
        self.assertEqual(A.__add__(a),NotImplemented)
        self.assertEqual(A.__add__(x+a),NotImplemented)

    def test_cvxpy_matrix_radd(self):
        A = c.arrays.cvxpy_matrix([[1.,2.],[3.,4.]],np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__radd__(x),NotImplemented)
        self.assertEqual(A.__radd__(a),NotImplemented)
        self.assertEqual(A.__radd__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__radd__(x),NotImplemented)
        self.assertEqual(A.__radd__(a),NotImplemented)
        self.assertEqual(A.__radd__(x+a),NotImplemented)

    def test_cvxpy_matrix_sub(self):
        A = c.arrays.cvxpy_matrix([[1.,2.],[3.,4.]],np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__sub__(x),NotImplemented)
        self.assertEqual(A.__sub__(a),NotImplemented)
        self.assertEqual(A.__sub__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__sub__(x),NotImplemented)
        self.assertEqual(A.__sub__(a),NotImplemented)
        self.assertEqual(A.__sub__(x+a),NotImplemented)

    def test_cvxpy_matrix_rsub(self):
        A = c.arrays.cvxpy_matrix([[1.,2.],[3.,4.]],np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__rsub__(x),NotImplemented)
        self.assertEqual(A.__rsub__(a),NotImplemented)
        self.assertEqual(A.__rsub__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__rsub__(x),NotImplemented)
        self.assertEqual(A.__rsub__(a),NotImplemented)
        self.assertEqual(A.__rsub__(x+a),NotImplemented)
    
    def test_cvxpy_matrix_mul(self):
        A = c.arrays.cvxpy_matrix([[1.,2.],[3.,4.]],np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__mul__(x),NotImplemented)
        self.assertEqual(A.__mul__(a),NotImplemented)
        self.assertEqual(A.__mul__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__mul__(x),NotImplemented)
        self.assertEqual(A.__mul__(a),NotImplemented)
        self.assertEqual(A.__mul__(x+a),NotImplemented)

    def test_cvxpy_matrix_rmul(self):
        A = c.arrays.cvxpy_matrix([[1.,2.],[3.,4.]],np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__rmul__(x),NotImplemented)
        self.assertEqual(A.__rmul__(a),NotImplemented)
        self.assertEqual(A.__rmul__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__rmul__(x),NotImplemented)
        self.assertEqual(A.__rmul__(a),NotImplemented)
        self.assertEqual(A.__rmul__(x+a),NotImplemented)

    # cvxpy_spmatrix
    def test_cvxpy_spmatrix_init(self):
        B1 = np.matrix([[1,2,3],[4,5,6]])
        B2 = sp.rand(10,20,format='lil')
        B3 = sp.rand(4,10,format='csr')
        A0 = c.arrays.cvxpy_spmatrix([[1,2,3],[4,5,6]],dtype=np.float64)
        self.assertEqual(A0.shape,(2,3))
        self.assertEqual(A0.dtype,np.float64)
        self.assertTrue(type(A0) is c.arrays.cvxpy_spmatrix)
        for i in range(0,2,1):
            for j in range(0,3,1):
                self.assertEqual(A0[i,j],B1[i,j])
        A1 = c.arrays.cvxpy_spmatrix(B1,dtype=np.float64)
        self.assertEqual(A1.shape,(2,3))
        self.assertEqual(A1.dtype,np.float64)
        self.assertTrue(type(A1) is c.arrays.cvxpy_spmatrix)
        for i in range(0,2,1):
            for j in range(0,3,1):
                self.assertEqual(A1[i,j],B1[i,j])
        A2 = c.arrays.cvxpy_spmatrix(B2,dtype=np.float32)
        self.assertEqual(A2.shape,(10,20))
        self.assertEqual(A2.dtype,np.float32)
        self.assertTrue(type(A2) is c.arrays.cvxpy_spmatrix)
        for i in range(0,10,1):
            for j in range(0,20,1):
                self.assertEqual(A2[i,j],np.float32(B2[i,j]))
        A3 = c.arrays.cvxpy_spmatrix(B3,dtype=np.float32)
        self.assertEqual(A3.shape,(4,10))
        self.assertEqual(A3.dtype,np.float32)
        self.assertTrue(type(A3) is c.arrays.cvxpy_spmatrix)
        C3 = B3.tolil()
        for i in range(0,4,1):
            for j in range(0,10,1):
                self.assertEqual(A3[i,j],np.float32(C3[i,j]))
        A4 = c.arrays.cvxpy_spmatrix(10,dtype=np.int32)
        self.assertEqual(A4.shape,(1,1))
        self.assertEqual(A4.dtype,np.int32)
        self.assertTrue(type(A4) is c.arrays.cvxpy_spmatrix) 
        A5 = c.arrays.cvxpy_spmatrix((10,20),dtype=np.int32)
        self.assertEqual(A5.shape,(10,20))

    def test_cvxpy_spmatrix_getattribute(self):
        A = np.matrix(np.random.randn(20,20))
        Asp = c.arrays.cvxpy_spmatrix(A,dtype=np.float64)
        self.assertEqual(Asp.shape,(20,20))
        self.assertEqual(Asp.dtype,np.float64)
        self.assertEqual(Asp.nnz,400)
        self.assertTrue(type(Asp[0:10,:]) is c.arrays.cvxpy_spmatrix)
        AspT = Asp.T
        for i in range(0,20):
            for j in range(0,20):
                self.assertEqual(Asp[i,j],AspT[j,i])
        B = sp.rand(20,20,format='coo',dtype=np.float64)
        B1 = c.arrays.cvxpy_spmatrix(B,dtype=np.float64)
        B = B.tolil()
        self.assertEqual(B1.shape,B.shape)
        self.assertEqual(B1.dtype,B.dtype)
        self.assertEqual(B1.nnz,B.nnz)
        for i in range(0,20):
            for j in range(0,20):
                self.assertEqual(B1[i,j],B[i,j])
        self.assertTrue(type(B1[:,0:10]) is c.arrays.cvxpy_spmatrix)
        C = c.arrays.cvxpy_spmatrix((10,10),dtype=np.float64)
        self.assertTrue(type(C) is c.arrays.cvxpy_spmatrix)
        self.assertTrue(type(C.T) is c.arrays.cvxpy_spmatrix)
        self.assertTrue(type(C[:,0:5]) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(C.shape,(10,10))
        self.assertEqual(C.dtype,np.float64)
        self.assertEqual(C.nnz,0)
        C[0,0] = 1.
        self.assertEqual(C.nnz,1)

    def test_cvxpy_spmatrix_add(self):
        A = c.arrays.cvxpy_spmatrix(sp.rand(2,2),dtype=np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__add__(x),NotImplemented)
        self.assertEqual(A.__add__(a),NotImplemented)
        self.assertEqual(A.__add__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__add__(x),NotImplemented)
        self.assertEqual(A.__add__(a),NotImplemented)
        self.assertEqual(A.__add__(x+a),NotImplemented)

    def test_cvxpy_spmatrix_radd(self):
        A = c.arrays.cvxpy_spmatrix(sp.rand(2,2),dtype=np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__radd__(x),NotImplemented)
        self.assertEqual(A.__radd__(a),NotImplemented)
        self.assertEqual(A.__radd__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__radd__(x),NotImplemented)
        self.assertEqual(A.__radd__(a),NotImplemented)
        self.assertEqual(A.__radd__(x+a),NotImplemented)

    def test_cvxpy_spmatrix_sub(self):
        A = c.arrays.cvxpy_spmatrix(sp.rand(2,2),dtype=np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__sub__(x),NotImplemented)
        self.assertEqual(A.__sub__(a),NotImplemented)
        self.assertEqual(A.__sub__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__sub__(x),NotImplemented)
        self.assertEqual(A.__sub__(a),NotImplemented)
        self.assertEqual(A.__sub__(x+a),NotImplemented)

    def test_cvxpy_spmatrix_rsub(self):
        A = c.arrays.cvxpy_spmatrix(sp.rand(2,2),dtype=np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__rsub__(x),NotImplemented)
        self.assertEqual(A.__rsub__(a),NotImplemented)
        self.assertEqual(A.__rsub__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__rsub__(x),NotImplemented)
        self.assertEqual(A.__rsub__(a),NotImplemented)
        self.assertEqual(A.__rsub__(x+a),NotImplemented)
    
    def test_cvxpy_spmatrix_mul(self):
        A = c.arrays.cvxpy_spmatrix(sp.rand(2,2),dtype=np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__mul__(x),NotImplemented)
        self.assertEqual(A.__mul__(a),NotImplemented)
        self.assertEqual(A.__mul__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__mul__(x),NotImplemented)
        self.assertEqual(A.__mul__(a),NotImplemented)
        self.assertEqual(A.__mul__(x+a),NotImplemented)

    def test_cvxpy_spmatrix_rmul(self):
        A = c.arrays.cvxpy_spmatrix(sp.rand(2,2),dtype=np.float64)
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(A.__rmul__(x),NotImplemented)
        self.assertEqual(A.__rmul__(a),NotImplemented)
        self.assertEqual(A.__rmul__(x+a),NotImplemented)
        x = c.arrays.cvxpy_var(2,2)
        a = c.arrays.cvxpy_param(2,2)
        self.assertEqual(A.__rmul__(x),NotImplemented)
        self.assertEqual(A.__rmul__(a),NotImplemented)
        self.assertEqual(A.__rmul__(x+a),NotImplemented)

    # cvxpy_sparray
    def test_cvxpy_sparray_init(self):
        f = c.arrays.cvxpy_sparray(40,30)
        self.assertEqual(f.shape,(40,30))
        self.assertEqual(f.type,c.defs.SPARRAY)
        for i in range(0,40):
            self.assertEqual(f.rows[i],[])
            self.assertEqual(f.data[i],[])
        self.assertEqual(f.nnz,0)

    def test_cvxpy_sparray_getattribute(self):
        f = c.arrays.cvxpy_sparray(40,30)
        A = sp.lil_matrix((40,30),dtype=np.float64)
        fT = f.T
        self.assertEqual(fT.shape,(30,40))
        self.assertEqual(fT.nnz,0)
        self.assertTrue(type(fT) is c.arrays.cvxpy_sparray)
        var_i = [1,4,19,29]
        var_j = [0,2,5,18]
        x = c.arrays.cvxpy_var(4,1)
        for k in range(0,4):
            x[k,0].value = np.random.rand()
            f[var_i[k],var_j[k]] = x[k,0]
            A[var_i[k],var_j[k]] = x[k,0].value
        self.assertEqual(f.nnz,4)
        fT = f.T
        self.assertEqual(fT.shape,(30,40))
        for k in range(0,4):
            self.assertTrue(fT[var_j[k],var_i[k]] is x[k,0])
        self.assertEqual(fT.nnz,4)
        B = f.value
        self.assertTrue(type(B) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(B.nnz,4)
        self.assertEqual(B.shape,(40,30))
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])
        a = c.arrays.cvxpy_param(4,1)
        a.value= c.matrix(np.random.rand(4,1))
        for k in range(0,4):
            f[var_j[k],var_i[k]] = a[k,0]
            A[var_j[k],var_i[k]] = a[k,0].value
        self.assertEqual(f.nnz,8)
        fT = f.T
        self.assertEqual(fT.shape,(30,40))
        for k in range(0,4):
            self.assertTrue(fT[var_j[k],var_i[k]] is x[k,0])
            self.assertTrue(fT[var_i[k],var_j[k]] is a[k,0])
        self.assertEqual(fT.nnz,8)
        self.assertEqual(len(f.variables),4)
        self.assertEqual(len(f.parameters),4)
        self.assertTrue(type(f.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(f.parameters) is c.constraints.cvxpy_list)
        for k in range(0,4):
            self.assertTrue(x[k,0] in f.variables)
            self.assertTrue(a[k,0] in f.parameters)
        B = f.value
        self.assertTrue(type(B) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(B.nnz,8)
        self.assertEqual(A.nnz,8)
        self.assertEqual(B.shape,(40,30))
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])
        x1 = c.scalars.cvxpy_scalar_var()
        x1.value = 100.
        f[0,0] = x1
        A[0,0] = x1.value
        self.assertEqual(len(f.variables),5)
        self.assertEqual(len(f.parameters),4)
        self.assertEqual(f.nnz,9)
        B = f.value
        self.assertEqual(B.nnz,9)
        self.assertEqual(A.nnz,9)
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])
        a1 = c.scalars.cvxpy_scalar_param()
        a1.value = 0.3
        f[3,3] = a1
        A[3,3] = a1.value
        self.assertEqual(len(f.variables),5)
        self.assertEqual(len(f.parameters),5)
        self.assertEqual(f.nnz,10)
        B = f.value
        self.assertEqual(B.nnz,10)
        self.assertEqual(A.nnz,10)
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])
        a2 = c.scalars.cvxpy_scalar_param()
        a2.value = 20.1
        f[19,5] = a2
        A[19,5] = a2.value
        self.assertEqual(len(f.variables),4)
        self.assertEqual(len(f.parameters),6)
        self.assertEqual(f.nnz,10)
        B = f.value
        self.assertEqual(B.nnz,10)
        self.assertEqual(A.nnz,10)
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])
        f[4,2] = 0.
        A[4,2] = 0.
        self.assertEqual(len(f.variables),3)
        self.assertEqual(len(f.parameters),6)
        self.assertEqual(f.nnz,9)
        B = f.value
        self.assertEqual(B.nnz,9)
        self.assertEqual(A.nnz,9)
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])        
        f[17,17] = 23.8
        A[17,17] = 23.8
        self.assertEqual(len(f.variables),3)
        self.assertEqual(len(f.parameters),6)
        self.assertEqual(f.nnz,10)
        B = f.value
        self.assertEqual(B.nnz,10)
        self.assertEqual(A.nnz,10)
        for i in range(0,A.nnz):
            self.assertEqual(A.rows[i],B.rows[i])
            self.assertEqual(A.data[i],B.data[i])        

    def test_cvxpy_sparray_setitem(self):
        f = c.arrays.cvxpy_sparray(3,7)
        self.assertRaises(TypeError,f.__setitem__,5,10)
        self.assertRaises(TypeError,f.__setitem__,[1,2],20)
        self.assertRaises(TypeError,f.__setitem__,(1,2,3),10)
        self.assertRaises(TypeError,f.__setitem__,([1,2,3],2),10)
        self.assertRaises(TypeError,f.__setitem__,(2,[1,2,3]),10)
        self.assertRaises(TypeError,f.__setitem__,(slice(0,2,1),1),1)
        self.assertRaises(TypeError,f.__setitem__,(1,slice(0,2,1)),1)
        self.assertRaises(TypeError,f.__setitem__,(slice(0,2,1),slice(0,2,1)),1)                                                 
        x = c.scalars.cvxpy_scalar_var()
        f.__setitem__((1,2),x)
        self.assertTrue(f[1,2] is x)
        self.assertEqual(f.nnz,1)
        self.assertRaises(ValueError,f.__setitem__,(-1,3),1)
        self.assertRaises(ValueError,f.__setitem__,(0,-1),1)
        self.assertRaises(ValueError,f.__setitem__,(3,0),1)
        self.assertRaises(ValueError,f.__setitem__,(0,7),1)
        a = parameter()
        f.__setitem__((np.int64(2),np.int64(6)),a)
        self.assertTrue(f[2,6] is a)
        self.assertEqual(f.nnz,2)
        self.assertRaises(TypeError,f.__setitem__,(1.3,2),10)
        self.assertRaises(TypeError,f.__setitem__,(0,2.2),10)
        b = parameter()
        f.__setitem__((np.int8(1),np.int16(5)),b)
        self.assertTrue(f[np.uint(1),np.int64(5)] is b)
        self.assertEqual(f.nnz,3)

    def test_cvxpy_sparray_getitem(self):
        f = c.arrays.cvxpy_sparray(30,40)
        A = sp.rand(30,40,density=0.5).tolil()
        for i in range(0,30):
            for j in range(0,40):
                if A[i,j] != 0.:
                    x = variable()
                    x.value = A[i,j]
                    f[i,j] = x
        self.assertEqual(f.nnz,A.nnz)                
        self.assertRaises(TypeError,f.__getitem__,4)
        self.assertRaises(TypeError,f.__getitem__,(1,2,3))
        self.assertRaises(TypeError,f.__getitem__,(2.3,0))
        self.assertRaises(TypeError,f.__getitem__,(0,1.3))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,1),slice(0,2,float(1))))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,1),slice(0,float(2),1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,1),slice(np.float64(0),2,1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,2,np.float(1)),slice(0,2,1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(float(0),2,1),slice(0,2,1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0,np.float64(2),1),slice(0,2,1)))
        self.assertRaises(ValueError,f.__getitem__,(-1,2))
        self.assertRaises(ValueError,f.__getitem__,(31,2))
        self.assertRaises(ValueError,f.__getitem__,(1,-1))
        self.assertRaises(ValueError,f.__getitem__,(1,50))
        self.assertRaises(ValueError,f.__getitem__,(slice(-1,2,1),0))
        self.assertRaises(ValueError,f.__getitem__,(0,slice(-1,2,1)))
        self.assertRaises(ValueError,f.__getitem__,(slice(0,32,1),0))
        self.assertRaises(ValueError,f.__getitem__,(0,slice(0,50,1)))
        self.assertRaises(TypeError,f.__getitem__,(0,slice(0,4,1.1)))
        self.assertRaises(TypeError,f.__getitem__,(slice(0.1,4,1),2))
        f1 = f[2:20:3,10:20:2]
        A1 = A[2:20:3,10:20:2]
        B1 = f1.value
        self.assertTrue(type(B1) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(B1.nnz,A1.nnz)
        self.assertTrue(np.allclose(B1.todense(),A1.todense()))
        f2 = f[2::np.uint(3),10:20]
        A2 = A[2::3,np.int64(10):20]
        B2 = f2.value
        self.assertTrue(type(B2) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(B2.nnz,A2.nnz)
        self.assertTrue(np.allclose(B2.todense(),A2.todense()))
        f3 = f[:15:3,:]
        A3 = A[:15:np.int8(3),:]
        B3 = f3.value
        self.assertTrue(type(B3) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(B3.nnz,A3.nnz)
        self.assertTrue(np.allclose(B3.todense(),A3.todense()))
        f4 = f[:,:]
        A4 = A[:,:]
        B4 = f4.value
        self.assertTrue(type(B4) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(B4.nnz,A4.nnz)
        self.assertTrue(np.allclose(B4.todense(),A4.todense()))
        for i in range(0,30):
            for j in range(0,40):
                obj = f[i,j]
                if np.isscalar(obj):
                    self.assertEqual(obj,A[i,j])
                else:
                    self.assertEqual(obj.value,A[i,j])
                    
