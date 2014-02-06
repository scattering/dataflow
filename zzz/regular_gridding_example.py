#taken from http://www.scipy.org/Cookbook/Matplotlib/Gridding_irregularly_spaced_data

import numpy as np
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy.ma as ma
from numpy.random import uniform

# make up some randomly distributed data
npts = 200
x = uniform(-2, 2, npts)
y = uniform(-2, 2, npts)
z = x * np.exp(-x ** 2 - y ** 2)

# define grid.
xi = np.linspace(-2.1, 2.1, 100)
yi = np.linspace(-2.1, 2.1, 100)

# grid the data.
zi = griddata(x, y, z, xi, yi)

# contour the gridded data, plotting dots at the randomly spaced data points.
CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.jet)
plt.colorbar() # draw colorbar

# plot data points.
plt.scatter(x, y, marker='o', c='b', s=5)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.title('griddata test (%d points)' % npts)
plt.show()

