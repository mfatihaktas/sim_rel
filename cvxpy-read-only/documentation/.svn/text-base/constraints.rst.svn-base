.. _constr:

***********
Constraints
***********
Constraints in CVXPY can be equalities, inequalities and set memberships. Equalities are constructed by using the interface function :func:`equals()<cvxpy.interface.equals>` or its abbreviation :func:`eq()<cvxpy.interface.eq>`. These functions take as arguments two expressions that are either of the same size, or that at least one is a scalar expression. When both arguments are scalar expressions, these functions return a :ref:`constraint object<constr_obj>`, otherwise they return a :ref:`list of constraints<constr_list_obj>`::

   >>> x = variable(name='x')
   >>> a = parameter(name='a')	

   >>> c = equals(2*x+a,10)				# Scalar == scalar
   >>> print c
   2*x + a == 10

   >>> c = eq(vstack((3*x,2*a)),5*x)			# Array == scalar
   >>> print c
   3*x == 5*x
   2*a == 5*x

Inequality constraints are constructed by using the interface functions :func:`greater_equals()<cvxpy.interface.greater_equals>`, :func:`less_equals()<cvxpy.interface.less_equals>` or their abbreviations :func:`geq()<cvxpy.interface.geq>` and :func:`leq()<cvxpy.interface.leq>`. These functions behave in a similar way to :func:`equals()<cvxpy.interface.equals>` and :func:`eq()<cvxpy.interface.eq>`::

   >>> z = variable(name='z')
   >>> b = parameter(2,2,name='b')
					 
   >>> c = less_equals(x+10,1)				# Scalar <= scalar
   >>> print c
   x + 10 <= 1

   >>> c = leq(b+z,(b+z).T)				# Array <= array
   >>> print c
   b[0,0] + z <= b[0,0] + z
   b[0,1] + z <= b[1,0] + z
   b[1,0] + z <= b[0,1] + z
   b[1,1] + z <= b[1,1] + z

   >>> c = geq(b[0,0]*z,ones((1,2)))			# Scalar >= matrix
   >>> print c
   b[0,0]*z >= 1.0
   b[0,0]*z >= 1.0

Finally, set memberships are constructed by using the interface function :func:`belongs()<cvxpy.interface.belongs>`. This function takes a :ref:`multidimensional object<multi_ref>` and a :ref:`set instance<set_ref>`, and returns a :ref:`constraint object<constr_obj>`::

   >>> w = variable(2,2,name='w')
   >>> c = belongs(w,semidefinite_cone)			#  Constrain w to be in the positive semidefinite cone
   >>> print c
   [[ w[0,0]  w[0,1] ]
    [ w[1,0]  w[1,1] ]]  in semidefinite_cone

   >>> x = variable(name='x')
   >>> a = parameter(name='a')
   >>> c = belongs(vstack((x,1,a)), exp_cone)		# Constrain (x,1,a) to be in the exponential cone
   >>> print c
   [[ x   ]
    [ 1.0 ]
    [ a   ]]  in exp_cone
