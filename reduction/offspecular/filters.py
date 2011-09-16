from numpy import cos, pi, cumsum, arange, ndarray, ones, zeros, array, newaxis, linspace, empty, resize, sin, allclose, zeros_like, linalg, dot, arctan2, float64, histogram2d
import os, simplejson, datetime, sys, types, xml.dom.minidom
from copy import deepcopy

from FilterableMetaArray import FilterableMetaArray as MetaArray
from he3analyzer import wxHe3AnalyzerCollection as He3AnalyzerCollection
from reduction.formats import load
import reduction.rebin as reb
import h5py

class Supervisor():
    """ class to hold rebinned_data objects and increment their reference count """
    def __init__(self):
        self.rb_count = 0
        self.rebinned_data_objects = []
        self.plottable_count = 0
        self.plottable_2d_data_objects = []
        self.plots2d_count = 0
        self.plots2d_data_objects = []
        self.plots2d_names = []

    def AddRebinnedData(self, new_object, name='', base_data_obj=None):  
        self.rebinned_data_objects.append(new_object)
        new_object.number = self.rb_count
        self.rb_count += 1
    
    def AddPlottable2dData(self, new_object, parent=None, name='', base_data_obj=None):
        self.plottable_2d_data_objects.append(new_object)
        self.plottable_count += 1
  
    def AddPlot2d(self, new_object, parent=None, name=''):
        self.plots2d_data_objects.append(new_object)
        self.plots2d_names.append(name)
        self.plots2d_count += 1
        
    def __iadd__(self, new_object):
        if isinstance(new_object, rebinned_data):
            self.AddRebinnedData(new_object)
        elif isinstance(new_object, plottable_2d_data):
            self.AddPlottable2dData(new_object)
        return self

