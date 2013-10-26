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

# Test set log_norm_cdf_hypo
class TestSetLogNormCdfHypo(unittest.TestCase):

    rtol = 1e-6
    atol = 1e-7

    def test_log_norm_cdf_hypo(self):
        self.assertEqual(log_norm_cdf_hypo.type,c.defs.SET)
        self.assertEqual(log_norm_cdf_hypo.name,'log_norm_cdf_hypo')
        self.assertEqual(log_norm_cdf_hypo.expansion_type,c.defs.DIF)
        self.assertRaises(ValueError,belongs,vstack([1]),log_norm_cdf_hypo)
        self.assertRaises(ValueError,belongs,ones((1,3)),log_norm_cdf_hypo)
        self.assertRaises(ValueError,belongs,ones((5,3)),log_norm_cdf_hypo)
        self.assertRaises(ValueError,belongs,variable(3,1),log_norm_cdf_hypo)
        self.assertRaises(ValueError,belongs,variable(1,2),log_norm_cdf_hypo)

    def test_log_norm_cdf_hypo_in_prog(self):
        x = variable()
        p = program(maximize(x),[belongs(vstack((0.5,x)),log_norm_cdf_hypo)])
        self.assertTrue(np.allclose(p(),-0.368946,self.rtol,self.atol))
        t = variable()
        p = program(maximize(t+0.4),[belongs(vstack((x + 0.2,t)),
                                             log_norm_cdf_hypo),
                                     leq(x + 0.3, -0.2)])
        self.assertTrue(np.allclose(p(),-0.562102818,self.rtol,self.atol))
