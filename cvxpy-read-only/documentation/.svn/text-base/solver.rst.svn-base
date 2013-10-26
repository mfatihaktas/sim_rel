.. _solver:

******************
Configuring solver
******************
Each program object in CVXPY contains a dictionary of ``options`` which configures the underlying solver. For more information about the solver, please visit the `CVXOPT <http://abel.ee.ucla.edu/cvxopt/>`_ website. The following is a description of the key-value pairs present in the ``options`` dictionary:

============================ ==================================================================== =====================
Key			     Description				  			  Default	  
============================ ==================================================================== =====================
``'abstol'``		     Absolute accuracy						       	  ``1e-7``							  
``'feastol'``  		     Tolerance for feasibility conditions				  ``1e-6``				  
``'reltol'``		     Relative accuracy 						       	  ``1e-6``	
``'maxiters``  		     Maximum number of iterations					  ``100``						   
============================ ==================================================================== =====================

The following example illustrates how to configure these options::

   >>> x = variable()						# Create variable
   >>> p = program(minimize(2*x+1),[geq(x,10)])			# Create program

   >>> p.options['maxiters']					# Defaul solver configuration
   100
   >>> p.options['abstol']
   1e-07
   >>> p.options['reltol']
   1e-06
   >>> p.options['feastol']
   1e-06

   >>> p.options['abstol'] = 1e-10				# Change solver configuration
   >>> p.options['reltol'] = 1e-9
   >>> p.options['feastol'] = 1e-9
   >>> p.options['maxiters'] = 200
