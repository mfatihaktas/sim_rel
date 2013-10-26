.. _components:

**********
Components
**********
This section describes the main modeling objects provided by CVXPY.

.. _variables:

Variables
=========
In CVXPY, optimization variables can be created by using the function :func:`variable()<cvxpy.interface.variable>`. This function can take as arguments the variable's ``shape``, ``structure`` and ``name``, and returns a :ref:`scalar variable<scalar_var_obj>` or a :ref:`multidimensional variable<multi_var_obj>`. Specifying a variable's name is useful when one needs to display the variable. If a name is not specified, a default letter followed by the contents of a variable counter is used::
   
   >>> from cvxpy import *				# Import cvxpy

   >>> x = variable()	 				# Create scalar variables
   >>> y = variable()			

   >>> print x,y					# Variables get default names
   v0 v1

   >>> x = variable(name='x')				# Create scalar variable and specify name
   >>> print x
   x
   
Multidimensional variables are arrays of scalar variables and behave in a way similar to matrices in `Numpy <http://numpy.scipy.org/>`_. In particular, they support the operations of slicing and taking transposes::

   >>> y = variable(3,1,name='y')      	   		# Create multidimensional variable  
   >>> print y
   [[ y[0,0] ]
    [ y[1,0] ]
    [ y[2,0] ]]     
    
   >>> print y.T					# Transpose operation
   [[ y[0,0]  y[1,0]  y[2,0] ]] 

   >>> z = variable(4,4,name='z')
   >>> print z[0:2,:]					# Slicing operation
   [[ z[0,0]  z[0,1]  z[0,2]  z[0,3] ]
    [ z[1,0]  z[1,1]  z[1,2]  z[1,3] ]] 
    
Multidimensional variables can also be structured. Valid structures are given by the strings :samp:`'lower_triangular'`, :samp:`'upper_triangular'` and :samp:`'symmetric'`::

   >>> x = variable(4,4,structure='lower_triangular',name='x')          # Create lower triangular variable
   >>> print x
   [[ x[0,0]  0.0     0.0     0.0    ]
    [ x[1,0]  x[1,1]  0.0     0.0    ]
    [ x[2,0]  x[2,1]  x[2,2]  0.0    ]
    [ x[3,0]  x[3,1]  x[3,2]  x[3,3] ]] 

   >>> y = variable(3,3,structure='symmetric',name='y')			# Create symmetric variable
   >>> print y
   [[ y[0,0]  y[1,0]  y[2,0] ]
    [ y[1,0]  y[1,1]  y[2,1] ]
    [ y[2,0]  y[2,1]  y[2,2] ]]

A scalar variable can also hold a numeric value. This value is ``NaN`` after instantiation and is assigned a number by CVXPY after an optimization problem involving the variable is solved. Once a value has been assigned to a variable, it can be retrieved by accessing the variables's ``value`` field. In the case of a multidimensional variable, its value is a :ref:`matrix<matrix_obj>` formed with the values of its scalar variable entries. For the following example, assume that ``x`` is a scalar variable, ``y`` is a 2x2 variable, and that numeric values have already been assigned to all scalar variables::

   >>> x.value	       	   	          	      	        # The value of x is a number
   5

   >>> map(lambda x: x.value,[y[0,0],y[0,1],y[1,0],y[1,1]])	# The values of y[0,0],y[0,1],y[1,0],y[1,1] are numbers
   [1, 0, 0, 2]

   >>> print y							# y is composed of y[0,0],y[0,1],y[1,0],y[1,1]
   [[ y[0,0]  y[0,1] ]
    [ y[1,0]  y[1,1] ]] 
		
   >>> y.value							# The value of y is a matrix
   matrix([[ 1.,  0.],
           [ 0.,  2.]])
      
.. _parameters:

