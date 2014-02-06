import numpy as np
from numpy.random import uniform
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt

def edges(C):
    E = 0.5*(C[:-1]+C[1:])
    return np.hstack((C[0]-2*(E[0]-C[0]), E, C[-1]+2*(C[-1]-E[-1])))


def regularlyGrid(xarr, yarr, zarr, xstart=None, xfinal=None, xstep=None, ystart=None, yfinal=None, ystep=None):
    "Returns the regularly grided xi, yi, and zi arrays from the initial data."
    # if xstart,xfinal,xstep,ystart,yfinal,ystep are NOT given, they are derived from the data
    if xstart == None:
        xstart = xarr.min() 
    if xfinal == None:
        xfinal = xarr.max()
    if xstep == None:
        xstep = 1.0 * (xfinal - xstart) / len(xarr)
    if ystart == None:
        ystart = yarr.min()
    if yfinal == None:
        yfinal = yarr.max()
    if ystep == None:
        ystep = 1.0 * (yfinal - ystart) / len(yarr)

    xi = np.arange(xstart, xfinal, xstep)
    yi = np.arange(ystart, yfinal, ystep)
    # Programming note:
	#	linspace does (start, final, how many steps)
	#	arange does (start, final, step)

    # grid the data.
    #print "gridding", len(xarr), len(yarr), len(zarr), len(xi), len(yi)

    xarr,yarr,zarr=remove_duplicates(xarr,yarr,zarr)
    zi = griddata(xarr, yarr, zarr, xi, yi)

    #print "done gridding"
    return xi, yi, zi

def remove_duplicates(xarr, yarr, zarr):
    """Removes duplicate points along the given axes for 2d plotting. In dataflow
    only removes the points temporarily for the plotting, thus changing the
    desired x and y axes will not result in a loss of data."""

    uniques = [] #list of row indices to skip (ie unique pts to keep in datafile)
    dups = []
    numrows = len(xarr)
    for index in range(numrows):
        dups.append(range(numrows)) #list of lists. Each inner list is a list of every row index (0 to len)
                        #when a row becomes distinct from another, its index is removed from the the other's index

    #for field in distinct:
    for i in range(numrows):
        if not uniques.__contains__(i): #if the row isn't unique
            for j in range(i + 1, numrows):
                if not uniques.__contains__(j) and dups[i].__contains__(j):
                    if xarr[i] != xarr[j] or yarr[i] != yarr[j]:
                        dups[i].remove(j)
                        dups[j].remove(i)  
            if len(dups[i]) == 1:
                #if every row in the column is distinct from the ith row, then it is unique
                #MAY NOT NEED TO KEEP TRACK OF UNIQUES...
                #CAN ALWAYS GET BY len(dups[i])==1
                uniques.append(i)

    if len(uniques) == numrows:
        #if all rows are deemed unique, return
        return xarr,yarr,zarr


    #ALL UNIQUE ROWS ARE INDEXED IN uniques NOW
    rows_to_be_removed = []
    for alist in dups:
        #average the detector counts of every detector of each row in alist
        #and save the resulting averages into the first row of alist.
        #then delete other rows, ie remove them
        if len(alist) == 1:
            #if the row is unique skip this list
            pass 
        else:
            for k in range(1, len(alist)):
                zarr[alist[0]] = (zarr[alist[0]] + zarr[alist[k]]) / 2.0
                dups[alist[k]] = [alist[k]] #now the kth duplicate set of indices has only k, so it will be skipped
                rows_to_be_removed.append(alist[k])

    rows_to_be_removed.sort() #duplicate rows to be removed indices in order now
    rows_to_be_removed.reverse() #duplicate rows to be removed indices in reverse order now

    for k in rows_to_be_removed:
        xarr = np.delete(xarr,k,0)
        yarr = np.delete(yarr,k,0)
        zarr = np.delete(zarr,k,0)

    #update primary detector dimension
    return xarr,yarr,zarr

def plotGrid(xi, yi, zi):
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
    z = x * np.exp(-x ** 2 - y ** 2)

    # define grid.
    xi = np.arange(-3.1, 3.1, 0.05)
    yi = np.arange(-3.1, 3.1, 0.05)

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
    z = x * np.exp(-x ** 2 - y ** 2)

    # define grid.
    xi = np.arange(-3.1, 3.1, 0.05)
    yi = np.arange(-3.1, 3.1, 0.05)

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