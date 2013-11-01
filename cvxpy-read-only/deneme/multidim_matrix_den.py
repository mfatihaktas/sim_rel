from cvxpy import *

def main():
  m = variable(2,2,2, name='m')
  print 'm: ', m
  
if __name__ == "__main__":
  main()  
  
