.. _expressions:

***********
Expressions
***********
:ref:`Variables<variables>`, :ref:`parameter<parameters>`, :ref:`functions<functions>`, :ref:`matrices<matrices>` and numbers can be combined to form expressions by using the operations of addition, subtraction, negation, multiplication and function composition::

   >>> x = variable(name='x')			
   >>> y = variable(name='y')
   >>> print x + 2*y					# Addition and multiplication
   x + 2*y

   >>> print sqrt(exp(x-y))				# Function composition
   sqrt(exp(x + -1.0*y))

   >>> a = parameter(2,2,name='a')
   >>> print 2*log(a)+x					# Array-scalar addition
   [[ 2*log(a[0,0]) + x  2*log(a[0,1]) + x ]
    [ 2*log(a[1,0]) + x  2*log(a[1,1]) + x ]]

.. note:: CVXPY does not allow multiplying two expressions when both of these contain optimization variables.

The variables and parameters of an expression can be extracted by accessing its ``variables`` and ``parameters`` fields::

    >>> x = variable(name='x')
    >>> y = variable(2,2,name='y')			# Create variables and parameters
    >>> b = parameter(1,2,name='b')		

    >>> t = max(hstack((x,diag(y).T,4)))+sum(b)		# Create an expression

    >>> print t.variables				# Extract variables
    x
    y[0,0]
    y[1,1]
    
    >>> print t.parameters				# Extract parameters
    b[0,0]
    b[0,1]		

When the variables and parameters of an expression contain numeric values, the value of the expression can be computed by accessing its ``value`` field. For the following example, suppose that the value of the scalar variable ``x`` has been assigned to ``5`` by CVXPY and that ``b`` is a 1x2 parameter::

   >>> x.value	       		     	       	   	# x has value 5 
   5

   >>> b.value = matrix([5,10])				# Set the value of b with a 1x2 matrix

   >>> b.value
   matrix([[  5.,  10.]])

   >>> t = square(x)-4*norm2(b.T)			# Construct expression
   
   >>> t.value						# Compute the value of the expression
   -19.7214

.. _utility:

Utility functions
=================

CVXPY provides utility functions that can be used for creating more complex expressions and for generating data. Many of these functions have been adapted from `Numpy <http://numpy.scipy.org/>`_ to handle :ref:`scalar objects<scalar_ref>` or :ref:`multidimensional objects<multi_ref>`, or to return an appropriate matrix type. The following table shows the utility functions that are currently available in CVXPY:

+-------------------------------------+-------------------------------------+
|Utility Functions		    					    |
+=====================================+=====================================+
|:func:`diag()<cvxpy.utils.diag>`     |:func:`seed()<cvxpy.utils.seed>`	    |
+-------------------------------------+-------------------------------------+
|:func:`eye()<cvxpy.utils.eye>`	      |:func:`sqrtm()<cvxpy.utils.sqrtm>`   |
+-------------------------------------+-------------------------------------+
|:func:`hstack()<cvxpy.utils.hstack>` |:func:`sum()<cvxpy.utils.sum>`       |
+-------------------------------------+-------------------------------------+
|:func:`ones()<cvxpy.utils.ones>`     |:func:`trace()<cvxpy.utils.trace>`   |
+-------------------------------------+-------------------------------------+
|:func:`rand()<cvxpy.utils.rand>`     |:func:`vstack()<cvxpy.utils.vstack>` |
+-------------------------------------+-------------------------------------+
|:func:`randn()<cvxpy.utils.randn>`   |:func:`zeros()<cvxpy.utils.zeros>`   |		
+-------------------------------------+-------------------------------------+

Please see the :ref:`Reference<ref>` section for more information about specific utility functions.
