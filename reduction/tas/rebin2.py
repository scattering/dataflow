import numpy as np

def create_xbin(xarr, num_bins=0, xstep=None, edges=True):
    size = len(xarr)
    xmin = min(xarr) 
    xmax = max(xarr)
    
    # Handling when xstep <= 0. Ignore negative signs and convert 0 to None.
    if xstep:
        if xstep < 0:
            xstep = -xstep
        elif xstep == 0:
            xstep = None
    
    if num_bins > 0: 
        if edges:
            xbin = np.linspace(xmin, xmax, num_bins + 1)
        else:
            xbin = np.linspace(xmin, xmax, num_bins)
    else:
        if not xstep:
            xstep = 1.0 * (xmax - xmin) / size
        if edges: 
            xbin = np.arange(xmin, xmax + xstep, xstep)
        else: 
            xbin = np.arange(xmin, xmax, xstep)
            
    return xarr, xbin
 


def rebin_1D(xarr, yarr, xbin=None, num_bins=0, xstep=None, edges=True):
    """
    Rebins data given from xarr and yarr. 
    
    num_bins = number of bins (overrides xstep)
    xstep may be provided beforehand, otherwise derived from data 
    edges = True --> binning with the number of edges given by len(xarr)+1
            False --> binning with the number of bins given by len(xarr)
    
    """
    
    size = len(xarr)
    
    if not xbin:
        xmin = min(xarr) 
        xmax = max(xarr)
        
        # Handling when xstep <= 0. Ignore negative signs and convert 0 to None.
        if xstep:
            if xstep < 0:
                xstep = -xstep
            elif xstep == 0:
                xstep = None
        
        if num_bins > 0: 
            if edges:
                xbin = np.linspace(xmin, xmax, num_bins + 1)
            else:
                xbin = np.linspace(xmin, xmax, num_bins)
            ybin = np.zeros(num_bins, dtype=np.float64)
        else:
            if not xstep:
                xstep = 1.0 * (xmax - xmin) / size
            if edges: 
                xbin = np.arange(xmin, xmax + xstep, xstep)
            else: 
                xbin = np.arange(xmin, xmax, xstep)
            ybin = np.zeros(len(xbin), dtype=np.float64)
    else:
        ybin = np.zeros(len(xbin), dtype=np.float64)


    #constructed ybin as an array to keep cumulative sum of data (to be averaged)
    #and ycounts as an array to keep track of how many points in each bin (for averaging)
    ycounts = ybin.copy() #should be a deep copy
    xbin_max_offset = len(xbin) - 1
    
    for i in range(size):
        xoffset = 0
        xval = xarr[i]
        while (xoffset < xbin_max_offset and xval > xbin[xoffset + 1]):
            xoffset += 1
        
        #Since the min/max values were extended to make the bins, the case where
        #a point is on the outter edge of the grid will never occur.
        if (xoffset > 0 and xoffset < xbin_max_offset) and xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
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


def rebin_2D (xarr, yarr, zarr, num_bins=0, xstep=None, ystep=None, edges=True):
    """ 
    Rebins the zarr values according to their (xarr,yarr) positions within the 
    rectuangularly defined bins. Returns xbin, ybin and zbin (2D array of zarr values binned).
    
    zbin results will have to be transposed for pylab plotting.
    
    num_bins = number of bins (overrides xstep and ystep)
    xstep and/or ystep may be provided beforehand, otherwise derived from data
    edges = True --> binning with the number of edges given by len(xarr)+1
            False --> binning with the number of bins given by len(xarr)
    
    """
    
    # if zarr is None, does 1D binning with xarr and yarr
    if zarr == None:
        xbin, ybin = rebin_1D(xarr, yarr, num_bins=num_bins, xstep=xstep, edges=edges)
        return xbin, ybin, None
        
    xmin = min(xarr)
    xmax = max(xarr)
    ymin = min(yarr)
    ymax = max(yarr)
    xsize = len(xarr)
    ysize = len(yarr)
    
    xbin_max_offset = -1

    
    # Handling when xstep or ystep <= 0. Ignore negative signs and convert 0 to None.
    if xstep:
        if xstep < 0:
            xstep = -xstep
        elif xstep == 0:
            xstep = None    
    if ystep:
        if ystep < 0:
            ystep = -ystep
        elif ystep == 0:
            ystep = None     

    if num_bins > 0: 
        if edges:
            xbin = np.linspace(xmin, xmax, num_bins + 1)
            ybin = np.linspace(ymin, ymax, num_bins + 1)
        else:
            xbin = np.linspace(xmin, xmax, num_bins)
            ybin = np.linspace(ymin, ymax, num_bins)
        zbin = np.zeros((num_bins, num_bins), dtype=np.float64)
    else:
        if not xstep:
            xstep = 1.0 * (xmax - xmin) / xsize
        if not ystep:
            ystep = 1.0 * (ymax - ymin) / ysize
        if edges:
            xbin = np.arange(xmin, xmax + xstep, xstep)
            ybin = np.arange(ymin, ymax + ystep, ystep)
        else:
            xbin = np.arange(xmin, xmax, xstep)
            ybin = np.arange(ymin, ymax, ystep)
        xbin_max_offset = len(xbin) - 1
        ybin_max_offset = len(ybin) - 1
        zbin = np.zeros((xbin_max_offset + 1, ybin_max_offset + 1), dtype=np.float64)
    
    # if the max_offsets were not defined, define them now
    if xbin_max_offset < 0:
        xbin_max_offset = len(xbin) - 1
        ybin_max_offset = len(ybin) - 1

    zcounts = zbin.copy() #should be a deep copy
    
    for i in range(len(xarr)):
        xoffset = 0
        yoffset = 0
        xval = xarr[i]
        yval = yarr[i]
        while xoffset < xbin_max_offset and xval > xbin[xoffset + 1]:
            xoffset += 1
        while yoffset < ybin_max_offset and yval > ybin[yoffset + 1]:
            yoffset += 1
        
        #Since the min/max values were extended to make the bins, the case where
        #a point is on the edge of the grid will never occur. Points located at bins'
        #corners are considered in the bottom left bin.
        if (xoffset > 0 and xoffset < xbin_max_offset) and (yoffset > 0 and yoffset < ybin_max_offset) and \
           xval == xbin[xoffset] and yval == ybin[yoffset]: # on intersection of bins' corners
            zbin[xoffset][yoffset] += zarr[i] / 4.0
            zbin[xoffset][yoffset + 1] += zarr[i] / 4.0
            zbin[xoffset + 1][yoffset] += zarr[i] / 4.0
            zbin[xoffset + 1][yoffset + 1] += zarr[i] / 4.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset + 1][yoffset] += 1
            zcounts[xoffset][yoffset + 1] += 1
            zcounts[xoffset + 1][yoffset + 1] += 1
        elif (xoffset > 0 and xoffset < xbin_max_offset) and xval == xbin[xoffset]: # on intersection of two x bins, put half of value in each bin
            zbin[xoffset][yoffset] += zarr[i] / 2.0
            zbin[xoffset + 1][yoffset] += zarr[i] / 2.0
            zcounts[xoffset][yoffset] += 1
            zcounts[xoffset + 1][yoffset] += 1
        elif (yoffset > 0 and yoffset < ybin_max_offset) and yval == ybin[yoffset]: # on intersection of two y bins, put half of value in each bin
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
