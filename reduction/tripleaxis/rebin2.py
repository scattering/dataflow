import numpy as np

#TODO incorporate a parameter "edges" to determine whether we bins have edges or edges+1
def rebin_1D(xarr, yarr, xbin=None, xstep=None, BINCOUNT=0):
    # if xbin is not given, it will be created based on the data
    size = len(xarr)
    if xbin == None:
        xmin = min(xarr) 
        xmax = max(xarr)
        
        if BINCOUNT > 0:
            xbin = np.linspace(xmin, xmax, BINCOUNT)
            ybin = np.zeros(BINCOUNT, dtype=np.float64)
        else:
            xstep = 1.0 * (xmax - xmin) / xsize
            xbin = np.arange(xmin, xmax, xstep)
            ybin = np.zeros(size, dtype=np.float64)            

    #constructed ybin as an array to keep cumulative sum of data (to be averaged)
    #and ycounts as an array to keep track of how many points in each bin (for averaging)
    ycounts = ybin.copy() #should be a deep copy
    
    for i in range(xsize):
        xoffset = 0
        xval = xarr[i]
        while (xval > xbin[xoffset + 1]):
            xoffset += 1
        
        #Since the min/max values were extended to make the bins, the case where
        #a point is on the outter edge of the grid will never occur.
        if (xoffset > 0 and xoffset < xsize-1) and xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
            ybin[xoffset] += yarr[i] / 2.0
            ybin[xoffset + 1] += yarr[i] / 2.0
            ycounts[xoffset] += 1
            ycounts[xoffset + 1] += 1
        else:
            ybin[xoffset] += yarr[i]
            ycounts[xoffset] += 1
        
    #find all cell indices of bins with points in them, then average their cumulative sums
    used_cells = np.where(ycounts > 0)
    for i in range(len(used_cells[0])):
        ybin[used_cells[0][i]] /= ycounts[used_cells[0][i]]
    
    return xbin, ybin


def rebin_rectangles(xarr, yarr, zarr, BINCOUNT=0):
    """ Given three arrays of data: bins the z values according to their (x,y) positions 
    within the rectuangularly defined bins. Returns 2D array of zarr values binned. """
    # could calculate the smallest x and y deltas to use to make the bins
    # for now, set up with kwarg BINCOUNT that hardcodes in 100 bins
    
    if zarr == None:
        xbin, ybin = rebin_1D(xarr, yarr, BINCOUNT=BINCOUNT)
        return xbin, ybin, None
        
    
    xmin=min(xarr)
    xmax=max(xarr)
    ymin=min(yarr)
    ymax=max(yarr)
    size = len(xarr)
    
    if BINCOUNT > 0:
        xbin = np.linspace(xmin, xmax, BINCOUNT)
        ybin = np.linspace(ymin, ymax, BINCOUNT)
        zbin = np.zeros((BINCOUNT, BINCOUNT), dtype=np.float64)
    else:
        xstep = 1.0 * (xmax - xmin) / size
        ystep = 1.0 * (ymax - ymin) / size
        xbin = np.arange(xmin, xmax, xstep)
        ybin = np.arange(ymin, ymax, xstep)
        zbin = np.zeros((size, size), dtype=np.float64)

    zcounts = zbin.copy() #should be a deep copy
    
    for i in range(len(xarr)):
        xoffset = 0
        yoffset = 0
        xval = xarr[i]
        yval = yarr[i]
        while (xval > xbin[xoffset + 1]):
            xoffset += 1
        while (yval > ybin[yoffset + 1]):
            yoffset += 1
        
        #Since the min/max values were extended to make the bins, the case where
        #a point is on the edge of the grid will never occur. Points located at bins'
        #corners are considered in the bottom left bin.
        if (xoffset > 0 and xoffset < size-1) and (yoffset > 0 and yoffset < size-1) and \
           xval == xbin[xoffset] and yval == ybin[yoffset]: # on intersection of bins' corners
            zbin[xoffset][yoffset] += zarr[i] / 4.0
            zbin[xoffset][yoffset + 1] += zarr[i] / 4.0
            zbin[xoffset + 1][yoffset] += zarr[i] / 4.0
            zbin[xoffset + 1][yoffset + 1] += zarr[i] / 4.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset + 1][yoffset] += 1
            zcounts[xoffset][yoffset + 1] += 1
            zcounts[xoffset + 1][yoffset + 1] += 1
        elif (xoffset > 0 and xoffset < size-1) and xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2.0
            zbin[xoffset + 1][yoffset] += zarr[i] / 2.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset + 1][yoffset] += 1
        elif (yoffset > 0 and yoffset < size-1) and yval == ybin[yoffset]: # on intersection of two y bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2.0
            zbin[xoffset][yoffset + 1] += zarr[i] / 2.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset][yoffset + 1] += 1
        else:
            zbin[xoffset][yoffset] += zarr[i]
            zcounts[xoffset][yoffset] += 1
        
    #find all cell index tuples (x,y) of bins with points in them, then average their cumulative sums
    used_cells = np.where(zcounts > 0)
    for i in range(len(used_cells[0])):
        zbin[used_cells[0][i]][used_cells[1][i]] /= zcounts[used_cells[0][i]][used_cells[1][i]]
    
    return xbin, ybin, zbin
            
          






