.. _partial:

**********************
New modeling functions
**********************
In the previous section we saw that optimization programs in CVXPY are functions. We can specify a list of formals at construction and then call the program with the appropriate arguments. The interesing part is that these arguments can be more than just numbers or matrices. They can be other CVXPY objects such as variables, parameters and expressions. In fact, the functions obtained with this method can be used in the descriptions of other optimization programs.

To illustrate these ideas, the following sequence of examples shows how to construct a new modeling function. Consider the following program::

   >>> t = variable()
   >>> x = variable()
   >>> p = program(maximize(t),[geq(x,square(t))],[x])			# Create program and define list of formals

This program takes a single argument and computes its square root::

   >>> p(4)
   2.00000
   
   >>> p(9)
   3.00000

We can also call it with :ref:`scalar objects<scalar_ref>`, in which case it returns :ref:`expression trees<tree_obj>`::
   
   >>> p(variable())							# Returns expression tree
   <cvxpy.scalars.cvxpy_tree object at 0x14ed590>			
  
   >>> p(parameter()*variable()+1)					# Returns expression tree
   <cvxpy.scalars.cvxpy_tree object at 0x14f3e10>

.. note:: If a parameter is used in the list of formals, the corresponding argument in a program call cannot contain any variables. To call a program with a non-numeric argument, the corresponding formal must be a variable.

As in the case of variables and parameters, we can specify a name for the program, which defines how it appears when printed within some expression. This can be done at construction by passing :func:`program()<cvxpy.interface.program>` an additional argument or by modifying the program's ``name`` field::

   >>> p.name = 'my_sqrt'   		       	   	     	      	# Specify program (function) name

   >>> c = parameter(name='c')
   >>> z = variable(name='z')

   >>> print p(c*z+1)							# Name is used when expression is printed
   my_sqrt(c*z + 1)
       
Now, to encapsulate the implementation of our new square root function, we can enclose it inside a ``def`` statement as follows::

   >>> def my_sqrt(x):
   ...     t = variable()
   ...     y = variable()
   ...     p = program(maximize(t),
   ...                 [geq(y,square(t))],		# Encapsulate function implementation in def statement
   ...                 [y],
   ...                 name='my_sqrt')
   ...     return p(x)

   >>> my_sqrt(4)
   2.0000
  
   >>> print my_sqrt(c*z+1)
   my_sqrt(c*z + 1)

We are done! We have created a new square root function which we can now use to model new optimization problems. This is illustrated in the following example::

   >>> w = variable()

   >>> new_p = program(maximize(my_sqrt(w)),		# Create a new program using our new function
   ...                 [leq(w,100)])

   >>> new_p.solve(quiet=True)				# Solve new program
   10.0000

   >>> w.value						# Get optimal point
   100.000

.. note::
   Every modeling function provided by CVXPY is in fact constructed with the same method that we have used here for constructing a square root function. In other words, every modeling function provided by CVXPY is just a program encapsulated in a definition statement.