Parameters
==========
Parameters are modeling objects that can be used for creating families of optimization problems. In CVXPY, parameters are defined in a way similar to variables, but by using the function :func:`parameter()<cvxpy.interface.parameter>`. This function can take as arguments the parameter's ``shape``, ``attribute`` and ``name``, and returns a :ref:`scalar parameter<scalar_param_obj>` or a :ref:`multidimensional parameter<multi_param_obj>` . As in the case of :ref:`variables<variables>`, if a parameter's name is not specified at construction, a default letter followed by the contents of a parameter counter is used. Also, multidimensional parameters are arrays of scalar parameters and behave in a way similar to matrices in `Numpy <http://numpy.scipy.org/>`_::
   
   >>> b = parameter(3,1,name='b')			# Create multidimensional parameter
   >>> print b
   [[ b[0,0] ]
    [ b[1,0] ]
    [ b[2,0] ]]
  
   >>> print b.T[0,0:3:2]				# Transpose and slicing operations
   [[ b[0,0]  b[2,0] ]] 

It is also possible to include sign information in a parameter by setting its ``attribute`` field. Valid attributes are given by the strings :samp:`'nonnegative'` and :samp:`'nonpositive'`. The use of this feature is covered in the :ref:`Disciplined Convex Programming<dcp>` section.

A parameter's value can be specified by setting its ``value`` field, which is initialized to ``NaN`` during instantiation. This value must be a number for scalar parameters and a :ref:`matrix<matrix_obj>` of appropriate shape for multidimensional parameters. If a parameter has a special attribute, *e.g.* :samp:`'nonnegative'`, the assigned value must be consistent with such attribute::

   >>> a = parameter()
   >>> a.value						# The parameter's value is initialized with NaN
   nan					
   
   >>> a.value = 10					# Set the value of a scalar parameter with a number
   >>> a.value 	 		  
   10
   
   >>> b = parameter(3,2)		
   >>> b.value = ones((3,2))				# Set the value of a multidimensional parameter with a matrix
   >>> b.value
   matrix([[ 1.,  1.],
           [ 1.,  1.],
           [ 1.,  1.]])
					
   >>> b[0,1].value					# The entries of a multidimensional parameter are set accordingly
   1.0

.. _matrices:

Matrices
========
Matrices in CVXPY are created by using the function :func:`matrix()<cvxpy.interface.matrix>`. These matrices are of type :class:`cvxpy_matrix<cvxpy.arrays.cvxpy_matrix>`, a subclass of `Numpy <http://numpy.scipy.org/>`_ matrices, so they behave in a similar way::

     >>> A = matrix([[1,2,3],[4,5,6]])     	    	# Create a matrix froma a list of lists
     >>> A
     matrix([[ 1.,  2.,  3.],
             [ 4.,  5.,  6.]])

     >>> A.T						# Transpose operation
     matrix([[ 1.,  4.],
             [ 2.,  5.],
	     [ 3.,  6.]])
	       
     >>> A[:,1]						# Slicing operation
     matrix([[ 2.],
             [ 5.]])

     >>> B = matrix('2,0,0;0,4,0;0,0,5')		# Create a matrix from a string
     >>> B
     matrix([[ 2.,  0.,  0.],
       	     [ 0.,  4.,  0.],
	     [ 0.,  0.,  5.]])

     >>> B.I						# Inverse operation
     matrix([[ 0.5 ,  0.  ,  0.  ],
             [ 0.  ,  0.25,  0.  ],
	     [ 0.  ,  0.  ,  0.2 ]])

.. note::
   All matrices used for describing optimization problems in CVXPY must be of type :class:`cvxpy_matrix<cvxpy.arrays.cvxpy_matrix>`. Other types of matrices do not combine correctly with variables and other CVXPY objects when forming :ref:`expressions <expressions>`. 

.. _functions:

Functions
=========
CVXPY provides a library of modeling functions that can be combined with other CVXPY objects to form :ref:`expressions <expressions>`. Each of these functions is in fact either convex or concave. Currently, the available functions are the following:

