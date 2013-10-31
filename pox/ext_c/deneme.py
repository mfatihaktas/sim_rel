import os,sys
#
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def main():
  #parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  #print 'parentdir: ', parentdir
  fig = plt.figure(figsize=(14,6))
  ax = fig.add_subplot(111, projection='3d')
  
  #ax.bar([1.4, 2], [1.4, 2], [1.83, 1], zdir='y', color='b', alpha=0.4, width=0.4)
  """
  x = [1.4, 2]
  y = [1.4, 2]
  z = [1.83, 1]
  """
  ax.bar3d(2, 2, 1, dx=0.1, dy=0.1, dz=1, color='b', alpha=0.4)
  ax.bar3d(3, 3, 1, dx=0.1, dy=0.1, dz=1, color='b', alpha=0.4)
  #ax.bar3d(x, y, z, dx=0.1, dy=0.1, dz=0.1, color='b', alpha=0.4)
  """
  for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
    xs = np.arange(20)
    ys = np.random.rand(20)

    # You can provide either a single color or an array. To demonstrate this,
    # the first bar of each set will be colored cyan.
    cs = [c] * len(xs)
    cs[0] = 'c'
    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)
  """
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')

  plt.show()

if __name__ == "__main__":
  main()
