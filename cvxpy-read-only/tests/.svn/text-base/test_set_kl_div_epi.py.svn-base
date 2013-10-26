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

# Test set kl_div_epi
class TestSetKlDivEpi(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_kl_div_epi(self):
        self.assertEqual(log_norm_cdf_hypo.type,c.defs.SET)
        self.assertEqual(kl_div_epi.name,'kl_div_epi')
        self.assertEqual(kl_div_epi.expansion_type,c.defs.DIF)
        self.assertRaises(ValueError,belongs,vstack([1]),kl_div_epi)
        self.assertRaises(ValueError,belongs,ones((1,3)),kl_div_epi)
        self.assertRaises(ValueError,belongs,ones((5,3)),kl_div_epi)
        self.assertRaises(ValueError,belongs,variable(1,2),kl_div_epi)
        self.assertRaises(ValueError,belongs,variable(2,1),kl_div_epi)
        self.assertRaises(ValueError,belongs,variable(6,1),kl_div_epi)

    def test_kl_div_epi_in_prog(self):
        x = variable(3,1)
        y = variable(3,1)
        t = variable()
        p = program(minimize(t),
                    [belongs(vstack((x,y,t)),kl_div_epi),
                     leq(x,0.2),geq(y,0.4)])
        self.assertTrue(np.allclose(p(),0.1841116,self.rtol,self.atol))
        self.assertTrue(np.allclose(x.value,0.2*ones((3,1)),
                                    self.rtol,self.atol))
        self.assertTrue(np.allclose(y.value,0.4*ones((3,1)),
                                    self.rtol,self.atol))
        seed(1)
        x = rand(5,1)
        y = rand(5,1)
        p = program(minimize(t),[belongs(vstack((x,y,t)),kl_div_epi)])
        temp = 0
        for i in range(0,5,1):
            temp += x[i,0]*np.log(x[i,0]/y[i,0]) - x[i,0] + y[i,0]
        self.assertTrue(np.allclose(p(),temp,self.rtol,self.atol))
        x = variable(3,1)
        y = variable(3,1)
        p = program(maximize(sum(x-y)),
                    [belongs(vstack((x,0.3,0.05,y,0.1)),kl_div_epi),
                     leq(x,1)])
        self.assertTrue(np.allclose(p(),0.37342423,self.rtol,self.atol))
        p = program(minimize(t),[geq(t,3),
                                 belongs(vstack((1,2,3,4,5,6,3)),
                                         kl_div_epi)])
        self.assertRaises(ValueError,p)
        p = program(minimize(t),[geq(t,3),
                                 belongs(vstack((1,2,3,4,5,6,4)),
                                         kl_div_epi)])
        self.assertTrue(np.allclose(p(),3,self.rtol,self.atol))