def th_2th_single_dataobj():
    info = [{"name": "Theta", "units": "degrees", "values": th_list },
            {"name": "TwoTheta", "units": "degrees", "values": twoth_list},
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": '++'}]
    data = MetaArray((th_len, twoth_len, 5), info=info)
    return data
    
def th_2th_polarized_dataobj():
    info = [{"name": "Theta", "units": "degrees", "values": th_list },
            {"name": "TwoTheta", "units": "degrees", "values": twoth_list},
            {"name": "PolState", "values": "++"},
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": '++'}]
    data = MetaArray((th_len, twoth_len, 1, 5), info=info)
    return data

def qx_qz_single_dataobj(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins):
    info = [{"name": "qz", "units": "inv. Angstroms", "values": linspace(qzmin, qzmax, qzbins) },
            {"name": "qx", "units": "inv. Angstroms", "values": linspace(qxmin, qxmax, qxbins) },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": '++'}]
    data = MetaArray((qzbins, qxbins, 4), info=info)
    return data

def default_qx_qz_grid():
    return EmptyQxQzGrid(-0.003, 0.003, 201, 0, 0.14, 201)

class EmptyQxQzGrid(MetaArray):
    def __new__(subtype, qxmin, qxmax, qxbins, qzmin, qzmax, qzbins):
        creation_story = subtype.__name__
        creation_story += "({0}, {1}, {2}, {3}, {4}, {5})".format(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
        info = [
            {"name": "qx", "units": "inv. frakking Angstroms", "values": linspace(qxmin, qxmax, qxbins) },
            {"name": "qz", "units": "inv. Angstroms", "values": linspace(qzmin, qzmax, qzbins) },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {'CreationStory': creation_story}]
        data = MetaArray(zeros((qxbins, qzbins, 4)), info=info)
        return data
    
def th_2th_combined_dataobj():
    info = [{"name": "Theta", "units": "degrees", "values": th_list },
            {"name": "TwoTheta", "units": "degrees", "values": twoth_list},
            {"name": "PolState", "values": ['++', '+-', '-+', '--']},
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]}]
    data = MetaArray((th_len, twoth_len, 4, 5), dtype='float', info=info)
    return data

def reflbinned_pixel_single_dataobj(datalen, xpixels):
    info = [{"name": "datapoints", "units": None, "values": range(datalen) },
            {"name": "xpixel", "units": "pixels", "values": range(xpixels) },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": '++'}]
    data = MetaArray(ones((datalen, xpixels, 5)), dtype='float', info=info)
    return data

def reflbinned_pixel_combined_dataobj(datalen, xpixels):
    info = [{"name": "datapoints", "units": None, "values": range(datalen) },
            {"name": "xpixel", "units": "pixels", "values": range(xpixels) },
            {"name": "PolState", "values": ['++', '+-', '-+', '--']},
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]}]
    data = MetaArray((datalen, xpixels, 4, 5), info=info)
    return data

class Filter2D:
    """ takes MetaArray with 2 dims (2 cols) as input
    and outputs the same thing """ 
    default_path = None
    
    def __init__(self, *args, **kwargs):
        self.valid_column_labels = [['', '']]

# ******duplicate decorator, so I commented it out********

#    def updateCreationStory(apply):
#        """ 
#        decorator for 'apply' method - it updates the Creation Story
#        for each filter application.
#        """
#        
#        def newfunc(self, data, *args, **kwargs):
#            result = apply(self, *args, **kwargs)
#            name = self.__class__.__name__
#            new_info = result.infoCopy()
#            new_type = result.dtype
#            new_data = result.view(ndarray)
#            new_args = "".join([', {arg}'.format(arg=arg) for arg in args])
#            new_kwargs = "".join([', {key}={value}'.format(key=key, value=kwargs[key]) for key in kwargs])
#            new_creation_story = "{old_cs}.filter('{fname}', {args}, {kwargs})".format(old_cs=old_cs, fname=name, args=new_args, kwargs=new_kwargs)
#            #print new_creation_story
#            #new_info[-1]["CreationStory"]
#            return result
#        return newfunc

    
    def check_labels(self, data):
        validated = True
        labelsets = self.valid_column_labels
        info = data.infoCopy()
        for labelset in labelsets:
            for col, label in zip(info, labelset):
                if not col["name"] == label:
                    validated = False
        return validated
    
    def validate(self, data):
        validated = True
        if not type(data) == MetaArray:
            print "not MetaArray"
            return False #short-circuit
        if not len(data.shape) == 3:
            print "# coordinate dims not equal 2"
            return False 
        return self.check_labels(data)
    
    def apply(self, data):
        if not self.validate(data):
            print "error in data type"
            return
        return data
 
def updateCreationStory(apply):
    """ 
    decorator for 'apply' method - it updates the Creation Story
    for each filter application.
    """
    
    def newfunc(self, data, *args, **kwargs):
        name = self.__class__.__name__
        new_args = "".join([', {arg}'.format(arg=arg) for arg in args])
        new_kwargs = "".join([', {key}={value}'.format(key=key, value=kwargs[key]) for key in kwargs])
        new_creation_story = ".filter('{fname}'{args}{kwargs})".format(fname=name, args=new_args, kwargs=new_kwargs)
        result = apply(self, data, *args, **kwargs)
        
        # Try update in place data._info instead! 
        result._info[-1]["CreationStory"] += new_creation_story
        # if the above didn't work, uncomment this below:
        #new_info = result.infoCopy()
        #new_dtype = result.dtype
        #new_data_array = result.view(ndarray)
        #new_info[-1]["CreationStory"] += new_creation_story
        #new_data = MetaArray(new_data_array, dtype=new_dtype, info=new_info)
        #return new_data
        return result
    return newfunc
 
def autoApplyToList(apply):
    """ 
    decorator for 'apply' method - if a list of data objects is given
    as the first argument, applies the filter to each item one at a time.
    """
    
    def newfunc(self, data, *args, **kwargs):
        if type(data) is types.ListType:
            result = []
            for datum in data:
                result.append(apply(self, datum, *args, **kwargs))
            return result
        else:
            return apply(self, data, *args, **kwargs)
    return newfunc

class CoordinateOffset(Filter2D):
    """ apply an offset to one or both of the coordinate axes """
    
    @autoApplyToList
    @updateCreationStory
    def apply(self, data, offsets={}):
        """ to apply an offset to an axis, add it to the dict of offsets.
        e.g. if data is theta, twotheta, then
        to apply 0.01 offset to twotheta only make offsets = {'twotheta': 0.01}
        """
        new_info = data.infoCopy()
        for key in offsets:
            try:
                axisnum = data._getAxis(key)
                new_info[axisnum]['values'] += offsets[key]
            except:
                pass
        new_data = MetaArray(data.view(ndarray).copy(), info=new_info)
        return new_data

class MaskData(Filter2D):
    """ set all data, normalization to zero within mask """
    
    @autoApplyToList
    @updateCreationStory
    def apply(self, data, xmin=None, xmax=None, ymin=None, ymax=None):
        xmin, xmax, ymin, ymax = [s for s in [xmin, xmax, ymin, ymax] if s!="" else None]
        def sanitize (item):
            return int(item) if item != "" else None
        dataslice = (slice(sanitize(xmin), sanitize(xmax)), slice(sanitize(ymin), sanitize(ymax)))
        new_data = MetaArray(data.view(ndarray).copy(), info=data.infoCopy())
        new_data[dataslice] = 0
        return new_data
        
              
class WiggleCorrection(Filter2D):
    """ 
    Remove the oscillatory artifact from the Brookhaven 2D detector data
    This filter properly works on data in pixel coordinates, so it belongs
    right at the beginning of most filter chains, before data is converted to
    angle (and then Q...) 
    
    The artifact is defined as being a sinusoidal variation in the effective width
    of the pixel --- this results in two effects: 
    1. an apparent oscillation in sensitivity
    2. an oscillatory shift in the effective location of the pixel with
        respect to an ordered grid of pixels.
    """
    
    def __init__(self, amp=0.140, **kwargs):
        Filter2D.__init__(self, **kwargs)
        self.wiggleAmplitude = amp
        self.valid_column_labels = [["theta", "xpixel"]]
        
        
    def correctionFromPixel(self, xpixel, wiggleAmplitude):
        xpixel = xpixel.astype('float')
        #wiggleAmplitude = self.wiggleAmplitude
        #pixelCorrection = ( (32.0 / (2.0 * pi) ) * wiggleAmplitude * sin( 2.0 * pi * xpixel / 32.0 ) )
        widthCorrection = (wiggleAmplitude * cos(2.0 * pi * xpixel / 32.0))
        pixelCorrection = cumsum(widthCorrection) - widthCorrection[0]
        return [widthCorrection, pixelCorrection]
    
    @autoApplyToList
    @updateCreationStory      
    def apply(self, data, amp=0.14):
        """ Data is MetaArray (for now) with axis values + labels
        Output is the same """
        if not self.validate(data):
            print "error in data type"
            return
        
        num_xpixels = len(data.axisValues('xpixel'))
        if not (num_xpixels == 608):
            print "this correction is only defined for Brookhaven detector!"
        xpixel = data.axisValues('xpixel')
        #arange(num_xpixels + 1, 'float')
        widthCorrection, pixelCorrection = self.correctionFromPixel(xpixel, amp)
        corrected_pixel = xpixel + pixelCorrection
        intens = data['Measurements': 'counts']
        corrected_I = intens / (1.0 + widthCorrection)
        new_info = data.infoCopy()
        new_info[1]["values"] = corrected_pixel
        new_data = MetaArray(data.view(ndarray).copy(), info=new_info)
        new_data['Measurements': 'counts'] = corrected_I

        return new_data

class AsterixPixelsToTwotheta(Filter2D):
    """ input array has pixels axis, convert to 
    two-theta based on distance from sample to detector and
    center pixel when two-theta motor is set to zero """
    
    @autoApplyToList
    @updateCreationStory
    def apply(self, data, qzero_pixel = 145., twotheta_offset=0.0, pw_over_d=0.0003411385649):
        """ pw_over_d is pixel width divided by distance (sample to detector) """
        new_info = data.infoCopy()
        # find pixels axis, and replace with two-theta
        # assuming there are only 2 dimensions of data, looking only at indices 0, 1
        xpixel_axis = next((i for i in xrange(len(new_info)) if new_info[i]['name'] == 'xpixel'), None) 
        if xpixel_axis < 0:
            print "error: no xpixel axis in this dataset"
            return
        
        new_info[xpixel_axis]['name'] = 'twotheta'    
        if data._info[-1].has_key('state'):
            twotheta_offset = float(data._info[-1]['state']['A[0]'])
        pixels = data.axisValues('xpixel')
        twotheta = arctan2((pixels - qzero_pixel) * pw_over_d, 1.0) * 180./pi + twotheta_offset
        new_info[xpixel_axis]['values'] = twotheta
        new_data = MetaArray(data.view(ndarray).copy(), info=new_info)
        
        return new_data
        
class AsterixTOFToWavelength(Filter2D):
    """ input array has TOF axis, convert to wavelength
    based on calibration (depends on distance from source to detector) """
    
    @autoApplyToList
    @updateCreationStory
    def apply(self, data, wl_over_tof=1.9050372144288577e-5):
        """ pw_over_d is pixel width divided by distance (sample to detector) """
        new_info = data.infoCopy()
        # find pixels axis, and replace with two-theta
        # assuming there are only 2 dimensions of data, looking only at indices 0, 1
        tof_axis = next((i for i in xrange(len(new_info)) if new_info[i]['name'] == 'tof'), None) 
        if tof_axis < 0:
            print "error: no tof axis in this dataset"
            return
        
        new_info[tof_axis]['name'] = 'wavelength'
        tof = data.axisValues('tof')
        wavelength = (tof * wl_over_tof)
        # shift by half-bin width to align to center of tof bins!
        wavelength += (tof[1] - tof[0])/2.0 * wl_over_tof
        # (bins appear to be centered)
        new_info[tof_axis]['values'] = wavelength
        new_data = MetaArray(data.view(ndarray).copy(), info=new_info)
        
        return new_data

class AsterixShiftData(Filter2D):

    @autoApplyToList
    @updateCreationStory
    def apply(self, data, edge_bin = 180):
        """ Shift 2D dataset along axis 0, also shifting the axisValues
        along that edge (assuming linear behaviour) 
        This is useful for time-of-flight data where the low-t data is empty due
        to spectrum shape, and can be interpreted as the high-t data from the
        previous pulse.""" 
        axis = 0
        new_info = data.infoCopy()
        old_axis_values = new_info[axis]['values']
        
        shifted_data = empty(data.shape)
        shifted_data[:-edge_bin,:,:] = data[edge_bin:,:,:]
        shifted_data[-edge_bin:,:,:] = data[:edge_bin,:,:]
        shifted_axis = zeros(data.shape[axis])
        dx = old_axis_values[1] - old_axis_values[0]
        shifted_axis[:-edge_bin] = old_axis_values[edge_bin:]
        shifted_axis[-edge_bin:] = old_axis_values[:edge_bin] + (old_axis_values[-1] - old_axis_values[0]) + dx
        
        new_info[axis]['values'] = shifted_axis
        new_data = MetaArray(shifted_data, info=new_info)
        return new_data

class PixelsToTwotheta(Filter2D):
    """ input array has axes theta and pixels:
    output array has axes theta and twotheta.
    
    Pixel-to-angle conversion is arithmetic (pixels-per-degree=constant)
    output is rebinned to fit in a rectangular array if detector angle 
    is not fixed. """
    
    @autoApplyToList
    @updateCreationStory 
    def apply(self, data, pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6):
        new_info = data.infoCopy()
        det_angle = new_info[0].pop('det_angle') # read and get rid of it!
        th_vector = data.axisValues('theta')
        th_spacing = th_vector[1] - th_vector[0]
        pixels = data.axisValues('xpixel')
        twoth = -1.0 * (pixels - qzero_pixel) / pixels_per_degree
        twoth_min = det_angle.min() + twoth.min()
        twoth_max = det_angle.max() + twoth.max()
        twoth_max_edge = twoth_max + 1.0 / pixels_per_degree
        dpp = 1.0 / pixels_per_degree
        output_twoth_bin_edges = arange(twoth_max + dpp, twoth_min - dpp, -dpp)
        output_twoth = output_twoth_bin_edges[:-1]
        
        #input_twoth_bin_edges = output_twoth_bin_edges.copy()
        #input_twoth_bin_edges[:-1] = twoth
        th_bin_edges = linspace(th_vector[0], th_vector[-1] + th_spacing, len(th_vector) + 1)
        new_info[1]['name'] = 'twotheta' # getting rid of pixel units: substitute twoth
        new_info[1]['values'] = output_twoth
        new_info[1]['units'] = 'degrees'
        new_data = MetaArray((len(th_vector), len(output_twoth), data.shape[2]), info=new_info) # create the output data object!
        # (still has to be filled with correct values)
                       
        if ((det_angle.max() - det_angle.min()) < instr_resolution):
            #then the detector is fixed and we can pass a single 2theta vector to rebin2d
            input_twoth_bin_edges = empty(len(pixels) + 1)
            input_twoth_bin_edges[0] = twoth_max + 1.0 / pixels_per_degree
            input_twoth_bin_edges[1:] = twoth + det_angle.min()
            data_cols = ['counts', 'pixels', 'monitor', 'count_time']
            for col in data_cols:
                array_to_rebin = data[:, :, col].view(ndarray).copy() 
                new_array = reb.rebin2d(th_bin_edges, input_twoth_bin_edges, array_to_rebin, th_bin_edges, output_twoth_bin_edges)
                new_data[:, :, col] = new_array
        else:
            #then the detector is not fixed, and we have to pass in each A4 value at a time to rebin
            tth_min = twoth.min()
            tth_max = twoth.max()
            for i, da in enumerate(det_angle):
                twoth_min = da + tth_min
                twoth_max = da + tth_max
                input_twoth_bin_edges = empty(len(pixels) + 1)
                input_twoth_bin_edges[0] = twoth_max + 1.0 / pixels_per_degree
                input_twoth_bin_edges[1:] = twoth + da         
                data_cols = ['counts', 'pixels', 'monitor', 'count_time']
                for col in data_cols:
                    array_to_rebin = data[i, :, col].view(ndarray).copy()
                    new_array = reb.rebin(input_twoth_bin_edges, array_to_rebin, output_twoth_bin_edges)
                    new_data[i, :, col] = new_array
                
        return new_data

class Autogrid(Filter2D):
    """ take multiple datasets and create a grid which covers all of them
    - stepsize is smallest stepsize found in datasets
    returns an empty grid with units and labels
    
    if extra_grid_point is True, adds one point to the end of each axis
    so each dimension is incremented by one (makes edges for rebinning) """
    
    def apply(self, list_of_datasets, extra_grid_point=True, min_step=1e-10):
        num_datasets = len(list_of_datasets)
        dims = 2
        dim_min = zeros((dims, num_datasets))
        dim_max = zeros((dims, num_datasets))
        dim_len = zeros((dims, num_datasets))
        dim_step = zeros((dims, num_datasets))
    
        for i, data in enumerate(list_of_datasets):
            info = data.infoCopy()
            for dim in range(dims):
                av = data.axisValues(dim)
                dim_min[dim, i] = av.min()
                dim_max[dim, i] = av.max()
                dim_len[dim, i] = len(av)
                if dim_len[dim, i] > 1:
                    dim_step[dim, i] = float(dim_max[dim, i] - dim_min[dim, i]) / (dim_len[dim, i] - 1)
                    # dim0_max[i] += th_step[i] # add back on the last step
                else:
                    dim_step[dim, i] = min_step

        final_stepsizes = []
        absolute_max = []
        absolute_min = []
        for dim in range(dims):
            dim_stepsize = dim_step[dim].max()
            if dim_stepsize < min_step:
                dim_stepsize = min_step
            final_stepsizes.append(dim_stepsize)
            
            absolute_max.append(dim_max[dim].max())
            absolute_min.append(dim_min[dim].min())
            
        # now calculate number of steps:
        output_dims = []
        for dim in range(dims):
            if (dim_len[dim].max() == 1) or (absolute_max[dim] == absolute_min[dim]):
                steps = 1
            else:
                steps = int(round(float(absolute_max[dim] - absolute_min[dim]) / final_stepsizes[dim]))
            if extra_grid_point == True:
                steps += 1
            output_dims.append(steps)
        
        new_info = list_of_datasets[0].infoCopy() # take units etc from first dataset
         # then tack on the number of columns already there:
        output_dims.append(len(new_info[2]['cols']))
        for dim in range(dims):
            new_info[dim]["values"] = (arange(output_dims[dim], dtype='float') * final_stepsizes[dim]) + absolute_min[dim]
        output_grid = MetaArray(tuple(output_dims), info=new_info)
        return output_grid
        
    
# *******duplicate?********
    
#class ICPDataFromFile(MetaArray):
#    default_path = None
#       
#    def __new__(subtype, filename, path=None, auto_PolState=False, PolState=''):
#        """ 
#        loads a data file into a MetaArray and returns that.
#        Checks to see if data being loaded is 2D; if not, quits
#        
#        Need to rebin and regrid if the detector is moving...
#        """
#        lookup = {"a":"--", "b":"+-", "c":"-+", "d":"++", "g": ""}
#        if path == None:
#            path = subtype.default_path
#        if path == None:
#            path = os.getcwd()
#        subtype.default_path = path
#        Filter2D.default_path = path
#        
#        def new_single(filename, path, auto_PolState, PolState):
#            file_obj = load(os.path.join(path, filename))
#            if not (len(file_obj.detector.counts.shape) == 2):
#                # not a 2D object!
#                return
#            if auto_PolState:
#                key = filename[-2] # na1, ca1 etc. are --, nc1, cc1 are -+...
#                PolState = lookup[key]
#            # force PolState to a regularized version:
#            if not PolState in lookup.values():
#                PolState = ''
#            datalen, xpixels = file_obj.detector.counts.shape
#            creation_story = "ICPDataFromFile('{fn}'".format(fn=filename)
#            if not PolState == '':
#                creation_story += ", PolState='{0}'".format(PolState)
#            creation_story += ")" 
#            info = [{"name": "theta", "units": "degrees", "values": file_obj.sample.angle_x, "det_angle":file_obj.detector.angle_x },
#                    {"name": "xpixel", "units": "pixels", "values": range(xpixels) },
#                    {"name": "Measurements", "cols": [
#                            {"name": "counts"},
#                            {"name": "pixels"},
#                            {"name": "monitor"},
#                            {"name": "count_time"}]},
#                    {"PolState": PolState, "filename": filename, "start_datetime": file_obj.date,
#                     "CreationStory":creation_story, "path":path}]
#            data_array = zeros((datalen, xpixels, 4))
#            mon = file_obj.monitor.counts
#            mon.shape += (1,) # broadcast the monitor over the other dimension
#            count_time = file_obj.monitor.count_time
#            count_time.shape += (1,)
#            data_array[:, :, 0] = file_obj.detector.counts
#            data_array[:, :, 1] = 1
#            data_array[:, :, 2] = mon
#            data_array[:, :, 3] = count_time
#            # data_array[:,:,4]... I wish!!!  Have to do by hand.
#            data = MetaArray(data_array, dtype='float', info=info)
#            return data
#        
#        if type(filename) is types.ListType:
#            result = [new_single(fn, path, auto_PolState, PolState) for fn in filename]
#            return result
#        else:
#            return new_single(filename, path, auto_PolState, PolState)

def hdf_to_dict(hdf_obj, convert_i1_tostr=True):
    out_dict = {}
    for key in hdf_obj:
        val = hdf_obj[key]
        if type(val) == h5py.highlevel.Dataset:
            if (val.value.dtype == 'int8') and (convert_i1_tostr == True):
                value = val.value.tostring()
            else:
                value = val.value 
            out_dict[key] = value
        else:
            out_dict[key] = hdf_to_dict(val)
    return out_dict

def LoadAsterixRawHDF(filename, path=None):
    if path == None:
        path = os.getcwd()
    hdf_obj = h5py.File(os.path.join(path, filename), mode='r')
    run_title = hdf_obj.keys()[0]
    run_obj = hdf_obj[run_title]
    state = hdf_to_dict(run_obj['ASTERIX'])
    monitor = hdf_to_dict(run_obj['scalars'])
    tof = run_obj['ordela_tof_pz']['tof'].value.astype(float64)
    twotheta_pixel = run_obj['ordela_tof_pz']['X'].value.astype(float64)
    data = run_obj['ordela_tof_pz']['data'].value.astype(float64)
    creation_story = "LoadAsterixRawHDF('{fn}')".format(fn=filename)
    pol_states = {0:'--', 1:'-+', 2:'+-', 3:'++'}
    output_objs = []
    for col in range(4):
        info = [{"name": "tof", "units": "nanoseconds", "values": tof[:-1] },
            {"name": "xpixel", "units": "pixels", "values": twotheta_pixel[:-1] },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": pol_states[col], "filename": filename, "start_datetime": None, 
             "state": state, "CreationStory":creation_story, "path":path}]
        data_array = zeros((500, 256, 4))
        data_array[:,:,1] = 1.0 # pixels
        data_array[:,:,2] = monitor['microamphours_p%d' % (col,)]
        data_array[:,:,3] = 1.0 # count time
        data_array[:,:,0] = data[col,:,:]
        output_objs.append(MetaArray(data_array[:], dtype='float', info=info[:]))
    hdf_obj.close()
    return output_objs 


