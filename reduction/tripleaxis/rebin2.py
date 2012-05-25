import numpy as np

#TODO: runs without error, but results seem incorrect; check everything!

def rebin_rectangles(xarr, yarr, zarr, BINCOUNT=100):
    """ Given three arrays of data: bins the z values according to their (x,y) positions 
    within the rectuangularly defined bins. Returns 2D array of zarr values bin'ed. """
    # could calculate the smallest x and y deltas to use to make the bins
    # for now, set up with kwarg BINCOUNT that hardcodes in 100 bins
    
    xmin=min(xarr)
    xmax=max(xarr)
    ymin=min(yarr)
    ymax=max(yarr)
    
    #adjusting extremes so the bins will encompass the actual extremes
    xmin -= (xmax - xmin) / BINCOUNT / 2
    xmax += (xmax - xmin) / BINCOUNT / 2
    ymin -= (ymax - ymin) / BINCOUNT / 2
    ymax += (ymax - ymin) / BINCOUNT / 2
    
    xbin = np.linspace(xmin, xmax, BINCOUNT + 1)
    ybin = np.linspace(ymin, ymax, BINCOUNT + 1)
    
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
            zbin[xoffset][yoffset] += zarr[i] / 4
            zbin[xoffset][yoffset + 1] += zarr[i] / 4
            zbin[xoffset + 1][yoffset] += zarr[i] / 4
            zbin[xoffset + 1][yoffset + 1] += zarr[i] / 4
        elif xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2
            zbin[xoffset + 1][yoffset] += zarr[i] / 2
        elif yval == ybin[yoffset]: # on intersection of two y bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2
            zbin[xoffset][yoffset + 1] += zarr[i] / 2
        else:
            zbin[xoffset][yoffset] += zarr[i]
            zcounts[xoffset][yoffset] += 1
        
    #find all cell index tuples (x,y) of bins with points in them, then average their cumulative sums
    used_cells = np.where(zcounts>0)
    for i in range(len(used_cells[0])):
        zbin[used_cells[0][i]][used_cells[1][i]] /= zcounts[used_cells[0][i]][used_cells[1][i]]
    
    return zbin
            
            