# The following two methods rebin_1D_bin and rebin_rectangles_bin were made to bin
# datasets with (BINCOUNT + 1)x(BINCOUNT + 1) edges to form (BINCOUNT)x(BINCOUNT)
# rectangular bins.

def rebin_1D_bin(xarr, yarr, BINCOUNT=100):
    xmin1 = min(xarr)
    xmax1 = max(xarr)
    
    xmin -= (xmax1 - xmin1) / BINCOUNT / 2
    xmax += (xmax1 - xmin1) / BINCOUNT / 2
    
    xbin = np.linspace(xmin, xmax, BINCOUNT)
    
    #constructing ybin as an array to keep cumulative sum of data (to be averaged)
    #and ycounts as an array to keep track of how many points in each bin (for averaging)
    ybin = np.zeros(BINCOUNT, dtype=np.float64)
    ycounts = ybin.copy() #should be a deep copy
    
    for i in range(len(xarr)):
        xoffset = 0
        xval = xarr[i]
        while (xval > xbin[xoffset + 1]):
            xoffset += 1
        
        #Since the min/max values were extended to make the bins, the case where
        #a point is on the outter edge of the grid will never occur.
        if xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
            ybin[xoffset] += yarr[i] / 2.0
            ybin[xoffset + 1] += yarr[i] / 2.0
            ycounts[xoffset] += 1
            ycounts[xoffset + 1] += 1
        else:
            ybin[xoffset] += yarr[i]
            ycounts[xoffset] += 1
        
    #find all cell indices of bins with points in them, then average their cumulative sums
    used_cells = np.where(ycounts > 0)
    for i in range(len(used_cells[0])):
        ybin[used_cells[0][i]] /= ycounts[used_cells[0][i]]
    
    return xbin, ybin

def rebin_rectangles_bin(xarr, yarr, zarr=None, BINCOUNT=100):
    """ Given three arrays of data: bins the z values according to their (x,y) positions 
    within the rectuangularly defined bins. Returns 2D array of zarr values binned. """
    # could calculate the smallest x and y deltas to use to make the bins
    # for now, set up with kwarg BINCOUNT that hardcodes in 100 bins
    
    if zarr == None:
        xbin, ybin = rebin_1D(xarr, yarr, BINCOUNT)
        return xbin, ybin, None
        
    
    xmin=min(xarr)
    xmax=max(xarr)
    ymin=min(yarr)
    ymax=max(yarr)
    
    '''
    #adjusting extremes so the bins will encompass the actual extremes
    xmin -= (xmax1 - xmin1) / BINCOUNT / 2
    xmax += (xmax1 - xmin1) / BINCOUNT / 2
    ymin -= (ymax1 - ymin1) / BINCOUNT / 2
    ymax += (ymax1 - ymin1) / BINCOUNT / 2
'''
    xbin = np.linspace(xmin, xmax, BINCOUNT)
    ybin = np.linspace(ymin, ymax, BINCOUNT )
  
    
    #constructing zbin as 2D array to keep cumulative sum of intensities (to be averaged)
    #and zcounts  as 2D array to keep track of how many points in each bin (for averaging)

    #zbin = np.array([])
    #for i in range(BINCOUNT):
    #    zbin = np.append(zbin, [np.zeros(BINCOUNT)])
    zbin = np.zeros((BINCOUNT, BINCOUNT), dtype=np.float64)
    zcounts = zbin.copy() #should be a deep copy
    
    for i in range(len(xarr)):
        xoffset = 0
        yoffset = 0
        xval = xarr[i]
        yval = yarr[i]
        while (xval > xbin[xoffset + 1]):
            xoffset += 1
        while (yval > ybin[yoffset + 1]):
            yoffset += 1
        
        #Since the min/max values were extended to make the bins, the case where
        #a point is on the edge of the grid will never occur. Points located at bins'
        #corners are considered in the bottom left bin.
        if xval == xbin[xoffset] and yval == ybin[yoffset]: # on intersection of bins' corners
            zbin[xoffset][yoffset] += zarr[i] / 4.0
            zbin[xoffset][yoffset + 1] += zarr[i] / 4.0
            zbin[xoffset + 1][yoffset] += zarr[i] / 4.0
            zbin[xoffset + 1][yoffset + 1] += zarr[i] / 4.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset + 1][yoffset] += 1
            zcounts[xoffset][yoffset + 1] += 1
            zcounts[xoffset + 1][yoffset + 1] += 1
        elif xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2.0
            zbin[xoffset + 1][yoffset] += zarr[i] / 2.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset + 1][yoffset] += 1            
        elif yval == ybin[yoffset]: # on intersection of two y bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2.0
            zbin[xoffset][yoffset + 1] += zarr[i] / 2.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset][yoffset + 1] += 1            
        else:
            zbin[xoffset][yoffset] += zarr[i]
            zcounts[xoffset][yoffset] += 1
        
    #find all cell index tuples (x,y) of bins with points in them, then average their cumulative sums
    used_cells = np.where(zcounts > 0)
    for i in range(len(used_cells[0])):
        zbin[used_cells[0][i]][used_cells[1][i]] /= zcounts[used_cells[0][i]][used_cells[1][i]]
    
    return xbin, ybin, zbin







if __name__ == "__main__":
    x = np.array([0, 0, 0, 0, 1, 2])
    y = np.array([1.0, 1.1, 1.2, 1.3, 1.4, 4.0])
    xbin, ybin, zbin = rebin_rectangles(x, y)
    print xbin
    print ybin