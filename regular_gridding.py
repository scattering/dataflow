import numpy as N
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from numpy.random import uniform

def regularlyGrid(xarr, yarr, zarr, xstart=None, xfinal=None, xstep=None, ystart=None, yfinal=None, ystep=None):
    "Returns the regularly grided xi, yi, and zi arrays from the initial data."
    # if xstart,xfinal,xstep,ystart,yfinal,ystep are NOT given, they are derived from the data
    if xstart==None:
        xstart=xarr.min()
    if xfinal==None:
        xfinal=xarr.max()
    if xstep==None:
        xstep=1.0*(xfinal-xstart)/len(xarr)
    if ystart==None:
        ystart=yarr.min()
    if yfinal==None:
        yfinal=yarr.max()
    if ystep==None:
        ystep=1.0*(yfinal-ystart)/len(yarr)
	
    # define grid.
	xi = N.arange(xstart, xfinal, xstep)
	yi = N.arange(ystart, yfinal, ystep)

	'''
	Programming note:
		linspace does (start, final, how many steps)
		arange does (start, final, step)
	'''

	# grid the data.
	zi = griddata(xarr, yarr, zarr, xi, yi)
    return xi, yi, zi


def plotGrid(xi,yi,zi):
	# contour the gridded data, plotting dots at the randomly spaced data points.
	CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
	CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.jet)
	plt.colorbar() # draw colorbar

	# plot data points.
	plt.scatter(xarr, yarr, marker='o', c='b', s=5)
	plt.xlim(xstart, xfinal)	#setting xlimits
	plt.ylim(ystart, yfinal)	#setting ylimits
	plt.title('Regular Grid')
	plt.show()

	

def regularlyGridRandom():
	"Makes a contour and contourf plot of randomly generated data pts."
	# make up some randomly distributed data
	npts = 1000
	x = uniform(-3, 3, npts)
	y = uniform(-3, 3, npts)
	z = x * N.exp(-x ** 2 - y ** 2)
    
	# define grid.
	xi = N.arange(-3.1, 3.1, 0.05)
	yi = N.arange(-3.1, 3.1, 0.05)

	# grid the data.
	zi = griddata(x, y, z, xi, yi)

	# contour the gridded data, plotting dots at the randomly spaced data points.
	CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
	CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.jet)
	plt.colorbar() # draw colorbar

	# plot data points.
	plt.scatter(x, y, marker='o', c='b', s=5)
	plt.xlim(-3, 3)
	plt.ylim(-3, 3)
	plt.title('griddata test (%d points)' % npts)
	plt.show()

	#returning data
	#results = [xi, yi, zi]
	#return results

def pcolorRandom():
	"Makes a pcolormesh plot of randomly generated data pts."
	# make up some randomly distributed data
	npts = 100
	x = uniform(-3, 3, npts)
	y = uniform(-3, 3, npts)
	z = x * N.exp(-x ** 2 - y ** 2)
    
	# define grid.
	xi = N.arange(-3.1, 3.1, 0.05)
	yi = N.arange(-3.1, 3.1, 0.05)

	# grid the data.
	zi = griddata(x, y, z, xi, yi)

	# contour the gridded data, plotting dots at the randomly spaced data points.
	plt.pcolormesh(xi, yi, zi)	
	#CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
	#CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
	plt.colorbar() # draw colorbar

	# plot data points.
	plt.scatter(x, y, marker='o', c='b', s=5)
	plt.xlim(-3, 3)
	plt.ylim(-3, 3)
	plt.title('griddata test (%d points)' % npts)
	plt.show()

if __name__ == "__main__":
	regularlyGridRandom()