=============================================== =================================================== =====================================================
..						              Library of Functions	     	    ..
=============================================== =================================================== =====================================================
:func:`abs<cvxpy.functions.abs>`	        :func:`log<cvxpy.functions.log>`                    :func:`nuclear_norm<cvxpy.functions.nuclear_norm>`
:func:`det_rootn<cvxpy.functions.det_rootn>`    :func:`log_norm_cdf<cvxpy.functions.log_norm_cdf>`  :func:`power_abs<cvxpy.functions.power_abs>` 
      :func:`exp<cvxpy.functions.exp>`	        :func:`log_sum_exp<cvxpy.functions.log_sum_exp>`    :func:`power_p<cvxpy.functions.power_p>`
:func:`geo_mean<cvxpy.functions.geo_mean>`      :func:`max<cvxpy.functions.max>`                    :func:`power_pos<cvxpy.functions.power_pos>`
:func:`huber<cvxpy.functions.huber>`	        :func:`min<cvxpy.functions.min>`                    :func:`quad_form<cvxpy.functions.quad_form>`
:func:`kl_div<cvxpy.functions.kl_div>` 	        :func:`norm1<cvxpy.functions.norm1>` 	            :func:`quad_over_lin<cvxpy.functions.quad_over_lin>`
:func:`lambda_max<cvxpy.functions.lambda_max>`  :func:`norm2<cvxpy.functions.norm2>`      	    :func:`sqrt<cvxpy.functions.sqrt>`
:func:`lambda_min<cvxpy.functions.lambda_min>`  :func:`norm_inf<cvxpy.functions.norm_inf>`          :func:`square<cvxpy.functions.square>` 
=============================================== =================================================== =====================================================

If a function is called with numeric arguments, it returns a number or a :ref:`matrix<matrix_obj>`. Otherwise, it returns an :ref:`expression tree<tree_obj>` or an :ref:`expression array<array_obj>`::

   >>> x = variable(name='x')  	       		          
   >>> abs(x)						# Returns an expression tree
   <cvxpy.scalars.cvxpy_tree object at 0x25397d0>
	       	      	    
   >>> print abs(x)
   abs(x)

   >>> abs(-5)						# Returns a number
   5.

   >>> abs(matrix([1,-1,-2]))				# Returns a matrix
   matrix([[ 1., 1., 2.]])

   >>> y = variable(2,2,name='y')		
   >>> square(y)					# Returns an expression array
   <cvxpy.arrays.cvxpy_array object at 0x25394d0>
   
   >>> print square(y)						
   [[ square(y[0,0])  square(y[0,1]) ]	
    [ square(y[1,0])  square(y[1,1]) ]] 

.. _sets:

Sets
====
CVXPY also provides a library of sets that can be used for forming constraints. Currently, the available sets are the following:

+---------------------------------------------------------+
|Library of Sets					  |
+=========================================================+
|:data:`exp_cone<cvxpy.sets.exp_cone>`			  |
+---------------------------------------------------------+
|:data:`geo_mean_cone<cvxpy.sets.geo_mean_cone>`	  |
+---------------------------------------------------------+
|:data:`kl_div_epi<cvxpy.sets.kl_div_epi>`                |
+---------------------------------------------------------+
|:data:`log_norm_cdf_hypo<cvxpy.sets.log_norm_cdf_hypo>`  |
+---------------------------------------------------------+
|:data:`power_pos_epi<cvxpy.sets.power_pos_epi>`          |
+---------------------------------------------------------+
|:data:`second_order_cone<cvxpy.sets.second_order_cone>`  |
+---------------------------------------------------------+
|:data:`semidefinite_cone<cvxpy.sets.semidefinite_cone>`  |
+---------------------------------------------------------+

Please refer to the :ref:`Constraints<constr>` section for a discussion on how to use sets.
