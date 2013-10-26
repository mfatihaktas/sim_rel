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

# Test constraints
class TestConstraints(unittest.TestCase):

    # cvxpy_constr
    def test_cvxpy_constr_init(self):
        f = c.constraints.cvxpy_constr(1,2,3)
        self.assertEqual(f.left,1)
        self.assertEqual(f.type,2)
        self.assertEqual(f.right,3)

    def test_cvxpy_constr_getattribute(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        b = c.scalars.cvxpy_scalar_param()
        c1 = greater_equals(x,1)
        self.assertTrue(type(c1.variables) is c.constraints.cvxpy_list)
        self.assertEqual(c1.variables,[x])
        c2 = less_equals(a,1)
        self.assertTrue(type(c2.variables) is c.constraints.cvxpy_list)
        self.assertEqual(c2.variables,[])
        c3 = equals(y,x)
        self.assertTrue(type(c3.variables) is c.constraints.cvxpy_list)
        self.assertEqual(len(c3.variables),2)
        self.assertEqual(set(c3.variables), set([x, y]))
        z = c.arrays.cvxpy_var(4,4)
        c4 = belongs(z,semidefinite_cone)
        self.assertTrue(type(c4.variables) is c.constraints.cvxpy_list)
        self.assertEqual(len(c4.variables),16)
        self.assertEqual(set(c4.variables),
                         set([z[i,j] for i in range(0,4,1)
                              for j in range(0,4,1)]))        
        c5 = greater_equals(a,1)
        self.assertTrue(type(c5.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(c5.parameters,[a])
        c6 = less_equals(1,x+y)
        self.assertTrue(type(c6.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(c6.parameters,[])
        c7 = equals(a,b)
        self.assertTrue(type(c7.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(len(c7.parameters),2)
        self.assertEqual(set(c7.parameters), set([a, b]))
        w = c.arrays.cvxpy_param(4,4)
        c8 = belongs(w,semidefinite_cone)
        self.assertTrue(type(c8.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(len(c8.parameters),16)
        self.assertEqual(set(c8.parameters),
                         set([w[i,j] for i in range(0,4,1)
                              for j in range(0,4,1)]))                
    
    def test_cvxpy_constr_str(self):
        x = c.scalars.cvxpy_scalar_var(name='x')
        a = c.scalars.cvxpy_scalar_param(name='a')
        c1 = greater_equals(x,a)
        self.assertEqual(str(c1),'x >= a')

    def test_cvxpy_constr_is_dcp(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        b = c.scalars.cvxpy_scalar_param()
        c1 = equals(x+a,b*y)
        self.assertTrue(c1.is_dcp())
        c2 = equals(2*x+4+a*b,7*(a*y-1)+1)
        self.assertTrue(c2.is_dcp())
        c3 = equals(square(x+a),y-b)
        self.assertFalse(c3.is_dcp())
        c4 = equals(1+a*b,sqrt(y+1))
        self.assertFalse(c4.is_dcp())
        c5 = less_equals(a*x,1+b)
        self.assertTrue(c5.is_dcp())
        c6 = less_equals(a*(x+1)+x, 10*y+b)
        self.assertTrue(c6.is_dcp())
        c7 = less_equals(sqrt(y-b),7)
        self.assertFalse(c7.is_dcp())
        c8 = less_equals(7*a+square(2*x+b*y),a+sqrt(2*(y+x)))
        self.assertTrue(c8.is_dcp())
        c9 = greater_equals(max(vstack((x,y,a,2))),x+b)
        self.assertFalse(c9.is_dcp())
        c10 = greater_equals(x+b*y,log_sum_exp(a*x+square(y)))
        self.assertTrue(c10.is_dcp())
        A = c.arrays.cvxpy_var(4,4)
        c11 = belongs(A,semidefinite_cone)
        self.assertTrue(c11.is_dcp())
        c12 = belongs(A+x,semidefinite_cone)
        self.assertTrue(c12.is_dcp())
        c13 = belongs(vstack((x,1,2,y)),second_order_cone)
        self.assertTrue(c13.is_dcp())
        c14 = belongs(square(A),semidefinite_cone)
        self.assertFalse(c14.is_dcp())
        c15 = belongs(sqrt(A),semidefinite_cone)
        self.assertFalse(c15.is_dcp())
        B = ones((3,3))
        c16 = belongs(B.T*B,semidefinite_cone)
        self.assertTrue(c16.is_dcp())
        c17 = equals(1,2)
        self.assertTrue(c17.is_dcp())
        c18 = less_equals(1,2)
        self.assertTrue(c18.is_dcp())
        c19 = greater_equals(1,2)
        self.assertTrue(c19.is_dcp())
        A = ones((2,3))
        A = A.T*A
        c20 = belongs(A,semidefinite_cone)
        self.assertTrue(c20.is_dcp())
        
    def test_cvxpy_constr_is_affine(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        c1 = equals(x,y+a)
        self.assertTrue(c1.is_affine())
        c2 = equals(1,1)
        self.assertTrue(c2.is_affine())
        c3 = equals(a*x,4)
        self.assertTrue(c3.is_affine())
        c4 = equals(4*a+2,y)
        self.assertTrue(c4.is_affine())
        c5 = equals(4,sqrt(y-a))
        self.assertFalse(c5.is_affine())
        c6 = equals(abs(x),a*4)
        self.assertFalse(c6.is_affine())
        c7 = less_equals(x+9*y-10*a,10+28*(a*x+20))
        self.assertTrue(c7.is_affine())
        c8 = less_equals(square(x+10),10+a)
        self.assertFalse(c8.is_affine())
        z = c.arrays.cvxpy_var(4,4)
        c9 = belongs(z,semidefinite_cone)
        self.assertFalse(c9.is_affine())
        A = ones((3,3))
        c10 = belongs(A,semidefinite_cone)
        self.assertFalse(c10.is_affine())
        c11 = greater_equals(square(x),a)
        self.assertFalse(c11.is_affine())
        c12 = greater_equals(huber(a*x+2*(y-1),2),x+y)
        self.assertFalse(c12.is_affine())
        c13 = greater_equals(x+a*y-10,4-x*100)
        self.assertTrue(c13.is_affine())
        
    # cvxpy_list
    def test_cvxpy_list_init(self):
        f = c.constraints.cvxpy_list([1,2,3])
        self.assertTrue(type(f) is c.constraints.cvxpy_list)

    def test_cvxpy_list_getattributes(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        z = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        b = c.scalars.cvxpy_scalar_param()
        d = c.scalars.cvxpy_scalar_param()
        l1 = less_equals(hstack((x,a,y,z)),b+d)
        self.assertTrue(type(l1) is c.constraints.cvxpy_list)
        self.assertTrue(type(l1.variables) is c.constraints.cvxpy_list)
        self.assertEqual(len(l1.variables),3)
        self.assertEqual(set(l1.variables), set([x, y, z]))
        self.assertTrue(type(l1.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(len(l1.parameters),3)
        self.assertEqual(set(l1.parameters), set([a, b, d]))
        l2 = greater_equals(hstack((x,b,y,z,a,x)),10+x+b)
        self.assertTrue(type(l2) is c.constraints.cvxpy_list)
        self.assertTrue(type(l2.variables) is c.constraints.cvxpy_list)
        self.assertEqual(len(l2.variables),3)
        self.assertEqual(set(l2.variables), set([x, y, z]))
        self.assertTrue(type(l2.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(len(l2.parameters),2)
        self.assertEqual(set(l2.parameters), set([a, b]))
        w = c.scalars.cvxpy_scalar_var()
        l3 = c.constraints.cvxpy_list([equals(x+y+huber(z+a+x,2),
                                              square(z+w))])
        self.assertTrue(type(l3.variables) is c.constraints.cvxpy_list)
        self.assertEqual(len(l3.variables),4)
        self.assertEqual(set(l3.variables), set([x, y, z, w]))
        self.assertTrue(type(l3.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(l3.parameters,[a])
        l4 = c.constraints.cvxpy_list([belongs(vstack((x,a,b*x,y,z)),
                                               second_order_cone)])
        self.assertTrue(type(l4) is c.constraints.cvxpy_list)
        self.assertEqual(len(l4.variables),3)
        self.assertEqual(set(l4.variables), set([x, y, z]))
        self.assertTrue(type(l4.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(len(l4.parameters),2)
        self.assertEqual(set(l4.parameters), set([a, b]))
        k = c.arrays.cvxpy_param(3,4)
        l5 = less_equals(k,d-b)
        self.assertTrue(type(l5) is c.constraints.cvxpy_list)
        self.assertTrue(type(l5.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(l5.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(l5.variables,[])
        self.assertEqual(len(l5.parameters),14)
        l6 = greater_equals(ones((4,5)),x + y)
        self.assertTrue(type(l6) is c.constraints.cvxpy_list)
        self.assertTrue(type(l6.variables) is c.constraints.cvxpy_list)
        self.assertTrue(type(l6.parameters) is c.constraints.cvxpy_list)
        self.assertEqual(l6.parameters,[])
        self.assertEqual(len(l6.variables),2)
        self.assertEqual(set(l6.variables), set([x, y]))
        
    def test_cvxpy_list_get_eq(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        z = c.arrays.cvxpy_var(4,4)
        c1 = less_equals(x,y)
        c2 = greater_equals(x,10)
        c3 = equals(10,20)
        c4 = equals(10,x+y*a)
        c5 = belongs(z,semidefinite_cone)
        l = c.constraints.cvxpy_list([c1,c2,c3,c4,c5])
        self.assertTrue(type(l._get_eq()) is c.constraints.cvxpy_list)
        self.assertEqual(len(l._get_eq()),2)
        self.assertTrue(l._get_eq()[0] is c3 or l._get_eq()[0] is c4)
        self.assertTrue(l._get_eq()[1] is c3 or l._get_eq()[1] is c4)

    def test_cvxpy_list_get_ineq_in(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        c1 = less_equals(x,y)
        c2 = greater_equals(x,10)
        c3 = equals(10,20)
        c4 = equals(10,x+y*a)
        c5 = belongs(vstack((x,y)),geo_mean_cone)
        l = c.constraints.cvxpy_list([c1,c2,c3,c4,c5])
        self.assertTrue(type(l._get_ineq_in()) is c.constraints.cvxpy_list)
        self.assertEqual(len(l._get_ineq_in()),3)
        for i in range(0,3,1):
            t = l._get_ineq_in()[i]
            self.assertTrue(t is c1 or t is c2 or t is c5)
            
    def test_cvxpy_list_is_dcp(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        Z = c.arrays.cvxpy_var(4,4)
        c1 = less_equals(square(x),1)
        c2 = greater_equals(square(x),1)
        c3 = less_equals(sqrt(x),1)
        c4 = greater_equals(sqrt(y),1)
        c5 = equals(x+5*y,10)
        c6 = less_equals(x,10)
        c7 = greater_equals(y,2)
        c8 = belongs(Z,semidefinite_cone)
        l1 = c.constraints.cvxpy_list([c1,c2,c3,c4,c5,
                                       c6,c7,c8])
        self.assertFalse(l1.is_dcp())
        l2 = c.constraints.cvxpy_list([])
        self.assertTrue(l2.is_dcp())
        l3 = c.constraints.cvxpy_list([c1,c4,c5,c6,c7,c8])
        self.assertTrue(l3.is_dcp())
        c9 = less_equals(vstack((x,x,x,y,1,2,3))+4,10)
        self.assertTrue(type(c9) is c.constraints.cvxpy_list)
        c10 = less_equals(norm2(vstack((1,2,3,x,x,y))),10+sqrt(y))
        c11 = belongs(Z+4+x,semidefinite_cone)
        l4 = c.constraints.cvxpy_list([c9,c10,c11])
        self.assertTrue(l4.is_dcp())
        l5 = l4 + c.constraints.cvxpy_list([equals(log(x+y),100)])
        self.assertFalse(l5.is_dcp())
        a = c.scalars.cvxpy_scalar_param()
        l6 = l4 + c.constraints.cvxpy_list([less_equals(a,1)])
        self.assertTrue(l6.is_dcp())
        l7 = l4 + c.constraints.cvxpy_list([greater_equals(log(x+y),
                                                           100)])
        self.assertTrue(l7.is_dcp())
        b = c.scalars.cvxpy_scalar_param(attribute='nonnegative')
        l8 = l4 + c.constraints.cvxpy_list([greater_equals(b*log(x+y),
                                                           100)])
        self.assertTrue(l8.is_dcp())
        l9 = l4 + c.constraints.cvxpy_list([greater_equals(a*log(x+y),
                                                           100)])
        self.assertFalse(l9.is_dcp())

    def test_cvxpy_list_is_affine(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        z = c.arrays.cvxpy_var(10,4)
        l1 = less_equals(z,x+7*y)
        self.assertTrue(type(l1) is c.constraints.cvxpy_list)
        self.assertEqual(len(l1),40)
        self.assertTrue(l1.is_affine())
        self.assertTrue(c.constraints.cvxpy_list([]).is_affine())
        l2 = c.constraints.cvxpy_list([less_equals(x,10),
                                       equals(x+hstack((5,6,x)),2)])
        self.assertTrue(type(l2) is c.constraints.cvxpy_list)
        self.assertTrue(l2.is_affine())
        l3 = l2 + c.constraints.cvxpy_list([less_equals(square(x),
                                                        sqrt(y))])
        self.assertFalse(l3.is_affine())

    def test_cvxpy_list_add_radd(self):
        x = c.scalars.cvxpy_scalar_var()
        y = c.scalars.cvxpy_scalar_var()
        a = c.scalars.cvxpy_scalar_param()
        c1 = less_equals(x,1)
        c2 = equals(a,y+a)
        c3 = belongs(vstack((a,a,x)),geo_mean_cone)
        l1 = c.constraints.cvxpy_list([c1,c2,c3])
        c4 = equals(x,y)
        l2 = c.constraints.cvxpy_list([c4])
        l3 = l1 + l2
        self.assertTrue(type(l3) is c.constraints.cvxpy_list)
        self.assertEqual(len(l3),4)
        self.assertTrue(l3[0] is c1)
        self.assertTrue(l3[1] is c2)
        self.assertTrue(l3[2] is c3)
        self.assertTrue(l3[3] is c4)
        l4 = l2 + [c1]
        self.assertTrue(type(l4) is c.constraints.cvxpy_list)
        self.assertEqual(len(l4),2)
        self.assertTrue(l4[0] is c4)
        self.assertTrue(l4[1] is c1)
        l5 = [c1] + l2
        self.assertTrue(type(l5) is c.constraints.cvxpy_list)
        self.assertEqual(len(l5),2)
        self.assertTrue(l5[0] is c1)
        self.assertTrue(l5[1] is c4)
        self.assertRaises(TypeError,l2.__add__,4)
        self.assertRaises(TypeError,l2.__radd__,4)

    def test_cvxpy_list_str(self):
        x = c.scalars.cvxpy_scalar_var(name='x')
        a = c.scalars.cvxpy_scalar_param(name='a')
        l1 = less_equals(vstack((x,a)),vstack((1,2)))
        self.assertTrue(type(l1) is c.constraints.cvxpy_list)
        self.assertEqual(str(l1),'x <= 1.0\na <= 2.0')

    # compare
    def test_compare(self):
        x = variable()
        X = variable(4,4)
        a = parameter()
        A = parameter(4,4)
        c1 = c.constraints.compare(x,c.defs.EQUALS,1)
        self.assertTrue(type(c1) is c.constraints.cvxpy_constr)
        self.assertEqual(c1.type,c.defs.EQUALS)
        self.assertTrue(c1.left is x)
        self.assertTrue(type(c1.right) is c.scalars.cvxpy_obj)
        self.assertEqual(c1.right.type,c.defs.CONSTANT)
        self.assertEqual(c1.right.value,1)
        self.assertEqual(c1.right.name,str(1))
        c2 = c.constraints.compare(1,c.defs.LESS_EQUALS,x)
        self.assertTrue(type(c2) is c.constraints.cvxpy_constr)
        self.assertEqual(c2.type,c.defs.LESS_EQUALS)
        self.assertTrue(c2.right is x)
        self.assertTrue(type(c2.left) is c.scalars.cvxpy_obj)
        self.assertEqual(c2.left.type,c.defs.CONSTANT)
        self.assertEqual(c2.left.value,1)
        self.assertEqual(c2.left.name,str(1))
        c3 = c.constraints.compare(a,c.defs.GREATER_EQUALS,x)
        self.assertTrue(type(c3) is c.constraints.cvxpy_constr)
        self.assertEqual(c3.type,c.defs.GREATER_EQUALS)
        self.assertTrue(c3.right is x)
        self.assertTrue(c3.left is a)
        c4 = c.constraints.compare(x,c.defs.EQUALS,a)
        self.assertTrue(type(c4) is c.constraints.cvxpy_constr)
        self.assertEqual(c4.type,c.defs.EQUALS)
        self.assertTrue(c4.right is a)
        self.assertTrue(c4.left is x)
        c5 = c.constraints.compare(a,c.defs.LESS_EQUALS,1)
        self.assertTrue(type(c5) is c.constraints.cvxpy_constr)
        self.assertEqual(c5.type,c.defs.LESS_EQUALS)
        self.assertTrue(c5.left is a)
        self.assertTrue(type(c5.right) is c.scalars.cvxpy_obj)
        self.assertEqual(c5.right.type,c.defs.CONSTANT)
        self.assertEqual(c5.right.value,1)
        self.assertEqual(c5.right.name,str(1))
        c6 = c.constraints.compare(1,c.defs.GREATER_EQUALS,a)
        self.assertTrue(type(c6) is c.constraints.cvxpy_constr)
        self.assertEqual(c6.type,c.defs.GREATER_EQUALS)
        self.assertTrue(c6.right is a)
        self.assertTrue(type(c6.left) is c.scalars.cvxpy_obj)
        self.assertEqual(c6.left.type,c.defs.CONSTANT)
        self.assertEqual(c6.left.value,1)
        self.assertEqual(c6.left.name,str(1))
        c7 = c.constraints.compare(1,c.defs.EQUALS,2)
        self.assertTrue(type(c7) is c.constraints.cvxpy_constr)
        self.assertEqual(c7.type,c.defs.EQUALS)
        self.assertTrue(type(c7.left) is c.scalars.cvxpy_obj)
        self.assertEqual(c7.left.type,c.defs.CONSTANT)
        self.assertEqual(c7.left.value,1)
        self.assertEqual(c7.left.name,str(1))
        self.assertTrue(type(c7.right) is c.scalars.cvxpy_obj)
        self.assertEqual(c7.right.type,c.defs.CONSTANT)
        self.assertEqual(c7.right.value,2)
        self.assertEqual(c7.right.name,str(2))
        c8 = c.constraints.compare(x+2*a,c.defs.LESS_EQUALS,1)
        self.assertTrue(type(c8) is c.constraints.cvxpy_constr)
        self.assertEqual(c8.type,c.defs.LESS_EQUALS)
        self.assertEqual(c8.left.type,c.defs.TREE)
        self.assertEqual(c8.right.type,c.defs.CONSTANT)
        self.assertEqual(c8.right.value,1)
        self.assertEqual(c8.right.name,str(1))
        c9 = c.constraints.compare(a,c.defs.GREATER_EQUALS,x+2*x)
        self.assertTrue(type(c9) is c.constraints.cvxpy_constr)
        self.assertEqual(c9.type,c.defs.GREATER_EQUALS)
        self.assertEqual(c9.right.type,c.defs.TREE)
        self.assertTrue(c9.left is a)
        c10 = c.constraints.compare(X,c.defs.EQUALS,10)
        self.assertTrue(type(c10) is c.constraints.cvxpy_list)
        self.assertTrue(all(list(map(lambda g: g.type == c.defs.EQUALS,c10))))
        self.assertEqual(len(c10), X.shape[0]*X.shape[1])
        for i in range(0,X.shape[0],1):
            for j in range(0,X.shape[1],1):
                self.assertTrue(c10[i*X.shape[1]+j].left is X[i,j])
                self.assertEqual(c10[i*X.shape[1]+j].right.type,
                                 c.defs.CONSTANT)
                self.assertEqual(c10[i*X.shape[1]+j].right.value,10)
                self.assertEqual(c10[i*X.shape[1]+j].right.type,
                                 c.defs.CONSTANT)
        c11 = c.constraints.compare(A,c.defs.LESS_EQUALS,x)
        self.assertTrue(type(c11) is c.constraints.cvxpy_list)
        self.assertTrue(all(list(map(lambda g: g.type == c.defs.LESS_EQUALS,
                                c11))))
        self.assertEqual(len(c11),A.shape[0]*A.shape[1])
        for i in range(0,A.shape[0],1):
            for j in range(0,A.shape[1],1):
                self.assertTrue(c11[i*A.shape[1]+j].left is A[i,j])
                self.assertTrue(c11[i*A.shape[1]+j].right is x)
        c12 = c.constraints.compare(a,c.defs.GREATER_EQUALS,A+X)
        self.assertTrue(type(c12) is c.constraints.cvxpy_list)
        self.assertTrue(all(list(map(lambda g: g.type == c.defs.GREATER_EQUALS,
                                c12))))
        self.assertEqual(len(c12),A.shape[0]*A.shape[1])
        for i in range(0,A.shape[0],1):
            for j in range(0,A.shape[1],1):
                self.assertEqual(c12[i*A.shape[1]+j].right.type,c.defs.TREE)
                self.assertTrue(c12[i*A.shape[1]+j].right.children[0] 
                                is A[i,j])
                self.assertTrue(c12[i*A.shape[1]+j].right.children[1]
                                is X[i,j])
                self.assertTrue(c12[i*A.shape[1]+j].left is a)
        B = ones((4,4))
        c13 = c.constraints.compare(B,c.defs.EQUALS,X)
        self.assertTrue(type(c13) is c.constraints.cvxpy_list)
        self.assertTrue(all(list(map(lambda g: g.type == c.defs.EQUALS,
                                c13))))
        self.assertEqual(len(c13),X.shape[0]*X.shape[1])
        for i in range(0,X.shape[0],1):
            for j in range(0,X.shape[1],1):
                self.assertTrue(c13[i*X.shape[1]+j].right is X[i,j])
                self.assertEqual(c13[i*X.shape[1]+j].left.type,
                                 c.defs.CONSTANT)
                self.assertEqual(c13[i*X.shape[1]+j].left.value,B[i,j])

        c14 = c.constraints.compare(B,c.defs.EQUALS,2)
        self.assertTrue(type(c14) is c.constraints.cvxpy_list)
        self.assertTrue(all(list(map(lambda g: g.type == c.defs.EQUALS,
                                c14))))
        self.assertEqual(len(c14),B.shape[0]*B.shape[1])
        for i in range(0,B.shape[0],1):
            for j in range(0,B.shape[1],1):
                self.assertEqual(c14[i*B.shape[1]+j].right.type,
                                 c.defs.CONSTANT)
                self.assertEqual(c14[i*B.shape[1]+j].right.value,2)
                self.assertEqual(c14[i*B.shape[1]+j].left.type,
                                 c.defs.CONSTANT)
                self.assertEqual(c14[i*B.shape[1]+j].left.value,B[i,j])
                
        self.assertRaises(ValueError,equals,A,ones((4,5)))
        self.assertRaises(TypeError,less_equals,A,[1,2,3])
        self.assertRaises(TypeError,equals,np.ones((4,3)),x)
        self.assertRaises(TypeError,greater_equals,
                          np.matrix([2,3,4]),a)
