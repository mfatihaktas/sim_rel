from setuptools import setup

setup(name='cvxpy',
      version='0.1',
      license='GPL',
      description='CVXPY',
      author='Tomas Tinoco de Rubira',
      author_email='ttinoco@stanford.edu',
      url='http://www.stanford.edu/~ttinoco',
      install_requires=['setuptools'],
      packages=['cvxpy','cvxpy.procedures',
                'cvxpy.sets','cvxpy.functions'],
      requires=['scipy', 'cvxopt', 'numpy'],
      test_suite='tests',)
