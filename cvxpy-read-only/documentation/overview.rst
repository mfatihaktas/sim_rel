.. _overview:

********
Overview
********

CVXPY is a **free** software package for modeling convex optimization problems in `Python <http://www.python.org>`_. It provides a modeling framework that allows users to easily describe optimization problems in a natural mathematical form and solve them. For example, suppose we want to solve a problem of the form

.. math::
   :nowrap:   

   \begin{center}
   \begin{eqnarray*}
	&\mbox{minimize}	&||Ax-b||_2 \\
	&\mbox{subject to}	&||Gx-h||_1 \leq \alpha \\
	&                       &x_i \geq 1, \quad i \in [n],
   \end{eqnarray*}
   \end{center}

where :math:`x \in \mathbb{R}^n` is the optimization variable, :math:`A \in \mathbb{R}^{m \times n}`, :math:`b \in \mathbb{R}^m`, :math:`G \in \mathbb{R}^{p \times n}`, :math:`h \in \mathbb{R}^p` and :math:`\alpha \geq 0`. Then, with CVXPY, we can solve an instance of this problem as follows::

   >>> from cvxpy import *	    		        # Import cvxpy
 
   >>> A = randn(50,5)					# Generate problem data
   >>> b = 20*randn(50,1)
   >>> G = randn(10,5)
   >>> h = 5*randn(10,1)
   >>> alpha = 60

   >>> x = variable(5,1)				# Create optimization variable

   >>> p = program(minimize(norm2(A*x-b)),		# Create problem instance
   ...             [leq(norm1(G*x-h),alpha),
   ...              geq(x,1)])
   
   >>> p.solve(quiet=True)				# Get optimal value
   138.069

   >>> x.value						# Get optimal point
   matrix([[ 1.00000],
           [ 1.00000],
           [ 1.92943],
           [ 1.00000],
           [ 1.11038]])

CVXPY accepts optimization problems that follow the rules of Disciplined Convex Programming (DCP), like `CVX <http://cvxr.com/cvx/>`_, and uses `CVXOPT <http://abel.ee.ucla.edu/cvxopt/>`_ to solve them.