def SuperLoadAsterixHDF(filename, path=None, center_pixel = 145.0, wl_over_tof=1.9050372144288577e-5, pixel_width_over_dist = 0.0195458*pi/180.):
    """ loads an Asterix file and does the most common reduction steps, 
    giving back a length-4 list of data objects in twotheta-wavelength space,
    with the low-tof region shifted to the high-tof region """
    data_objs = LoadAsterixRawHDF(filename, path)
    tth_converted = AsterixPixelsToTwotheta().apply(data_objs, qzero_pixel=center_pixel, pw_over_d=pixel_width_over_dist)
    wl_converted = AsterixTOFToWavelength().apply(tth_converted, wl_over_tof=wl_over_tof)
    shifted = AsterixShiftData().apply(wl_converted, edge_bin=180)
    return shifted   

def LoadAsterixHDF(filename, path=None, center_pixel = 145.0, wl_over_tof=1.9050372144288577e-5):
    if path == None:
        path = os.getcwd()
    hdf_obj = h5py.File(os.path.join(path, filename))
    run_title = hdf_obj.keys()[0]
    run_obj = hdf_obj[run_title]
    state = hdf_to_dict(run_obj['ASTERIX'])
    print state
    monitor = hdf_to_dict(run_obj['scalars'])
    tof = run_obj['ordela_tof_pz']['tof'].value.astype(float64)
    twotheta_pixel = run_obj['ordela_tof_pz']['X'].value.astype(float64)
    data = run_obj['ordela_tof_pz']['data'].value.astype(float64)
    tof_to_wavelength_conversion = (0.019050372144288577 / 1000.)
    wavelength = (tof * wl_over_tof)[:-1]
    # shift by half-bin width to align to center of tof bins!
    wavelength += (tof[1] - tof[0])/2.0 * wl_over_tof 
    # (bins appear to be centered)
    shifted_data = empty(data.shape)
    shifted_data[:,:320,:] = data[:,-320:,:]
    shifted_data[:,320:,:] = data[:,:-320,:]
    shifted_wavelength = zeros(wavelength.shape)
    shifted_wavelength[:320] = wavelength[-320:]
    shifted_wavelength[320:] = wavelength[:-320] + (wavelength[-1] + wavelength[0])
    pixel_width_over_dist = 0.0195458*pi/180.
    twotheta_offset = float(state['A[0]'])
    twotheta = arctan2((twotheta_pixel - center_pixel) * pixel_width_over_dist, 1.0) * 180./pi + twotheta_offset
    print 'tth:', float(state['A[0]'])
    pol_states = {0:'--', 1:'-+', 2:'+-', 3:'++'}
    creation_story = "LoadAsterixHDF('{fn}')".format(fn=filename)
    #wavelength_axis = data_in[:,0,0]
    #twotheta_axis = data_in[0,:,1]
    output_objs = []
    for col in range(4):
        info = [{"name": "wavelength", "units": "Angstroms", "values": shifted_wavelength },
            {"name": "twotheta", "units": "degrees", "values": twotheta },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": pol_states[col], "filename": filename, "start_datetime": None, 
             "theta": float(state['A[1]']), "det_angle": float(state['A[0]']),
             "CreationStory":creation_story, "path":path}]
        data_array = zeros((500, 256, 4))
        data_array[:,:,1] = 1.0 # pixels
        data_array[:,:,2] = 1.0 # monitor
        data_array[:,:,3] = 1.0 # count time
        data_array[:,:,0] = shifted_data[col,:,:]
        output_objs.append(MetaArray(data_array[:], dtype='float', info=info[:]))
    return output_objs 

