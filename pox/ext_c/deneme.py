import os,sys

def main():
  parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  print 'parentdir: ', parentdir

if __name__ == "__main__":
  main()
