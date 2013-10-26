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

# Test set geo_mean_cone
class TestSetGeoMeanCone(unittest.TestCase):

    rtol = 1e-5
    atol = 1e-6

    def test_geo_mean_cone(self):
        self.assertEqual(geo_mean_cone.type,c.defs.SET)
        self.assertEqual(geo_mean_cone.name,'geo_mean_cone')
        self.assertRaises(ValueError,belongs,vstack([1]),geo_mean_cone)
        self.assertRaises(ValueError,belongs,ones((1,3)),geo_mean_cone)
        self.assertRaises(ValueError,belongs,ones((5,3)),geo_mean_cone)

    def test_geo_mean_cone_in_prog(self):
        x = variable()
        p = program(minimize(x),[belongs(vstack((1,x,2)),geo_mean_cone)])
        self.assertTrue(np.allclose(p(),4,self.rtol,self.atol))
        p = program(minimize(x),[belongs(vstack((1,x+2,2)),
                                         geo_mean_cone)])
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))
        p = program(maximize(x),[belongs(vstack((1,4,x)),geo_mean_cone)])
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))
        p = program(minimize(x),[geq(x,2),belongs(vstack((1,10,3)),
                                                  geo_mean_cone)])
        self.assertTrue(np.allclose(p(),2,self.rtol,self.atol))
        p = program(minimize(0),[belongs(vstack((2,3,4,2.6)),geo_mean_cone)])
        self.assertEqual(p(),0)
        p = program(maximize(0),[belongs(vstack((2,3,4,2.6)),geo_mean_cone)])
        self.assertEqual(p(),0)
