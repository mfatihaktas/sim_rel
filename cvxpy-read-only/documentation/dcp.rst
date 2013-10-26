.. _dcp:

******************************
Disciplined Convex Programming
******************************
Disciplined Convex Programming is a modeling methodology that imposes a set of rules for constructing convex optimization programs. The details can be found `here <http://stanford.edu/~boyd/papers/disc_cvx_prog.html>`_ . As mentioned before, CVXPY will only attempt to solve a program if this satisfies DCP rules. To determine if program is DCP compliant, or to determine if an expression is affine, satisfies the the rules for convexity or satisfies the rules for concavity, one can use the methods ``is_dcp()``, ``is_affine()``, ``is_convex()`` and ``is_concave()``::

   >>> x = variable()
   >>> y = variable()							# Create some variables and a parameter
   >>> a = parameter()     

   >>> (x+a*y).is_affine()						# Check if expression is affine
   True
	    
   >>> square(x+a*y).is_convex()					# Check if expression follows convexity rules
   True
	    
   >>> log(sqrt(x+2*y+10+a)).is_concave()				# Check if expression follows concavity rules
   True
	    
   >>> w = variable(3,1)
   >>> norm2(w+2*a).is_convex()
   True
	    
   >>> leq(norm2(w-a),sqrt(y)).is_dcp()					# Check if inequality constraint is DCP-compliant
   True
	    
   >>> geq(norm2(a*w+1),sqrt(y)).is_dcp()
   False

   >>> A = variable(4,4)
   >>> belongs(A,semidefinite_cone).is_dcp()				# Check if set membership constraint is DCP-compliant
   True

   >>> belongs(abs(A),semidefinite_cone).is_dcp()
   False
	     
   >>> p = prog(minimize(norm1(w)),[geq(sqrt(w),3)])			# Check if a program is DCP-compliant
   >>> p.is_dcp()
   True

   >>> p.objective.is_convex()
   True
	     
   >>> p.constraints.is_dcp()
   True

.. _param_attributes_dcp:

DCP-compliance of families of programs
======================================
As mentioned earlier, parameters can contain sign information. This information can be specified at construction by passing :func:`parameter() <cvxpy.interface.parameter>` an attribute argument or by setting a parameter's ``attribute`` field with the string ``'nonnegative'`` or ``'nonpositive'``. Specifying a parameter's sign is useful for determining DCP-compliance of expressions containing parameters and hence of families of optimization programs::

   >>> a = parameter() 		    	    	 	      	# Create a variable and parameter
   >>> x = variable()

   >>> (a*square(x+1)).is_convex()   			        # Convexity of expression can't be guaranteed
   False

   >>> a.attribute = 'nonnegative'				# Restrict a to be nonnegative

   >>> (a*square(x+1)).is_convex()				# Convexity of expression can now be guaranteed
   True   

   >>> b = parameter(attribute='nonpositive')			# Create a parameter and specify attribute at construction

   >>> p = program(minimize(x),[geq(-b*sqrt(x),2)])		
   >>> p.is_dcp()					        # DCP-compliance of family of programs is guaranteed
   True
