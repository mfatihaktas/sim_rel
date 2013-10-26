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

# Test scalars
class TestScalars(unittest.TestCase):
    
    # cvxpy_obj
    def test_cvxpy_obj_init(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertEqual(x.type,c.defs.CONSTANT)
        self.assertEqual(x.value,5)
        self.assertEqual(x.name,'5')
        self.assertEqual(x.shape,(1,1))
        self.assertEqual(type(x.variables),c.constraints.cvxpy_list)
        self.assertEqual(x.variables,[])
        self.assertEqual(type(x.parameters),c.constraints.cvxpy_list)
        self.assertEqual(x.parameters,[])
        self.assertTrue(x.T is x)
        y = c.scalars.cvxpy_scalar_var()
        self.assertTrue(y.T is y)
        z = c.scalars.cvxpy_scalar_param()
        self.assertTrue(z.T is z)
        w = y+1
        self.assertTrue(w.T is w)

    def test_cvxpy_obj_is_convex(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertTrue(x.is_convex())

    def test_cvxpy_obj_is_concave(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertTrue(x.is_concave())
    
    def test_cvxpy_obj_is_dcp(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertTrue(x.is_dcp())

    def test_cvxpy_obj_is_affine(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertTrue(x.is_affine())
       
    def test_cvxpy_obj_is_nonnegative_constant(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertTrue(x.is_nonnegative_constant())
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,-5,str(-5))
        self.assertFalse(x.is_nonnegative_constant())
    
    def test_cvxpy_obj_is_nonpositive_constant(self):
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertFalse(x.is_nonpositive_constant())
        x = c.scalars.cvxpy_obj(c.defs.CONSTANT,-5,str(-5))
        self.assertTrue(x.is_nonpositive_constant())
        
    def test_cvxpy_obj_arith(self):
        x = c.scalars.cvxpy_scalar_var()
        f = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        a = parameter()
        t = x+a
        A = matrix([[1,2],[3,4]])
        s1L = x + 5
        s1R = 5 + x
        self.assertEqual(s1L.type,c.defs.TREE)
        self.assertEqual(s1L.item.name,c.defs.SUMMATION)
        self.assertEqual(s1R.item.name,c.defs.SUMMATION)
        self.assertEqual(s1R.type,c.defs.TREE)
        self.assertEqual(s1L.item.type,c.defs.OPERATOR)
        self.assertEqual(s1L.children[0],x)
        self.assertEqual(s1L.children[1].type,c.defs.CONSTANT)
        self.assertEqual(s1L.children[1].value,5)
        self.assertEqual(s1R.item.type,c.defs.OPERATOR)
        self.assertEqual(s1R.children[1],x)
        self.assertEqual(s1R.children[0].type,c.defs.CONSTANT)
        self.assertEqual(s1R.children[0].value,5)
        s2L = x + f
        s2R = f + x
        self.assertEqual(s2L.item.name,c.defs.SUMMATION)
        self.assertEqual(s2R.item.name,c.defs.SUMMATION)
        self.assertEqual(s2L.item.type,c.defs.OPERATOR)
        self.assertEqual(s2L.children[0],x)
        self.assertEqual(s2L.children[1].type,c.defs.CONSTANT)
        self.assertEqual(s2L.children[1].value,5)
        self.assertEqual(s2R.item.type,c.defs.OPERATOR)
        self.assertEqual(s2R.children[1],x)
        self.assertEqual(s2R.children[0].type,c.defs.CONSTANT)
        self.assertEqual(s2R.children[0].value,5)
        s3L = x + a
        s3R = a + x
        self.assertEqual(s3L.item.name,c.defs.SUMMATION)
        self.assertEqual(s3R.item.name,c.defs.SUMMATION)
        self.assertEqual(s3L.item.type,c.defs.OPERATOR)
        self.assertEqual(s3L.children,[x,a])
        self.assertEqual(s3R.item.type,c.defs.OPERATOR)
        self.assertEqual(s3R.children,[a,x])
        s4L = x + t
        s4R = t + x
        self.assertEqual(s4L.item.name,c.defs.SUMMATION)
        self.assertEqual(s4R.item.name,c.defs.SUMMATION)
        self.assertEqual(s4L.item.type,c.defs.OPERATOR)
        self.assertEqual(s4L.children,[x,x,a])
        self.assertEqual(s4R.item.type,c.defs.OPERATOR)
        self.assertEqual(s4R.children,[x,a,x])
        s5L = x + A
        s5R = A + x
        for i in range(0,A.shape[0],1):
            for j in range(0,A.shape[1],1):
                self.assertEqual(s5L[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s5R[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(s5L[i,j].children[0],x)
                self.assertEqual(s5L[i,j].children[1].value,A[i,j])
                self.assertEqual(s5R[i,j].children[1],x)
                self.assertEqual(s5R[i,j].children[0].value,A[i,j])
                self.assertEqual(s5L[i,j].type,c.defs.TREE)
                self.assertEqual(s5R[i,j].type,c.defs.TREE)
                self.assertEqual(s5L[i,j].item.name,c.defs.SUMMATION)
                self.assertEqual(s5R[i,j].item.name,c.defs.SUMMATION)
        s6L = x-4
        s6R = 4-x
        self.assertEqual(s6L.type,c.defs.TREE)
        self.assertEqual(s6L.item.name,c.defs.SUMMATION)
        self.assertEqual(s6R.item.name,c.defs.SUMMATION)
        self.assertEqual(s6R.type,c.defs.TREE)
        self.assertEqual(s6L.item.type,c.defs.OPERATOR)
        self.assertEqual(s6L.children[0],x)
        self.assertEqual(s6L.children[1].type,c.defs.CONSTANT)
        self.assertEqual(s6L.children[1].value,-4)
        self.assertEqual(s6R.item.type,c.defs.OPERATOR)
        self.assertEqual(s6R.children[1].type,c.defs.TREE)
        self.assertEqual(s6R.children[1].item.type,c.defs.OPERATOR)
        self.assertEqual(s6R.children[1].item.name,c.defs.MULTIPLICATION)
        self.assertEqual(s6R.children[1].children[1],x)
        self.assertEqual(s6R.children[1].children[0].type,c.defs.CONSTANT)
        self.assertEqual(s6R.children[1].children[0].value,-1)
        self.assertEqual(s6R.children[0].type,c.defs.CONSTANT)
        self.assertEqual(s6R.children[0].value,4)
               
    def test_cvxpy_obj_mulhandle(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        A = matrix([[2,3],[4,5]])
        As = spmatrix(sp.rand(20,30,density=0.5))
        t = x*5
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].value,5)
        self.assertEqual(t.children[0].name,str(5))
        self.assertEqual(t.children[1],x)
        t = 5*x
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].value,5)
        self.assertEqual(t.children[0].name,str(5))
        self.assertEqual(t.children[1],x)
        t = x*0
        self.assertEqual(t,0)
        t = 0*x
        self.assertEqual(t,0)
        t = 1*x
        self.assertEqual(t,x)
        t = x*1
        self.assertEqual(t,x)
        t = 5*(x+2)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.SUMMATION)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].children[0].value,5)
        self.assertEqual(t.children[0].children[0].name,str(5))
        self.assertEqual(t.children[0].children[1],x)
        self.assertEqual(t.children[1].type,c.defs.CONSTANT)
        self.assertEqual(t.children[1].value,10)
        self.assertEqual(t.children[1].name,str(10))
        t = (x+2)*5
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.SUMMATION) 
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].children[0].value,5)
        self.assertEqual(t.children[0].children[0].name,str(5))
        self.assertEqual(t.children[0].children[1],x)
        self.assertEqual(t.children[1].type,c.defs.CONSTANT)
        self.assertEqual(t.children[1].value,10)
        self.assertEqual(t.children[1].name,str(10))
        t = (x+1)*a
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[1].type,c.defs.TREE)
        self.assertEqual(t.children[1].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[1].item.name,c.defs.SUMMATION)
        self.assertEqual(t.children[1].children[0],x)
        self.assertEqual(t.children[1].children[1].type,c.defs.CONSTANT)
        self.assertEqual(t.children[1].children[1].value,1)
        self.assertEqual(t.children[0],a)        
        t = a*(x+1)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[1].type,c.defs.TREE)
        self.assertEqual(t.children[1].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[1].item.name,c.defs.SUMMATION)
        self.assertEqual(t.children[1].children[0],x)
        self.assertEqual(t.children[1].children[1].type,c.defs.CONSTANT)
        self.assertEqual(t.children[1].children[1].value,1)
        self.assertEqual(t.children[0],a)        
        t = x*(a+a)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[1].type,c.defs.VARIABLE)
        self.assertEqual(t.children[1],x)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,c.defs.SUMMATION)
        self.assertEqual(t.children[0].children[0],a)
        self.assertEqual(t.children[0].children[1],a)
        t = (a+a)*x
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[1].type,c.defs.VARIABLE)
        self.assertEqual(t.children[1],x)
        self.assertEqual(t.children[0].type,c.defs.TREE)
        self.assertEqual(t.children[0].item.type,c.defs.OPERATOR)
        self.assertEqual(t.children[0].item.name,c.defs.SUMMATION)
        self.assertEqual(t.children[0].children[0],a)
        self.assertEqual(t.children[0].children[1],a)
        t = 4*(5*x)
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].value,20)
        self.assertEqual(t.children[0].name,str(20))
        self.assertEqual(t.children[1],x)
        t = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))*4
        self.assertEqual(t.type,c.defs.CONSTANT)
        self.assertEqual(t.value,20)
        self.assertEqual(t.name,str(20))
        t = 4*c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertEqual(t.type,c.defs.CONSTANT)
        self.assertEqual(t.value,20)
        self.assertEqual(t.name,str(20))
        t = a*A
        self.assertTrue(type(t) is c.arrays.cvxpy_array)
        self.assertEqual(t.shape,A.shape)
        for i in range(0,A.shape[0],1):
            for j in range(0,A.shape[1],1):
                self.assertEqual(t[i,j].type,c.defs.TREE)
                self.assertEqual(t[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(t[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(t[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(t[i,j].children[0].value,A[i,j])
                self.assertEqual(t[i,j].children[0].name,str(A[i,j]))
                self.assertEqual(t[i,j].children[1],a)
        t = x*As
        self.assertTrue(type(t) is c.arrays.cvxpy_sparray)
        self.assertEqual(t.nnz,As.nnz)
        self.assertEqual(t.shape,As.shape)
        for i in range(0,As.shape[0]):
            rowi_indeces = As.rows[i]
            rowi_values = As.data[i]
            for k in range(0,len(rowi_indeces)):
                j = rowi_indeces[k]
                aij = rowi_values[k]
                self.assertEqual(t[i,j].type,c.defs.TREE)
                self.assertEqual(t[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(t[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(t[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(t[i,j].children[0].value,aij)
                self.assertEqual(t[i,j].children[0].name,str(aij))
                self.assertTrue(t[i,j].children[1] is x)
        t = As*a
        self.assertTrue(type(t) is c.arrays.cvxpy_sparray)
        self.assertEqual(t.nnz,As.nnz)
        self.assertEqual(t.shape,As.shape)
        for i in range(0,As.shape[0]):
            rowi_indeces = As.rows[i]
            rowi_values = As.data[i]
            for k in range(0,len(rowi_indeces)):
                j = rowi_indeces[k]
                aij = rowi_values[k]
                self.assertEqual(t[i,j].type,c.defs.TREE)
                self.assertEqual(t[i,j].item.type,c.defs.OPERATOR)
                self.assertEqual(t[i,j].item.name,c.defs.MULTIPLICATION)
                self.assertEqual(t[i,j].children[0].type,c.defs.CONSTANT)
                self.assertEqual(t[i,j].children[0].value,aij)
                self.assertEqual(t[i,j].children[0].name,str(aij))
                self.assertTrue(t[i,j].children[1] is a)        
                
    def test_cvxpy_obj_neg(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        f = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        t = -x
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].value,-1)
        self.assertEqual(t.children[0].name,'-1.0')
        self.assertEqual(t.children[1],x)
        t = -a
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.MULTIPLICATION)
        self.assertEqual(t.children[0].type,c.defs.CONSTANT)
        self.assertEqual(t.children[0].value,-1)
        self.assertEqual(t.children[0].name,'-1.0')
        self.assertEqual(t.children[1],a)
        t = -f
        self.assertEqual(t.type,c.defs.CONSTANT)
        self.assertEqual(t.value,-5)
        self.assertEqual(t.name,'-5.0')

    def test_cvxpy_obj_str(self):
        f = c.scalars.cvxpy_obj(c.defs.CONSTANT,5,str(5))
        self.assertEqual(str(f),'5')
    
    # cvxpy_scalar_var
    def test_cvxpy_scalar_var_init_(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var(name='y')
        self.assertEqual(x.type,c.defs.VARIABLE)
        self.assertEqual(y.type,c.defs.VARIABLE)
        self.assertTrue(np.isnan(x.value))
        self.assertTrue(np.isnan(y.value))
        self.assertEqual(y.name,'y')
        self.assertEqual(x.shape,(1,1))
        self.assertEqual(y.shape,(1,1))
    
    def test_cvxpy_scalar_var_getattribute(self):
        x = c.scalars.cvxpy_scalar_var(name='x')
        self.assertEqual(type(x.variables),c.constraints.cvxpy_list)
        self.assertEqual(type(x.parameters),c.constraints.cvxpy_list)
        self.assertEqual(x.variables,[x])
        self.assertEqual(x.parameters,[])
    
    def test_cvxpy_scalar_var_isnonnegconstant(self):
        x = c.scalars.cvxpy_scalar_var()
        self.assertFalse(x.is_nonnegative_constant())

    def test_cvxpy_scalar_var_isnonpositiveconstant(self):
        x = c.scalars.cvxpy_scalar_var()
        self.assertFalse(x.is_nonpositive_constant())

    def test_cvxpy_scalar_var_is_convex(self):
        x = c.scalars.cvxpy_scalar_var()
        self.assertTrue(x.is_convex())

    def test_cvxpy_scalar_var_is_concave(self):
        x = c.scalars.cvxpy_scalar_var()
        self.assertTrue(x.is_concave())
    
    def test_cvxpy_scalar_var_is_dcp(self):
        x = c.scalars.cvxpy_scalar_var()
        self.assertTrue(x.is_dcp())

    def test_cvxpy_scalar_var_is_affine(self):
        x = c.scalars.cvxpy_scalar_var()
        self.assertTrue(x.is_affine())

    # cvxpy_scalar_param
    def test_cvxpy_scalar_param_init(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(a.type,c.defs.PARAMETER)
        self.assertTrue(np.isnan(a.value))
        self.assertEqual(a.shape,(1,1))
        self.assertTrue(a.attribute is None)
        a = c.scalars.cvxpy_scalar_param(name='a')
        self.assertEqual(a.type,c.defs.PARAMETER)
        self.assertTrue(np.isnan(a.value))
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.name,'a')
        self.assertTrue(a.attribute is None)
        a = c.scalars.cvxpy_scalar_param('nonnegative','a')
        self.assertEqual(a.type,c.defs.PARAMETER)
        self.assertTrue(np.isnan(a.value))
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.name,'a')
        self.assertEqual(a.attribute,c.defs.NONNEGATIVE)
        a = c.scalars.cvxpy_scalar_param('nonpositive','a')
        self.assertEqual(a.type,c.defs.PARAMETER)
        self.assertTrue(np.isnan(a.value))
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.name,'a')
        self.assertEqual(a.attribute,c.defs.NONPOSITIVE)
    
    def test_cvxpy_scalar_param_getattribute(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertEqual(type(a.variables),c.constraints.cvxpy_list)
        self.assertEqual(type(a.parameters),c.constraints.cvxpy_list)
        self.assertEqual(a.variables,[])
        self.assertEqual(a.parameters,[a])

    def test_cvxpy_scalar_param_setattr(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue(np.isnan(a.value))
        a.value = 10
        self.assertEqual(a.value,10)
        a.value = -10
        self.assertEqual(a.value,-10)
        self.assertRaises(TypeError,
                          a.__setattr__,'value',np.matrix([1]))
        self.assertRaises(TypeError,
                          a.__setattr__,'value',[1,2,3])
        a = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        self.assertTrue(np.isnan(a.value))
        a.value = 0
        self.assertEqual(a.value,0)
        a.value = 10
        self.assertEqual(a.value,10)
        self.assertRaises(ValueError,
                          a.__setattr__,'value',-10)
        a = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertTrue(np.isnan(a.value))
        a.value = 0
        self.assertEqual(a.value,0)
        a.value = -10
        self.assertEqual(a.value,-10)
        self.assertRaises(ValueError,
                          a.__setattr__,'value',10)
        a = c.scalars.cvxpy_scalar_param()
        self.assertRaises(ValueError,
                          a.__setattr__,'attribute','badness')
        self.assertRaises(ValueError,
                          a.__setattr__,'attribute',[1,2,3])
        a.attribute = 'nonnegative'
        self.assertEqual(a.attribute,'nonnegative')
        a.attribute = 'nonpositive'
        self.assertEqual(a.attribute,'nonpositive')
        a.attribute = None
        self.assertTrue(a.attribute is None)
        a = c.scalars.cvxpy_scalar_param()
        a.value = -10
        self.assertEqual(a.value,-10)
        a.attribute = 'nonnegative'
        self.assertTrue(np.isnan(a.value))
        a.value = 10
        self.assertEqual(a.value,10)
        a.attribute = 'nonpositive'
        self.assertTrue(np.isnan(a.value))
        
    def test_cvxpy_scalar_param_isnonnegativeconstant(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertFalse(a.is_nonnegative_constant())
        a.attribute = 'nonnegative'
        self.assertTrue(a.is_nonnegative_constant())
        a.attribute = 'nonpositive'
        self.assertFalse(a.is_nonnegative_constant())

    def test_cvxpy_scalar_param_isnonpositiveconstant(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertFalse(a.is_nonpositive_constant())
        a.attribute = 'nonnegative'
        self.assertFalse(a.is_nonpositive_constant())
        a.attribute = 'nonpositive'
        self.assertTrue(a.is_nonpositive_constant())

    def test_cvxpy_scalar_param_is_convex(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue(a.is_convex())

    def test_cvxpy_scalar_param_is_concave(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue(a.is_concave())
    
    def test_cvxpy_scalar_param_is_dcp(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue(a.is_dcp())

    def test_cvxpy_scalar_param_is_affine(self):
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue(a.is_affine())

    # cvxpy_tree
    def test_cvxpy_tree_init(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        t = x + a
        self.assertEqual(t.type,c.defs.TREE)
        self.assertEqual(t.name,'')
        self.assertEqual(t.item.type,c.defs.OPERATOR)
        self.assertEqual(t.item.name,c.defs.SUMMATION)
        self.assertEqual(t.children[0],x)
        self.assertEqual(t.children[1],a)

    def test_cvxpy_tree_getattribute(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        b = c.scalars.cvxpy_scalar_param()
        x.value = 10
        y.value = 3
        a.value = 5
        b.value = 8
        t1 = x+a
        self.assertTrue(type(t1.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(t1.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(t1.value,15)
        self.assertEqual(t1.variables,[x])
        self.assertEqual(t1.parameters,[a])
        t2 = a+x
        self.assertTrue(type(t2.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(t2.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(t2.value,15)
        self.assertEqual(t2.variables,[x])
        self.assertEqual(t2.parameters,[a])
        t3 = b+2*(x+y)-a*3
        self.assertTrue(type(t3.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(t3.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(t3.value,19)
        self.assertTrue(len(t3.variables) == 2)
        self.assertEqual(set(t3.variables), set([x, y]))
        self.assertEqual(set(t3.parameters), set([b, a]))
        self.assertTrue(len(t3.parameters) == 2)
        t4 = (a+3*b)*(x+abs(y-2*y))
        self.assertTrue(type(t4.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(t4.parameters) is c.constraints.cvxpy_list)
        self.assertTrue(np.allclose(t4.value,377))
        self.assertTrue(len(t4.variables) == 2)
        self.assertEqual(set(t4.variables), set([x, y]))
        self.assertEqual(set(t4.parameters), set([a, b]))
        self.assertTrue(len(t4.parameters) == 2)
        
    def test_cvxpy_tree_str(self):
        x = c.scalars.cvxpy_scalar_var(name='x')
        a = c.scalars.cvxpy_scalar_param(name='a')
        t = x + 5
        self.assertEqual(str(t),'x + 5')
        t = x * 5
        self.assertEqual(str(t),'5*x')
        t = (x + 4)*4
        self.assertEqual(str(t),'4*x + 16')
        t = (x+5)*(a + 5)
        self.assertEqual(str(t),'(a + 5)*(x + 5)')
        t = square(x+4)
        self.assertEqual(str(t),'square(x + 4)')

    def test_cvxpy_tree_is_convex(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue((x+5).is_convex())
        self.assertTrue((x+5+a).is_convex())
        self.assertTrue((x+5+2*(x-1)).is_convex())
        self.assertTrue((square(x) - sqrt(x)).is_convex())
        self.assertFalse((square(x) + sqrt(x)).is_convex())
        self.assertTrue((5*x).is_convex())
        self.assertTrue((x*5).is_convex())
        self.assertTrue(((-5)*x).is_convex())
        self.assertTrue((x*(-5)).is_convex())
        self.assertTrue((a*x).is_convex())
        self.assertTrue((a*5).is_convex())
        self.assertFalse((-square(2*(x+1))).is_convex())
        self.assertTrue((square(2*(x+1))).is_convex())
        self.assertTrue((-log(2*(x+1))).is_convex())
        self.assertTrue((-5*log(2*(x+1))).is_convex())
        self.assertTrue(max(vstack([5*x,4,square(x)])).is_convex())
        self.assertFalse(max(hstack([5*x,5,sqrt(x)])).is_convex())
        self.assertTrue(((-8)*(log(sqrt(x+4)))).is_convex())
        self.assertTrue((abs(4-x)).is_convex())
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        d = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertTrue((a+x).is_convex())
        self.assertTrue((x+a).is_convex())
        self.assertTrue((b+x).is_convex())
        self.assertTrue((x+b).is_convex())
        self.assertTrue((d+x).is_convex())
        self.assertTrue((x+d).is_convex())
        self.assertTrue((d+b).is_convex())
        self.assertTrue((d+a).is_convex())
        self.assertTrue((b-d).is_convex())
        self.assertTrue((-a-b).is_convex())
        self.assertTrue((2-a-b+d-100).is_convex())
        self.assertTrue((a*x).is_convex())
        self.assertTrue((b*x).is_convex())
        self.assertTrue((d*x).is_convex())
        self.assertTrue((x*a).is_convex())
        self.assertTrue((x*b).is_convex())
        self.assertTrue((x*d).is_convex())
        self.assertTrue((a*b).is_convex())
        self.assertTrue((a*d).is_convex())
        self.assertTrue((a*a).is_convex())
        self.assertTrue((b*a).is_convex())
        self.assertTrue((b*b).is_convex())
        self.assertTrue((b*d).is_convex())
        self.assertTrue((d*a).is_convex())
        self.assertTrue((d*b).is_convex())
        self.assertTrue((d*b).is_convex())
        self.assertFalse((a*square(x)).is_convex())
        self.assertFalse((a*log(x)).is_convex())
        self.assertTrue((b*square(x)).is_convex())
        self.assertTrue((b*abs(x+d+b+a)).is_convex())
        self.assertTrue(((b-4*d)*square(x+10)).is_convex())
        self.assertFalse((d*exp(x)).is_convex())
        self.assertTrue((d*sqrt(x)).is_convex())
        self.assertFalse((square(x)*a).is_convex())
        self.assertFalse((log(x)*a).is_convex())
        self.assertTrue((square(x)*b).is_convex())
        self.assertTrue((abs(x+d+b+a)*b).is_convex())
        self.assertTrue((square(x+10)*(3*b-10*d)).is_convex())
        self.assertFalse((exp(x)*d).is_convex())

    def test_cvxpy_tree_is_concave(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue((x+5).is_concave())
        self.assertTrue((x+5+a).is_concave())
        self.assertTrue((x+5+2*(x-1)).is_concave())
        self.assertTrue((-square(x) + sqrt(x)).is_concave())
        self.assertFalse((square(x) + sqrt(x)).is_concave())
        self.assertTrue((5*x).is_concave())
        self.assertTrue((x*5).is_concave())
        self.assertTrue(((-5)*x).is_concave())
        self.assertTrue((x*(-5)).is_concave())
        self.assertTrue((a*x).is_concave())
        self.assertTrue((a*5).is_concave())
        self.assertTrue((-square(2*(x+1))).is_concave())
        self.assertFalse((square(2*(x+1))).is_concave())
        self.assertTrue((log(2*(x+1)+a)).is_concave())
        self.assertTrue((5*log(2*(x-a))).is_concave())
        self.assertTrue((min(vstack([5*x,4,sqrt(x)]))).is_concave())
        self.assertFalse((min(vstack([5*x,5,abs(x)]))).is_concave())
        self.assertTrue((8*log(sqrt(a*x+4))).is_concave())
        self.assertFalse((abs(4-x)).is_concave())
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        d = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertTrue((a+x).is_concave())
        self.assertTrue((x+a).is_concave())
        self.assertTrue((b+x).is_concave())
        self.assertTrue((x+b).is_concave())
        self.assertTrue((d+x).is_concave())
        self.assertTrue((x+d).is_concave())
        self.assertTrue((d+b).is_concave())
        self.assertTrue((d+a).is_concave())
        self.assertTrue((b-d).is_concave())
        self.assertTrue((-a-b).is_concave())
        self.assertTrue((2-a-b+d-100).is_concave())
        self.assertTrue((a*x).is_concave())
        self.assertTrue((b*x).is_concave())
        self.assertTrue((d*x).is_concave())
        self.assertTrue((x*a).is_concave())
        self.assertTrue((x*b).is_concave())
        self.assertTrue((x*d).is_concave())
        self.assertTrue((a*b).is_concave())
        self.assertTrue((a*d).is_concave())
        self.assertTrue((a*a).is_concave())
        self.assertTrue((b*a).is_concave())
        self.assertTrue((b*b).is_concave())
        self.assertTrue((b*d).is_concave())
        self.assertTrue((d*a).is_concave())
        self.assertTrue((d*b).is_concave())
        self.assertTrue((d*b).is_concave())
        self.assertFalse((a*sqrt(x)).is_concave())
        self.assertFalse((a*square(x)).is_concave())
        self.assertTrue((b*sqrt(x)).is_concave())
        self.assertTrue((b*log(x+d+b+a)).is_concave())
        self.assertTrue(((b-4*d)*log(x+10)).is_concave())
        self.assertFalse((d*sqrt(x)).is_concave())
        self.assertTrue((d*exp(x)).is_concave())
        self.assertFalse((square(x)*a).is_concave())
        self.assertFalse((log(x)*a).is_concave())
        self.assertTrue((sqrt(x)*b).is_concave())
        self.assertTrue((log(x+d+b+a)*b).is_concave())
        self.assertTrue((sqrt(x+10)*(3*b-10*d)).is_concave())
        self.assertTrue((exp(x)*d).is_concave())

    def test_cvxpy_tree_is_dcp(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue((x+1).is_dcp())
        self.assertTrue((x+a).is_dcp())
        self.assertTrue((square(x+3)).is_dcp())
        self.assertFalse((square(square(x+4))).is_dcp())
        self.assertTrue((log(sqrt(x)+4)).is_dcp())
        self.assertFalse((log(sqrt(x)) + square(x)).is_dcp())
        self.assertTrue((x + square(x) - sqrt(x)).is_dcp())
        self.assertFalse((x + square(x) + sqrt(x)).is_dcp())
        self.assertTrue((x - square(x) + sqrt(x)).is_dcp())
        self.assertTrue((5*x).is_dcp())
        self.assertTrue((x*5).is_dcp())
        self.assertTrue(((5+4)*(x+2*x+2)).is_dcp())
        self.assertTrue(((a+4)*x).is_dcp())
        self.assertTrue((x*(a+4)).is_dcp())
        self.assertTrue((square(x+4-2+2*(x+1))).is_dcp())
        self.assertTrue(max(vstack([3,4,5,x,-x])).is_dcp())
        self.assertFalse(max(hstack([sqrt(x),x])).is_dcp())
        self.assertTrue((log_sum_exp(vstack([-sqrt(x),square(x),
                                              5,x]))).is_dcp())
        self.assertTrue((quad_over_lin(5,x)).is_dcp())
        self.assertTrue((quad_over_lin(5,sqrt(x))).is_dcp())
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        d = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertTrue((a+a).is_dcp())
        self.assertTrue((a+x).is_dcp())
        self.assertTrue((x+a).is_dcp())
        self.assertTrue((a+b).is_dcp())
        self.assertTrue((b+a).is_dcp())
        self.assertTrue((a+d).is_dcp())
        self.assertTrue((d+a).is_dcp())
        self.assertTrue((b+d).is_dcp())
        self.assertTrue((d+b).is_dcp())
        self.assertTrue((1+2+a+b+x+d+100).is_dcp())
        self.assertTrue((a*a).is_dcp())
        self.assertTrue((a*b*d).is_dcp())
        self.assertTrue((d*b*a).is_dcp())
        self.assertTrue((b*d*a).is_dcp())
        self.assertTrue((b*a*d).is_dcp())
        self.assertTrue((b*a).is_dcp())
        self.assertTrue((b*d).is_dcp())
        self.assertTrue((a*d).is_dcp())
        self.assertTrue((a*b).is_dcp())
        self.assertTrue((d*a).is_dcp())
        self.assertTrue((d*b).is_dcp())
        self.assertTrue((a*10).is_dcp())
        self.assertTrue((10*a).is_dcp())
        self.assertTrue(((-100)*a).is_dcp())
        self.assertTrue(((-100)*b).is_dcp())
        self.assertTrue(((-100)*d).is_dcp())
        self.assertTrue((a*(-100)).is_dcp())
        self.assertTrue((b*(-100)).is_dcp())
        self.assertTrue((d*(-100)).is_dcp())
        self.assertTrue(abs(a+b+d+x+100).is_dcp())
        self.assertTrue(log(a*100+b*(-10)+d*x+100*x*b).is_dcp())
        self.assertTrue((b*square(d*x+a)).is_dcp())
        self.assertTrue((d*square(d*x+a)).is_dcp())
        self.assertTrue((d*square(x+a)-b*abs(x)).is_dcp())
        self.assertFalse((d*square(x+a)-d*abs(x)).is_dcp())
        self.assertFalse((a*square(d*x+a)).is_dcp())
        
    def test_cvxpy_tree_is_affine(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        self.assertTrue((x+4+2*x).is_affine())
        self.assertFalse((x+square(x)).is_affine())
        self.assertTrue((4*x).is_affine())
        self.assertTrue((4*(x+12)).is_affine())
        self.assertTrue((a*x).is_affine())
        self.assertTrue((x+a).is_affine())
        self.assertTrue((x*a).is_affine())
        self.assertTrue((a*5).is_affine())
        self.assertTrue((5*a).is_affine())
        self.assertFalse((square(x)).is_affine())
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        d = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertTrue((x+a).is_affine())
        self.assertTrue((x+a+b+d).is_affine())
        self.assertFalse(abs(x+a+180).is_affine())
        self.assertTrue(abs(a+b+100*d).is_affine())
        self.assertTrue((a*b).is_affine())
        self.assertTrue((a*x).is_affine())
        self.assertTrue((d*a).is_affine())
        self.assertTrue((b*a).is_affine())
        self.assertTrue((x*a).is_affine())
        self.assertTrue((b*d).is_affine())
        self.assertTrue((b*x).is_affine())
        self.assertTrue((d*x).is_affine())
        self.assertTrue(((a+b+100*d)*(x+100*x+2*x+1000)).is_affine())
        
    def test_cvxpy_tree_isnonnegativeconstant(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        d = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertTrue((b+1).is_nonnegative_constant())
        self.assertFalse((-(b+1)).is_nonnegative_constant())
        self.assertTrue((1-(-b)).is_nonnegative_constant())
        self.assertFalse((-1+b).is_nonnegative_constant())
        self.assertFalse(square(b).is_nonnegative_constant())
        self.assertFalse((b+x).is_nonnegative_constant())
        self.assertFalse((1+x).is_nonnegative_constant())
        self.assertFalse((square(b+1)*abs(b+2*(b+1))).is_nonnegative_constant())
        self.assertTrue(((b+10)*(2*b+10)).is_nonnegative_constant())
        self.assertTrue(((-10)*(-b)).is_nonnegative_constant())
        self.assertFalse((a*10).is_nonnegative_constant())
        self.assertFalse((a+10).is_nonnegative_constant())
        self.assertFalse((a+a*a+10+a).is_nonnegative_constant())
        self.assertFalse((1+b+d).is_nonnegative_constant())
        self.assertTrue((1+b-d).is_nonnegative_constant())
        self.assertTrue((-d).is_nonnegative_constant())
        self.assertFalse((x+1).is_nonnegative_constant())
        self.assertFalse((a*(d+10)).is_nonnegative_constant())

    def test_cvxpy_tree_isnonpositiveconstant(self):
        x = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        d = c.scalars.cvxpy_scalar_param(attribute='nonpositive')
        self.assertFalse((b-1).is_nonpositive_constant())
        self.assertFalse((b+1).is_nonpositive_constant())
        self.assertTrue((-(b+1)).is_nonpositive_constant())
        self.assertFalse((1-(-b)).is_nonpositive_constant())
        self.assertFalse((-1-(-b)).is_nonpositive_constant())
        self.assertFalse((-1+b).is_nonpositive_constant())
        self.assertFalse(square(b).is_nonpositive_constant())
        self.assertFalse((b+x).is_nonpositive_constant())
        self.assertFalse((1+x).is_nonpositive_constant())
        self.assertFalse((square(b+1)*abs(b+2*(b+1))).is_nonpositive_constant())
        self.assertFalse(((b+10)*(2*b+10)).is_nonpositive_constant())
        self.assertTrue(((-b-10)*(2*b+10)).is_nonpositive_constant())
        self.assertFalse(((d+10)*(b-100)).is_nonpositive_constant())
        self.assertTrue(((100+b)*(-200+d)).is_nonpositive_constant())
        self.assertTrue(((-10)*(-d)).is_nonpositive_constant())
        self.assertFalse((a*10).is_nonpositive_constant())
        self.assertFalse((a+10).is_nonpositive_constant())
        self.assertFalse((a+a*a+10+a).is_nonpositive_constant())
        self.assertFalse((1+b+d).is_nonpositive_constant())
        self.assertTrue((-1+d-b).is_nonpositive_constant())
        self.assertTrue((-b).is_nonpositive_constant())
        self.assertFalse((x+1).is_nonpositive_constant())
        self.assertTrue((b*d).is_nonpositive_constant())
        self.assertTrue((d*b).is_nonpositive_constant())
        self.assertTrue(((-1)*b).is_nonpositive_constant())
        self.assertTrue((b*(-100)).is_nonpositive_constant())
        self.assertTrue((8*d).is_nonpositive_constant())
        self.assertTrue((d*8).is_nonpositive_constant())
        self.assertFalse((b*b).is_nonpositive_constant())
        self.assertTrue((b*(-9)).is_nonpositive_constant())
