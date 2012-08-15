from numpy import ndarray, zeros, logical_and, sum
import os, types
from ..offspecular.FilterableMetaArray import FilterableMetaArray as MetaArray
from reduction.formats import load

def autoApplyToList(apply):
    """ 
    decorator for 'apply' method - if a list of data objects is given
    as the first argument, applies the filter to each item one at a time.
    """
    
    def newfunc(data, *args, **kwargs):
        if type(data) is types.ListType:
            result = []
            for datum in data:
                result.append(apply(datum, *args, **kwargs))
            return result
        else:
            return apply(data, *args, **kwargs)
    return newfunc

def LoadICPData(filename, path=None, auto_PolState=False, PolState=''):
    """ 
    loads a data file into a MetaArray and returns that.
    Checks to see if data being loaded is 2D; if not, quits
    
    Need to rebin and regrid if the detector is moving...
    """
    lookup = {"a":"_down_down", "b":"_up_down", "c":"_down_up", "d":"_up_up", "g": ""}
    if path == None:
        path = os.getcwd() # if 'path' is not specified, then the actual path of the current directory is found
    file_obj = load(os.path.join(path, filename), format='NCNR NG-1')
    if not (len(file_obj.detector.counts.shape) == 2):
        # not a 2D object!
        return
    if auto_PolState:
        key = filename[-2] # na1, ca1 etc. are --, nc1, cc1 are -+...
        PolState = lookup[key]
    # force PolState to a regularized version:
    if not PolState in lookup.values():
        PolState = ''
    datalen, xpixels = file_obj.detector.counts.shape
    creation_story = "LoadICPData('{fn}', path='{p}', auto_PolState={aPS}, PolState='{PS}'".format(fn=filename, p=path, aPS=auto_PolState, PS=PolState)

# doesn't really matter; changing so that each keyword (whether it took the default value
# provided or not) will be defined
#    if not PolState == '':
#        creation_story += ", PolState='{0}'".format(PolState)

        
    creation_story += ")" 
    info = [{"name": "theta", "units": "degrees", "values": file_obj.sample.angle_x, "det_angle":file_obj.detector.angle_x }, # FilterableMetaArray information
            {"name": "xpixel", "units": "pixels", "values": range(xpixels) },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": PolState, "filename": filename, "start_datetime": file_obj.date,
             "CreationStory":creation_story, "path":path}]
    data_array = zeros((datalen, xpixels, 4))
    mon = file_obj.monitor.counts
    mon.shape += (1,) # broadcast the monitor over the other dimension
    count_time = file_obj.monitor.count_time
    count_time.shape += (1,)
    data_array[:, :, 0] = file_obj.detector.counts
    data_array[:, :, 1] = 1
    data_array[:, :, 2] = mon
    data_array[:, :, 3] = count_time
    # data_array[:,:,4]... I wish!!!  Have to do by hand.
    data = MetaArray(data_array, dtype='float', info=info)
    return data
    
@autoApplyToList
def FootprintCorrection(input, start='0', end='0', slope='0', intercept='0'):
    """ 
    Makes copy of DataArray, iterates through it (beginning at "start" and ending at "finish"), and adds footprint correction to each value.
    Returns resulting data values as a MetaArray.
    """
    data = MetaArray(input.view(ndarray).copy(), input.dtype, input.infoCopy())  # creates copy of input array
    start = float(start) # beginning of footprint region
    end = float(end) # end of footprint region
    slope = float(slope) # slope of line interactor plugin
    intercept = float(intercept) # y-intercept of line interactor plugin
    
    """
    mask = (xaxisvalues > start) and (xaxisvalues < end)
    data[0][mask] += data[0][mask] * slope + intercept
    """
    endpoint = data['Measurements':'counts'][data.axisValues(0) > end][0]
    
    mask = logical_and((data.axisValues(0) >= start), (data.axisValues(0) <= end)) # 'mask' defines interval of footprint region
    xvalues = data.axisValues(0)[mask] # interval of x-values used to calculate footprint region
    counts = data['Measurements':'counts'][mask] # values in footprint region that will be adjusted
    #monitor = data['Measurements':'monitor']
    #avg_monitor = sum(monitor) / monitor.shape[0]
    #counts = data[0][start:end, 0] # interval of data specified by start and finish
    #print 'before correction: ', data['Measurements':'counts'][mask]
    counts = counts * endpoint / ((xvalues * slope) + intercept) # applying footprint correction
    data['Measurements':'counts'][mask] = counts # replaces original counts values in footprint region with adjusted values
    #print 'after correction: ', data['Measurements':'counts'][mask]
    #monitor[mask]  += ... oops - we need to know the max of the monitor to do this.
    #data[0][start:end, 0] = ccounts # replacing original data in specified interval with corrected data
    return data

@autoApplyToList    
def BackgroundSubtraction(input, background='0'):
    """
    Makes copy of input (DataArray) and subtracts "background" from "counts" values.
    """
    data = MetaArray(input.view(ndarray).copy(), input.dtype, input.infoCopy()) # creates copy of input array
    counts = data['Measurements':'counts']
    background = float(background) # turns string argument 'background' into its decimal value
    counts = counts - background
    data['Measurements':'counts'] = counts # updates data array with updated 'counts' values
    return data

@autoApplyToList    
def NormalizeToMonitor(input):
    """
    Divides all the 'counts' values by the 'monitor' values and outputs the result as 'normcounts'
    """
    output = zeros(input.shape[:-1] + (5,), dtype=float) # creates array of zeros with same number of rows but with an extra column      
    copy = input.infoCopy() # makes copy of original FilterableMetaArray information
    copy[1]['cols'].extend([{'name':'normcounts'}]) # adds 'normcounts' label to copied information
    
    counts = input['Measurements':'counts']  # pointers to data of original input array
    monitor = input['Measurements':'monitor']
    norm = counts/monitor   
    pixels = input['Measurements':'pixels']
    time = input['Measurements':'count_time']
    
    for x in range(0, output.shape[0]):  # traverses through array of zeros and replaces zeros with the original values in their original positions
        output[x][0] = counts[x]
        output[x][1] = pixels[x]
        output[x][2] = monitor[x]
        output[x][3] = time[x]
        output[x][4] = norm[x] # adds new 'normcounts' values
    
    result = MetaArray(output, output.dtype, copy) # creates new FilterableMetaArray object with update info and updated array values
    return result
    
    
   
