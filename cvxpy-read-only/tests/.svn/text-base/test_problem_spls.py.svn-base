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
import cvxopt
import unittest
import scipy.sparse
import numpy as np
from cvxpy import *
import scipy.sparse as sp

# Test problem Sparse Least Squares
class TestProblemSPLS(unittest.TestCase):
    
    def test_spls(self):
        for i in range(0,2):
            np.random.seed(i)
            A = spmatrix(sp.rand(300,30,density=0.4))
            
            # make sure A has no empty columns
            A._create_col_based_rep()
            self.assertEqual(len([j for j in range(0,30) if len(A.cols[j]) == 0]),0)
            
            x = variable(30,1)
            b = rand(300,1)
            p = program(minimize(norm2(A*x-b))) # minimize || Ax-b ||
            p.solve(quiet=True)
            Ad = A.todense()
            AdTAd = Ad.T*Ad
            AdTb = Ad.T*b
            self.assertTrue(np.linalg.norm(AdTAd*x.value-AdTb,np.inf) < 1e-10)

        for i in range(0,2):
            np.random.seed(i+2)
            A = spmatrix(sp.rand(300,30,density=0.4))

            # make sure A has no empty columns
            A._create_col_based_rep()
            self.assertEqual(len([j for j in range(0,30) if len(A.cols[j]) == 0]),0)

            x = variable(30,1)
            b = rand(300,1)
            p = program(minimize(norm2(x.T*A.T-b.T))) # minimize || (Ax-b)^T ||
            p.solve(quiet=True)
            Ad = A.todense()
            AdTAd = Ad.T*Ad
            AdTb = Ad.T*b
            self.assertTrue(np.linalg.norm(AdTAd*x.value-AdTb,np.inf) < 1e-10)

        # example cvxopt conversions
        # create random scipy sparse matrix (format LIL) (can be any format)
        np.random.seed(5)
        A = scipy.sparse.rand(300,30,density=0.4,format='lil') 

        # convert scipy sparse matrix (format LIL) to scipy sparse matrix (format COO)
        Acoo = A.tocoo() # ("triplet" or "ijv" format)

        # construct cvxopt sparse matrix from scipy sparse matrix (format COO)
        size = Acoo.shape # get size
        v = Acoo.data # get data array
        i = Acoo.row # get row index array
        j = Acoo.col # get col index array
        Acvxopt = cvxopt.spmatrix(v,i,j,size) 

        # construct scipy sparse matrix (format COO) from cvxopt sparse matrix
        Ascipy = scipy.sparse.coo_matrix((list(Acvxopt.V),
                                          (list(Acvxopt.I),
                                           list(Acvxopt.J))),
                                         shape=Acvxopt.size)

        # construct cvxpy sparse matrix from scipy sparse matrix (format COO)
        # spmatrix accepts the same inputs as the function
        # scipy.sparse.lil_matrix
        Acvxpy = spmatrix(Ascipy)

        # validate conversions
        self.assertTrue(np.allclose(Acvxpy.todense(),A.todense())) 
        
        # make sure Acvxpy has no empty columns
        Acvxpy._create_col_based_rep()
        self.assertEqual(len([j for j in range(0,30) if len(Acvxpy.cols[j]) == 0]),0)

        # use cvxpy sparse matrix for solving least squares
        x = variable(30,1)
        b = rand(300,1)
        p = program(minimize(norm2(Acvxpy*x-b))) # minimize || Ax-b ||
        p.solve(quiet=True)

        # check that normal equations hold
        Ad = Acvxpy.todense()
        AdTAd = Ad.T*Ad
        AdTb = Ad.T*b
        self.assertTrue(np.linalg.norm(AdTAd*x.value-AdTb,np.inf) < 1e-10)
        
        
        
    
