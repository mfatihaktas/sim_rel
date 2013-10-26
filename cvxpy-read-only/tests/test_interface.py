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


# Test interface
class TestInterface(unittest.TestCase):

    # variable
    def test_variable(self):
        x = variable(4,2,None,'x')
        self.assertTrue(type(x) is c.arrays.cvxpy_var)
        self.assertEqual(x.type,c.defs.ARRAY)
        self.assertEqual(x.shape,(4,2))
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                self.assertTrue(type(x[i,j]) is c.scalars.cvxpy_scalar_var)
                self.assertEqual(str(x[i,j]),'x['+str(i)+','+str(j)+']')
        x = variable(1,1,name='x')
        self.assertTrue(type(x) is c.scalars.cvxpy_scalar_var)
        self.assertEqual(x.shape,(1,1))
        self.assertEqual(x.name,'x')
        x = variable(name='x')
        self.assertTrue(type(x) is c.scalars.cvxpy_scalar_var)
        self.assertEqual(x.shape,(1,1))
        self.assertEqual(x.name,'x')
        x = variable(4,4,'symmetric')
        self.assertTrue(type(x) is c.arrays.cvxpy_var)
        self.assertEqual(x.shape,(4,4))
        for i in range(0,x.shape[0],1):
            for j in range(0,i+1,1):
                self.assertTrue(type(x[i,j]) is c.scalars.cvxpy_scalar_var)
                self.assertTrue(x[i,j] is x[j,i])
        x = variable()
        self.assertTrue(type(x) is c.scalars.cvxpy_scalar_var)
        self.assertEqual(x.shape,(1,1))
        self.assertRaises(ValueError,variable,4,3,'lower_symmetric','x')
        self.assertRaises(ValueError,variable,4,4,'badness','x')
    
    def test_variable_reset(self):
        variable_reset()
        v = variable()
        self.assertEqual(str(v),'v0')
        v = variable()
        self.assertEqual(str(v),'v1')
        variable_reset()
        v = variable()
        self.assertEqual(str(v),'v0')

    def test_parameter(self):
        a = parameter(4,2,None,'a')
        self.assertTrue(type(a) is c.arrays.cvxpy_param)
        self.assertEqual(a.type,c.defs.ARRAY)
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertTrue(type(a[i,j]) is c.scalars.cvxpy_scalar_param)
                self.assertEqual(str(a[i,j]),'a['+str(i)+','+str(j)+']')
                self.assertTrue(a[i,j].attribute is None)
        self.assertEqual(a.shape,(4,2))
        a = parameter(1,1,name='a')
        self.assertTrue(type(a) is c.scalars.cvxpy_scalar_param)
        self.assertEqual(a.shape,(1,1))
        self.assertTrue(a.attribute is None)
        self.assertEqual(a.name,'a')
        a = parameter(name='a')
        self.assertTrue(type(a) is c.scalars.cvxpy_scalar_param)
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.attribute,None)
        self.assertEqual(a.name,'a')
        a = parameter()
        self.assertTrue(type(a) is c.scalars.cvxpy_scalar_param)
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.attribute,None)
        a = parameter(1,1,'nonnegative')
        self.assertTrue(type(a) is c.scalars.cvxpy_scalar_param)
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.attribute,c.defs.NONNEGATIVE)
        a = parameter(attribute='nonnegative')
        self.assertTrue(type(a) is c.scalars.cvxpy_scalar_param)
        self.assertEqual(a.shape,(1,1))
        self.assertEqual(a.attribute,c.defs.NONNEGATIVE)
        a = parameter(5,3,'nonpositive','a')
        self.assertTrue(type(a) is c.arrays.cvxpy_param)
        self.assertEqual(a.type,c.defs.ARRAY)
        self.assertEqual(a.shape,(5,3))
        for i in range(0,a.shape[0],1):
            for j in range(0,a.shape[1],1):
                self.assertEqual(a[i,j].attribute,c.defs.NONPOSITIVE)
        self.assertRaises(ValueError,parameter,1,1,'badness','a')
        
    def test_param_reset(self):
        parameter_reset()
        a = parameter()
        self.assertEqual(str(a),'a0')
        a = parameter()
        self.assertEqual(str(a),'a1')
        parameter_reset()
        a = parameter()
        self.assertEqual(str(a),'a0')
        
    def test_matrix(self):
        A = matrix([[1,2,3],[4,5,6]])
        self.assertTrue(type(A) is c.arrays.cvxpy_matrix)
        self.assertEqual(A.shape,(2,3))
        self.assertEqual(A[0,0],1)
        self.assertEqual(A[1,2],6)
        self.assertTrue(A.dtype is np.dtype(np.float64))
        B = matrix(np.matrix([[1,2],[3,4]]))
        self.assertTrue(type(B) is c.arrays.cvxpy_matrix)
        self.assertEqual(B.shape,(2,2))
        self.assertTrue(B.dtype is np.dtype(np.float64))
        C = matrix(np.array([1,2,3,3,4,5,6]))
        self.assertTrue(type(C) is c.arrays.cvxpy_matrix)
        self.assertEqual(C.shape,(1,7))
        self.assertTrue(C.dtype is np.dtype(np.float64))
        D = matrix("1,2,3;4,5,6")
        self.assertTrue(type(D) is c.arrays.cvxpy_matrix)
        self.assertEqual(D.shape,(2,3))
        self.assertTrue(D.dtype is np.dtype(np.float64))

    def test_spmatrix(self):
        A = np.matrix([[1,2,3],[4,5,6]])
        As = spmatrix(A)
        self.assertEqual(As.shape,A.shape)
        self.assertTrue(type(As) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(As.nnz,6)
        self.assertEqual(As.dtype,np.float64)
        self.assertEqual(As[0,0],A[0,0])
        B = sp.rand(10,10,format='csr')
        Bs = spmatrix(B)
        self.assertEqual(Bs.shape,B.shape)
        self.assertTrue(type(Bs) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(Bs.nnz,B.nnz)
        self.assertEqual(Bs.dtype,np.float64)
        Blil = B.tolil()
        for i in range(0,10):
            for j in range(0,10):
                self.assertEqual(Bs[i,j],Blil[i,j])
        Cs = spmatrix((50,50))
        self.assertEqual(Cs.shape,(50,50))
        self.assertTrue(type(Cs) is c.arrays.cvxpy_spmatrix)
        self.assertEqual(Cs.nnz,0)
        self.assertEqual(Cs.dtype,np.float64)
        for i in range(0,50):
            for j in range(0,50):
                self.assertEqual(Cs[i,j],0.)

    def test_equals(self):
        x = variable()
        a = parameter()
        c1 = equals(x,a)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(c1.right is a)

    def test_eq(self):
        x = variable()
        a = parameter()
        c1 = eq(x,a)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(c1.right is a)

    def test_less_equals(self):
        x = variable()
        a = parameter()
        c1 = less_equals(x,a)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.LESS_EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(c1.right is a)

    def test_leq(self):
        x = variable()
        a = parameter()
        c1 = leq(x,a)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.LESS_EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(c1.right is a)

    def test_greater_equals(self):
        x = variable()
        a = parameter()
        c1 = greater_equals(x,a)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.GREATER_EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(c1.right is a)

    def test_geq(self):
        x = variable()
        a = parameter()
        c1 = geq(x,a)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.GREATER_EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(c1.right is a)

    def test_minimize(self):
        x = variable()
        obj = x + 1
        f = minimize(obj)
        self.assertEqual(f[0],c.defs.MINIMIZE)
        self.assertTrue(f[1] is obj)
    
    def test_maximize(self):
        x = variable()
        obj = x + 1
        f = maximize(obj)
        self.assertEqual(f[0],c.defs.MAXIMIZE)
        self.assertTrue(f[1] is obj)

    def test_program(self):
        x = variable()
        p = program(minimize(x))
        self.assertTrue(type(p) is c.programs.cvxpy_program)
        self.assertTrue(p.objective is x)
        self.assertEqual(p.constraints,[])
        self.assertTrue(type(p.constraints) is c.constraints.cvxpy_list)
        self.assertTrue(type(p.formals) is c.constraints.cvxpy_list)
        self.assertEqual(p.formals,[])
        self.assertEqual(p.name,'prog')
        c1 = less_equals(x,1)
        p = program(maximize(x),[c1],[],name='myprog')
        self.assertTrue(p.objective is x)
        self.assertTrue(p.constraints[0] is c1)
        self.assertEqual(p.formals,[])
        self.assertEqual(p.name,'myprog')
        a = parameter()
        b = parameter()
        c2 = greater_equals(x,b+a)
        p = program(maximize(b),[c1,c2],[a,b])
        self.assertTrue(type(p) is c.programs.cvxpy_program)
        self.assertTrue(p.objective is b)
        self.assertTrue(p.constraints[0] is c1)
        self.assertTrue(p.constraints[1] is c2)
        self.assertTrue(p.parameters[0],a)
        self.assertTrue(p.parameters[1],b)
        p = program(maximize(1))
        self.assertEqual(p.objective.type,c.defs.CONSTANT)
        self.assertEqual(p.objective.value,1)
        self.assertEqual(p.objective.name,str(1))
        v = c.scalars.cvxpy_obj(c.defs.CONSTANT,4,str(4))
        p = program(minimize(v))
        self.assertTrue(type(p) is c.programs.cvxpy_program)
        self.assertTrue(p.objective is v)
        self.assertRaises(TypeError,program,minimize([1,2,3]))
        self.assertRaises(TypeError,program,minimize(variable(3,3)))
        self.assertRaises(TypeError,program,minimize(matrix([1])))
        y = variable(4,4)
        d = parameter(4,2)
        p = program(minimize(x+a+lambda_max(y)+sum(d)),
                    [less_equals(a,2)],
                    [x,a,y,d])
        self.assertTrue(type(p) is c.programs.cvxpy_program)
        self.assertTrue(p.formals[0] is x)
        self.assertTrue(p.formals[1] is a)
        self.assertTrue(p.formals[2] is y)
        self.assertTrue(p.formals[3] is d)
        self.assertRaises(TypeError,p,minimize(0),[],[1])
        self.assertRaises(TypeError,p,minimize(x),[equals(x,1)],
                          [x,a,y,[1,2,3]])

    def test_belongs(self):
        x = variable(4,4)
        y = variable()
        c1 = belongs(x,semidefinite_cone)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.BELONGS)
        self.assertTrue(c1.right is semidefinite_cone)
        self.assertTrue(c1.left is x)
        c2 = belongs(vstack((y,y,1,2)),second_order_cone)
        self.assertTrue(type(c2) is c.constraints.cvxpy_constr)
        self.assertEqual(c2.type,c.defs.BELONGS)
        self.assertTrue(c2.right is second_order_cone)
        c3 = belongs(vstack((y,y,1,2)),geo_mean_cone)
        self.assertTrue(type(c3) is c.constraints.cvxpy_constr)
        self.assertEqual(c3.type, c.defs.BELONGS)
        self.assertTrue(c3.right is geo_mean_cone)
        c4 = belongs(x+1,semidefinite_cone)
        self.assertTrue(type(c4) is c.constraints.cvxpy_constr)
        self.assertEqual(c4.type,c.defs.BELONGS)
        self.assertTrue(c4.right is semidefinite_cone)
        A = matrix([[1,2,3],[4,5,6],[4,4,4]])
        c5 = belongs(A,semidefinite_cone)
        self.assertTrue(type(c5) is c.constraints.cvxpy_constr)
        self.assertEqual(c5.type,c.defs.BELONGS)
        self.assertTrue(c5.right is semidefinite_cone)
        self.assertEqual(c5.left.type,c.defs.ARRAY)
        self.assertEqual(c5.left.shape,(3,3))
        for i in range(0,3,1):
            for j in range(0,3,1):
                self.assertEqual(c5.left[i,j],A[i,j])
        a = parameter(5,1)
        c6 = belongs(a,second_order_cone)
        self.assertTrue(type(c6) is c.constraints.cvxpy_constr)
        self.assertTrue(c6.right,second_order_cone)
        self.assertTrue(c6.left is a)
        self.assertEqual(c6.type,c.defs.BELONGS)
        self.assertRaises(TypeError,belongs,1,second_order_cone)
        self.assertRaises(TypeError,belongs,x,1)
        self.assertRaises(TypeError,belongs,x,x)
        self.assertRaises(TypeError,belongs,x,parameter())
        self.assertRaises(TypeError,belongs,a,[1,2,3])
        self.assertRaises(ValueError,belongs,variable(3,4),semidefinite_cone)
        self.assertRaises(ValueError,belongs,variable(4,1),exp_cone)
        self.assertRaises(ValueError,belongs,variable(3,2),second_order_cone)
        self.assertRaises(ValueError,belongs,variable(3,4),geo_mean_cone)