def LoadAsterixData(filename, path = None):
    if path == None:
        path = os.getcwd()
    pol_states = {2:'--', 3:'-+', 4:'+-', 5:'++'}  
    creation_story = "LoadAsterixData('{fn}')".format(fn=filename)
    data_in = loadtxt(os.path.join(path, filename)).reshape(500,256,6)
    wavelength_axis = data_in[:,0,0]
    twotheta_axis = data_in[0,:,1]
    output_objs = []
    for col in range(2,6):
        info = [{"name": "wavelength", "units": "Angstroms", "values": wavelength_axis },
            {"name": "twotheta", "units": "degrees", "values": twotheta_axis },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {"PolState": pol_states[col], "filename": filename, "start_datetime": None, 
             "CreationStory":creation_story, "path":path}]
        data_array = zeros((500, 256, 4))
        data_array[:,:,1] = 1.0 # pixels
        data_array[:,:,2] = 1.0 # monitor
        data_array[:,:,3] = 1.0 # count time
        data_array[:,:,0] = data_in[:,:,col]
        output_objs.append(MetaArray(data_array[:], dtype='float', info=info[:]))
    return output_objs    

def LoadICPData(filename, path=None, auto_PolState=False, PolState=''):
    """ 
    loads a data file into a MetaArray and returns that.
    Checks to see if data being loaded is 2D; if not, quits
    
    Need to rebin and regrid if the detector is moving...
    """
    lookup = {"a":"--", "b":"+-", "c":"-+", "d":"++", "g": ""}
    if path == None:
        path = os.getcwd()
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
    info = [{"name": "theta", "units": "degrees", "values": file_obj.sample.angle_x, "det_angle":file_obj.detector.angle_x },
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

class InsertTimestamps(Filter2D):
    """ This is a hack.  
    Get the timestamps from the source file directory listing
    and interpolate between the start time and the end time.
    """
    
    @autoApplyToList
    @updateCreationStory
    def apply(self, data, timestamps, override_existing=False, filename=None):
        # first of all, if there is already a timestamp, skip!
        #extra info changed
        if data._info[-1].has_key('end_datetime') and not override_existing:
            return data
        # now figure out which file was the source:
        new_info = data.infoCopy()
        source_filename = filename[1:] or new_info[-1]['filename'][1:] # strip off leading 'I'
        try:
            end_timestamp = timestamps[source_filename]
        except KeyError:
            print "source file 'last modified time' (mtime) not found"
            return
        end_datetime = datetime.datetime.fromtimestamp(end_timestamp)
        new_info[-1]['end_datetime'] = end_datetime
        new_data_array = data.view(ndarray).copy()
        new_data = MetaArray(new_data_array, info=new_info)
        return new_data       
    

class AppendPolarizationMatrix(Filter2D):
    """
    Takes a dataset with a defined polarization state (not None) and
    calculates the row of the NT matrix that corresponds to each datapoint
    (This is more straightforward for raw pixel data where the 
    timestamp is the same for all pixels in a single measurement 'point')
    """
        
    @autoApplyToList
    @updateCreationStory
    def apply(self, data, he3cell=None):
        """ can use He3AnalyzerCollection in place of He3Analyzer...
        then calls to getNTRow(t) get automatically routed to the correct cell object
        """
        #cell = self.supervisor.He3_cells[str(inData.cell_id)] # link to the cell object
        if he3cell == None:
            print "where is the He cell?"
            # extra info changed
            he3cell = He3AnalyzerCollection(path=data._info[-1]['path'])
        new_info = data.infoCopy()
        if not new_info[-1]['PolState'] in  ["--", "+-", "-+", "++"]:
            print "polarization state not defined: can't get correction matrix"
            return
        start_datetime = new_info[-1]['start_datetime']
        #start_time_offset = start_datetime - he3cell.start_datetime
        #offset_seconds = start_time_offset.days * 86400. + start_time_offset.seconds 
        # weird implementation of datetime difference measures in days, seconds, microseconds
        end_datetime = new_info[-1]['end_datetime']
        elapsed = end_datetime - start_datetime
        datalen = data.shape[0]
        delta_t = elapsed / datalen 
        #el_seconds = el.days * 86400. + el.seconds # datetime timedelta is an odd duck

        
        time_list = [start_datetime + delta_t * i for i in range(datalen)]
        #time_array += offset_seconds # get total time from cell T0
        #time_array.shape += (1,)
        
        data_array = data.view(ndarray).copy()
        new_data_array = zeros(data_array.shape[:-1] + (data_array.shape[-1] + 4,))
        new_data_array[:, :, 0:-4] = data_array[:]
        PolState = new_info[-1]['PolState']
        flipper_on = (PolState[0] == '-') # check for flipper on in incoming polarization state
        He3_up = (PolState[1] == '+')
        for i in range(datalen):
            t = start_datetime + delta_t * i
            #print 't: ', t
            pol_corr = he3cell.getNTRow(t, flipper_on=flipper_on, He3_up=He3_up)
            monitor_row = data['Measurements':'monitor'][i].view(ndarray).copy()
            # NT is multiplied by I_0, or monitor in this case:
            new_data_array[i, :, -4:] = pol_corr[newaxis, :] * monitor_row[:, newaxis]
            
            
        #pol_corr_list = [he3cell.getNTRow(t, flipper_on = flipper_on, He3_up = He3_up) for t in time_list]
        #pol_corr_array = array(pol_corr_list)

        #fill the first four columns with existing data:
        
        #1new_data_array[:,:,0:4] = data_array[:,:,0:4]
        
        # now append the polarization matrix elements!
        # from He3Analyzer: 
        # """creates matrix elements for the polarization-correction 
        #    this assumes the order of elements is Rup-up, Rup-down, Rdown-down, Rdown-up
        #    and for I: Iup-up, Iup-down, Idown-up, Idown-down   """
        
        #1new_data_array[:,:,4:8] = pol_corr_array[newaxis, newaxis, :]
        
        # the order of columns here is determined by the order coming out of He3Analyer NTRow:
        # (++, +-, --, -+)
        pol_columns = [{"name": 'NT++'}, {"name": 'NT+-'}, {"name": 'NT--'}, {"name": 'NT-+'}]
        new_info[2]["cols"] = new_info[2]["cols"][:4] + pol_columns
        new_data = MetaArray(new_data_array, info=new_info)
        
        return new_data



class Combine(Filter2D):
    """ combine multiple datasets with or without overlap, adding 
    all the values in the time, monitor and data columns, and populating
    the pixels column (number of pixels in each new bin)
    
    If no grid is provided, use Autogrid filter to generate one.
    """
    #@updateCreationStory
    def apply(self, list_of_datasets, grid=None):
        if grid == None:
            grid = Autogrid().apply(list_of_datasets)
        for dataset in list_of_datasets:
            grid = self.add_to_grid(dataset, grid)
        
        # extra info changed
        old_creation_stories = "[" + "".join([data._info[-1]['CreationStory'] + ", " for data in list_of_datasets]) + "]"
        name = self.__class__.__name__
        new_creation_story = "{fname}().apply({oldcs})".format(fname=name, oldcs=old_creation_stories)
        grid._info[-1]['CreationStory'] = new_creation_story
        # strip info that is meaningless in combined dataset: (filename, start_time, end_time)
        for key in ['filename', 'start_datetime', 'end_datetime']:
            if grid._info[-1].has_key(key): grid._info[-1].pop(key)
        return grid
        
    def add_to_grid(self, dataset, grid):
        dims = 2
        bin_edges = []
        for dim in range(dims):
            av = grid.axisValues(dim).copy()
            dspacing = (av.max() - av.min()) / (len(av) - 1)
            edges = resize(av, len(av) + 1)
            edges[-1] = av[-1] + dspacing
            bin_edges.append(edges)
        
        data_edges = []
        for dim in range(dims):
            av = dataset.axisValues(dim).copy()
            dspacing = (av.max() - av.min()) / (len(av) - 1)
            edges = resize(av, len(av) + 1)
            edges[-1] = av[-1] + dspacing
            data_edges.append(edges)
        
        cols_to_add = ['counts', 'pixels', 'monitor', 'count_time'] # standard data columns
        cols_to_add += ['NT++', 'NT+-', 'NT-+', 'NT--'] # add in all the polarization correction matrices too!
        
        new_info = dataset.infoCopy()        
        for i, col in enumerate(new_info[2]['cols']):
            if col['name'] in cols_to_add:
                array_to_rebin = dataset[:, :, col['name']].view(ndarray) 
                new_array = reb.rebin2d(data_edges[0], data_edges[1], array_to_rebin, bin_edges[0], bin_edges[1])
                grid[:, :, col['name']] += new_array
                
        return grid

class CombinePolarized(Filter2D):
    """ 
    Combines on a per-polarization state basis.
    Master output grid is calculated that will cover ALL the inputs,
    without regard for polarization state, but then separate
    copies of this grid are filled with data from each
    PolState separately.
    """

    def sortByPolarization(self, list_of_datasets):
        """ takes an unsorted list of datasets, peeks at the PolState inside,
        and groups them into a labeled list of lists (dictionary!)"""
        pol_datasets = {}
        for dataset in list_of_datasets:
            # extra info changed
            PolState = dataset._info[-1].get('PolState', '')
            if not PolState in pol_datasets.keys():
                pol_datasets[PolState] = []
            pol_datasets[PolState].append(dataset)
        return pol_datasets
        
    def getListOfDatasets(self, pol_datasets):
        """ inverse of sortByPolarization: take a dictionary of PolState-grouped
        data and return a flat list of every dataset inside """
        list_of_datasets = []
        for PolState in pol_datasets:
            list_of_datasets += pol_datasets[PolState]
        return list_of_datasets
                
    
    def apply(self, pol_datasets, grid=None):
        if type(pol_datasets) is types.ListType:
            # then we got an unordered list of polarized datasets.
            # that's ok - we can label and group them together!
            list_of_datasets = pol_datasets
            pol_datasets = self.sortByPolarization(pol_datasets)
        else:
            list_of_datasets = self.getListOfDatasets(pol_datasets)
                
        if grid == None:
            grid = Autogrid().apply(list_of_datasets)
        # grid covering all polstates is now made:  now create
        # sublists for each polarization state
        
        combined_datasets = []
        for PolState in pol_datasets:
            # combined single polarization:
            csingle = Combine().apply(pol_datasets[PolState], deepcopy(grid))
            #print type(pol_datasets[PolState])
            #extra info changed
            csingle._info[-1]['PolState'] = PolState
            combined_datasets.append(csingle)
        # we end up with a dictionary set of datasets (e.g. {"++": data1, "--": data2} )
        
        return combined_datasets

class TwothetaLambdaToQxQz(Filter2D):
    """ Figures out the Qx, Qz values of each datapoint
    and throws them in the correct bin.  If no grid is specified,
    one is created that covers the whole range of Q in the dataset
    
    If autofill_gaps is True, does reverse lookup to plug holes
    in the output (but pixel count is still zero for these bins)
    """
    
    default_qxqz_gridvals = (-0.003, 0.003, 201, 0, 0.1, 201)
    
    def getQxQz (self, theta, twotheta, wavelength = 5.0): 
        qLength = 2.0 * pi / wavelength
        tilt = theta - ( twotheta / 2.0 )
        dq = 2.0 * qLength * sin( ( pi / 180.0 ) * ( twotheta / 2.0 ) )
        qxOut = dq * sin( pi * tilt / 180.0 )
        qzOut = dq * cos( pi * tilt / 180.0 )
        return [qxOut, qzOut]
    
    @autoApplyToList
    #@updateCreationStory
    def apply(self, data, output_grid=None, theta=None):
        if output_grid == None:
            output_grid = EmptyQxQzGrid(*self.default_qxqz_gridvals)
        else:
            output_grid = deepcopy(output_grid)
            
        if theta == None:
            if 'theta' in data._info[-1]:
                theta = data._info[-1]['theta']
            else:
                print "can't run without theta!"
                return
       
        wl_array = data.axisValues('wavelength').copy()
        wl_array.shape = wl_array.shape + (1,)
        twotheta_array = data.axisValues('twotheta').copy()
        twotheta_array.shape = (1,) + twotheta_array.shape
        qxOut, qzOut = self.getQxQz(theta, twotheta_array, wl_array)
        
        # getting values from output grid:
        outgrid_info = output_grid.infoCopy()
        numcols = len(outgrid_info[2]['cols'])
        qx_array = output_grid.axisValues('qx')
        dqx = qx_array[1] - qx_array[0]
        qz_array = output_grid.axisValues('qz')
        dqz = qz_array[1] - qz_array[0]
        framed_array = zeros((qz_array.shape[0]+2, qx_array.shape[0]+2, numcols))
        target_qx = ((qxOut - qx_array[0])/dqx + 1).astype(int)
        #return target_qx, qxOut
        target_qz = ((qzOut - qz_array[0])/dqz + 1).astype(int)
        target_mask = (target_qx >= 0) * (target_qx < qx_array.shape[0])
        target_mask *= (target_qz >= 0) * (target_qz < qz_array.shape[0])
        target_qx_list = target_qx[target_mask]
        target_qz_list = target_qz[target_mask]
        #target_qx = target_qx.clip(0, qx_array.shape[0]+1)
        #target_qz = target_qz.clip(0, qz_array.shape[0]+1)
        
        for i, col in enumerate(outgrid_info[2]['cols']):
            values_to_bin = data[:,:,col['name']][target_mask]
            outshape = (output_grid.shape[0], output_grid.shape[1])
            hist2d, xedges, yedges = histogram2d(target_qx_list,target_qz_list, bins = (outshape[0],outshape[1]), range=((0,outshape[0]),(0,outshape[1])), weights=values_to_bin)
            output_grid[:,:,col['name']] += hist2d
            #framed_array[target_qz_list, target_qx_list, i] = data[:,:,col['name']][target_mask]
            
        #trimmed_array = framed_array[1:-1, 1:-1]
        #output_grid[:,:] = trimmed_array
        
        creation_story = data._info[-1]['CreationStory']
        new_creation_story = creation_story + ".filter('{0}', {1})".format(self.__class__.__name__, output_grid._info[-1]['CreationStory'])
        #print new_creation_story
        output_grid._info[-1] = data._info[-1].copy()
        output_grid._info[-1]['CreationStory'] = new_creation_story
        return output_grid
              
class ThetaTwothetaToQxQz(Filter2D):
    """ Figures out the Qx, Qz values of each datapoint
    and throws them in the correct bin.  If no grid is specified,
    one is created that covers the whole range of Q in the dataset
    
    If autofill_gaps is True, does reverse lookup to plug holes
    in the output (but pixel count is still zero for these bins)
    """
    
    default_qxqz_gridvals = (-0.003, 0.003, 201, 0, 0.1, 201)
    
    @autoApplyToList
    #@updateCreationStory
    def apply(self, data, output_grid=None, wavelength=5.0):
        if output_grid == None:
            output_grid = EmptyQxQzGrid(*self.default_qxqz_gridvals)
        
        qLength = 2.0 * pi / wavelength
        th_array = data.axisValues('theta').copy()
        th_array.shape = th_array.shape + (1,)
        twotheta_array = data.axisValues('twotheta').copy()
        twotheta_array.shape = (1,) + twotheta_array.shape
        tilt_array = th_array - (twotheta_array / 2.0)
        qxOut = 2.0 * qLength * sin((pi / 180.0) * (twotheta_array / 2.0)) * sin(pi * tilt_array / 180.0)
        qzOut = 2.0 * qLength * sin((pi / 180.0) * (twotheta_array / 2.0)) * cos(pi * tilt_array / 180.0)
        
        # getting values from output grid:
        outgrid_info = output_grid.infoCopy()
        numcols = len(outgrid_info[2]['cols'])
        qx_array = output_grid.axisValues('qx')
        dqx = qx_array[1] - qx_array[0]
        qz_array = output_grid.axisValues('qz')
        dqz = qz_array[1] - qz_array[0]
        framed_array = zeros((qz_array.shape[0] + 2, qx_array.shape[0] + 2, numcols))
        target_qx = ((qxOut - qx_array[0]) / dqx + 1).astype(int)
        #return target_qx, qxOut
        target_qz = ((qzOut - qz_array[0]) / dqz + 1).astype(int)
        
        target_mask = (target_qx >= 0) * (target_qx < qx_array.shape[0])
        target_mask *= (target_qz >= 0) * (target_qz < qz_array.shape[0])
        target_qx_list = target_qx[target_mask]
        target_qz_list = target_qz[target_mask]
        #target_qx = target_qx.clip(0, qx_array.shape[0]+1)
        #target_qz = target_qz.clip(0, qz_array.shape[0]+1)
        
        for i, col in enumerate(outgrid_info[2]['cols']):
            values_to_bin = data[:,:,col['name']][target_mask]
            outshape = (output_grid.shape[0], output_grid.shape[1])
            hist2d, xedges, yedges = histogram2d(target_qx_list,target_qz_list, bins = (outshape[0],outshape[1]), range=((0,outshape[0]),(0,outshape[1])), weights=values_to_bin)
            output_grid[:,:,col['name']] += hist2d
            #framed_array[target_qz_list, target_qx_list, i] = data[:,:,col['name']][target_mask]
     
        #extra info changed
        creation_story = data._info[-1]['CreationStory']
        new_creation_story = creation_story + ".filter('{0}', {1})".format(self.__class__.__name__, output_grid._info[-1]['CreationStory'])
        #print new_creation_story
        output_grid._info[-1] = data._info[-1].copy()
        output_grid._info[-1]['CreationStory'] = new_creation_story
        return output_grid

class PolarizationCorrect(Filter2D):
    """ 
    Takes 2 to 4 input datasets with appended Polarization Matrix, 
    inverts the polarization matrix and applies to the data.
    Outputs fully polarization-corrected intensities.
    
    # 0: "no assumptions (use all I++, I+-, I-+, I--)",
    # 1: "R+- assumed equal to R-+ (use I++, I-+ and I--)",
    # 2: "R-+ assumed equal to R+- (use I++, I+- and I--)",
    # 3: "R-+ and R+- equal zero (use I++, I--)"
    
    Requires that Polarization state is defined for each dataset ("PolState")
    and that at least "++" and "--" PolStates are present.
    """
    
    polstate_order = {'++':0, '+-':1, '-+':2, '--':3}
    
    def progress_update(self, percent_done):
        print '{0}% done'.format(percent_done)
        
    def check_grids(self, datasets):
        """ Combined data will be dictionary of labeled datasets: 
        e.g. {"++": datapp, "+-": datapm} etc."""
        compatible = True
        firstdata = datasets[0]
        for dataset in datasets[1:]:
            # allclose is the next best thing to "==" for a floating point array
            compatible &= allclose(dataset.axisValues(0), firstdata.axisValues(0))
            compatible &= allclose(dataset.axisValues(1), firstdata.axisValues(1))
        return compatible
    
    def guess_assumptions(self, datasets):
        assumptions = None
        polstates = [datum._info[-1]['PolState'] for datum in datasets]
        if set(polstates) == set(["++", "+-", "-+", "--"]):
            assumptions = 0
        elif set(polstates) == set(["++", "-+", "--"]):
            assumptions = 1
        elif set(polstates) == set(["++", "+-", "--"]):
            assumptions = 2
        elif set(polstates) == set(["++", "--"]):
            assumptions = 3
        return assumptions
        
    def apply(self, combined_data, assumptions=0, auto_assumptions=True):
        # do I apply assumptions here, or in separate subclasses?
        if auto_assumptions:
            assumptions = self.guess_assumptions(combined_data)
            print "assumptions: ", assumptions
            
        if not self.check_grids(combined_data):
            # binning on datasets in combined data is not the same!  quit.
            return
            
        data_shape = combined_data[0].shape
        polstates = [datum._info[-1]['PolState'] for datum in combined_data]
            
        NT = empty(data_shape[:2] + (4, 4))
        alldata = empty(data_shape[:2] + (len(polstates), 4))
        # recall order of I, R is different for the way we've set up NT matrix (not diagonal)
        # [Iuu, Iud, Idu, Idd] but [Ruu, Rud, Rdd, Rdu]
        #['NT++','NT+-','NT--','NT-+']
        for dataset in combined_data:
            PolState = dataset._info[-1]['PolState']
            NT[:, :, self.polstate_order[PolState]] = dataset[:, :, ['NT++', 'NT+-', 'NT-+', 'NT--']]
            alldata[:, :, self.polstate_order[PolState]] = dataset[:, :, ['counts', 'pixels', 'monitor', 'count_time']]
            #alldata[:,:,self.polstate_order[PolState]] = combined_data[PolState][:,:,['counts','pixels','monitor','count_time']]
        # should result in: 
        #NT[:,:,0] = combined_data['++'][:,:,['NT++','NT+-','NT-+','NT--']]
        #NT[:,:,1] = combined_data['+-'][:,:,['NT++','NT+-','NT-+','NT--']]
        #NT[:,:,2] = combined_data['-+'][:,:,['NT++','NT+-','NT-+','NT--']]
        #NT[:,:,3] = combined_data['--'][:,:,['NT++','NT+-','NT-+','NT--']]
        #alldata[:,:,0] = combined_data['++'][:,:,['counts','pixels','monitor','count_time']]
        #alldata[:,:,1] = combined_data['+-'][:,:,['counts','pixels','monitor','count_time']]
        #alldata[:,:,2] = combined_data['-+'][:,:,['counts','pixels','monitor','count_time']]
        #alldata[:,:,3] = combined_data['--'][:,:,['counts','pixels','monitor','count_time']]
        # by arranging this new NT matrix as above, I'm undoing the weird arrangement in
        # the He3Analyzer module.  now the order is: 
        # [Iuu, Iud, Idu, Idd] AND [Ruu, Rud, Rdu, Rdd] !!!
        output_columns = {'++':0, '+-':1, '-+':2, '--':3}        
        
        if assumptions == 1:
            NT = NT[:, :, [0, 2, 3], :] #remove +- (second) row
            NT[:, :, :, 1] += NT[:, :, :, 2] # add -+(column 3) to +- (column 2), (cols. 1 and 2 in zero-indexed)
            NT = NT[:, :, :, [0, 1, 4]] # drop column 3 (2 in zero-indexing)
            # should now be (th_len, 2th_len, 3, 3) matrix
            output_columns = {'++':0, '-+':1, '--':2} 
        
        elif assumptions == 2:
            NT = NT[:, :, [0, 1, 3], :] #remove -+ (third) row
            NT[:, :, :, 1] += NT[:, :, :, 2] # add -+ column 3 to +- column 2 (zero-indexed)
            NT = NT[:, :, :, [0, 1, 4]] # drop column 3 (2 in zero-indexing)
            # should now be (th_len, 2th_len, 3, 3) matrix
            output_columns = {'++':0, '+-':1, '--':2} 
            
        elif assumptions == 3:
            NT = NT[:, :, [0, 3], :] #remove both middle rows
            NT = NT[:, :, :, [0, 3]] # remove both middle columns (1,2 in zero-indexing)
            # should now be (th_len, 2th_len, 2, 2) matrix
            output_columns = {'++':0, '--':1} 
 
        R = deepcopy(alldata)
        # output will have the same shape as input... just with different values!
        
        invNT = zeros_like(NT)
        normNT = zeros(data_shape[:2])
        
        n = 0
        percent_done = -1
        nmax = NT.shape[0] * NT.shape[1]
        #return NT
        
        for i in range(NT.shape[0]):
            for j in range(NT.shape[1]):
                try:
                    invNT[i, j] = linalg.inv(NT[i, j])
                    normNT[i, j] = linalg.norm(invNT[i, j])
                    R[i, j, :, 0] = dot(invNT[i, j], alldata[i, j, :, 0]) # counts
                    R[i, j, :, 1] = dot(invNT[i, j], alldata[i, j, :, 1]) / normNT[i, j] # pixels (need unitary transform)
                    R[i, j, :, 2] = 1.0 # monitor is set to one.  Not sure about this one
                    R[i, j, :, 3] = 1.0 # count time is set to one also.
                except:
                    print sys.exc_info()
                    sys.exit()
                    R[i, j, :, 0] = 0.0 # counts
                    R[i, j, :, 1] = 0.0 # pixels (need unitary transform)
                    R[i, j, :, 2] = 1.0 # monitor is set to one.  Not sure about this one
                    R[i, j, :, 3] = 1.0 # count time is set to one also.
                    # this leaves zeros where the inversion fails
                    # not sure what else to do!
                n += 1
                new_percent_done = (100 * n) / nmax
                if new_percent_done > percent_done:
                    self.progress_update(new_percent_done)
                    percent_done = new_percent_done
                    
        combined_R = []
        for index, PolState in enumerate(polstates):
            combined_R.append(MetaArray(R[:, :, output_columns[PolState]], info=combined_data[index].infoCopy()))
        return combined_R
            
    def add_to_grid(self, dataset, grid):
        dims = 2
        bin_edges = []
        for dim in range(dims):
            av = grid.axisValues(dim).copy()
            dspacing = (av.max() - av.min()) / (len(av) - 1)
            edges = resize(av, len(av) + 1)
            edges[-1] = av[-1] + dspacing
            bin_edges.append(edges)
        
        data_edges = []
        for dim in range(dims):
            av = dataset.axisValues(dim).copy()
            dspacing = (av.max() - av.min()) / (len(av) - 1)
            edges = resize(av, len(av) + 1)
            edges[-1] = av[-1] + dspacing
            data_edges.append(edges)
        
        cols_to_add = ['counts', 'pixels', 'monitor', 'count_time'] # standard data columns
        cols_to_add += ['NT++', 'NT+-', 'NT-+', 'NT--'] # add in all the polarization correction matrices too!
        
        new_info = dataset.infoCopy()        
        for i, col in enumerate(new_info[2]['cols']):
            if col['name'] in cols_to_add:
                array_to_rebin = dataset[:, :, col['name']].view(ndarray) 
                new_array = reb.rebin2d(data_edges[0], data_edges[1], array_to_rebin, bin_edges[0], bin_edges[1])
                grid[:, :, col['name']] += new_array
                
        return grid

class wxPolarizationCorrect(PolarizationCorrect):
    
    def apply(self, *args, **kwargs):
        self.progress_meter = wx.ProgressDialog("Progress", "% done", parent=None, style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL) 
        return PolarizationCorrect.apply(self, *args, **kwargs)
        
    def progress_update(self, percent_done): 
        self.progress_meter.Update(int(percent_done), "Polarization Correction Progress:\n{0}% done".format(percent_done))

class Subtract(Filter2D):
    """ takes two data objects and subtracts them. """
    def apply(self, data1, data2):
        new_grid = Autogrid().apply([data1, data2])
        # need to figure out overlap somehow
        
          
class CombinePolcorrect(Filter2D):
    """ combine and polarization-correct """
    def apply(self, list_of_datasets, grid=None):
        pass

# rowan tests
if __name__ == '__main__':
    data1 = LoadICPData('Isabc2003.cg1', '/home/brendan/dataflow/sampledata/ANDR/sabc/')
    data2 = LoadICPData('Isabc2004.cg1', '/home/brendan/dataflow/sampledata/ANDR/sabc/')
    data = [data1, data2]
    data = Combine().apply(data)
    data = data.filter('CoordinateOffset', offsets={'theta': 0.1})
    data = data.filter('WiggleCorrection')
    print data
    #print data._info[-1]["CreationStory"]
    #print eval(data._info[-1]["CreationStory"])
    #print data
    assert data.all() == eval(data._info[-1]["CreationStory"]).all()

