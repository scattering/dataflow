from numpy import cos, pi, cumsum, arange, ndarray, ones, zeros, array, newaxis, linspace, empty
import os, simplejson, datetime
import types
from copy import deepcopy
from FilterableMetaArray import FilterableMetaArray as MetaArray
from He3Analyzer import wxHe3AnalyzerCollection as He3AnalyzerCollection
import reflectometry.reduction as red
from reflectometry.reduction import rebin as reb
#import get_timestamps
import xml.dom.minidom

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

    def AddRebinnedData(self, new_object, name='', base_data_obj = None):  
        self.rebinned_data_objects.append(new_object)
        new_object.number = self.rb_count
        self.rb_count += 1
    
    def AddPlottable2dData(self, new_object, parent = None, name='', base_data_obj = None):
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
        creation_story +=  "({0}, {1}, {2}, {3}, {4}, {5})".format(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
        info = [{"name": "qz", "units": "inv. Angstroms", "values": linspace(qzmin, qzmax, qzbins) },
            {"name": "qx", "units": "inv. Angstroms", "values": linspace(qxmin, qxmax, qxbins) },
            {"name": "Measurements", "cols": [
                    {"name": "counts"},
                    {"name": "pixels"},
                    {"name": "monitor"},
                    {"name": "count_time"}]},
            {'CreationStory': creation_story}]
        data = MetaArray((qzbins, qxbins, 4), info=info)
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
    
    def updateCreationStory(apply):
        """ 
        decorator for 'apply' method - it updates the Creation Story
        for each filter application.
        """
        
        def newfunc(self, data, *args, **kwargs):
            result = apply(self, *args, **kwargs)
            name = self.__class__.__name__
            new_info = result.infoCopy()
            new_type = result.dtype
            new_data = result.view(ndarray)
            new_args = "".join([', {arg}'.format(arg=arg) for arg in args])
            new_kwargs = "".join([', {key}={value}'.format(key=key, value=kwargs[key]) for key in kwargs])
            new_creation_story = "{old_cs}.filter('{fname}', {args}, {kwargs})".format(old_cs=old_cs, fname=name, args=new_args, kwargs=new_kwargs)
            #print new_creation_story
            #new_info[-1]["CreationStory"]
            return result
        return newfunc
    
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
    def apply(self, data, offsets = {}):
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
        widthCorrection = ( wiggleAmplitude * cos( 2.0 * pi * xpixel / 32.0 ) )
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

class PixelsToTwotheta(Filter2D):
    """ input array has axes theta and pixels:
    output array has axes theta and twotheta.
    
    Pixel-to-angle conversion is arithmetic (pixels-per-degree=constant)
    output is rebinned to fit in a rectangular array if detector angle 
    is not fixed. """
    
    @autoApplyToList
    @updateCreationStory 
    def apply(self, data, pixels_per_degree=80.0, qzero_pixel=309, instr_resolution = 1e-6):
        new_info = data.infoCopy()
        det_angle = new_info[0].pop('det_angle') # read and get rid of it!
        th_vector = data.axisValues('theta')
        th_spacing = th_vector[1] - th_vector[0]
        pixels = data.axisValues('xpixel')
        twoth = -1.0 * (pixels - qzero_pixel) / pixels_per_degree
        twoth_min = det_angle.min() + twoth.min()
        twoth_max = det_angle.max() + twoth.max()
        twoth_max_edge = twoth_max + 1.0 / pixels_per_degree
        dpp = 1.0/pixels_per_degree
        output_twoth_bin_edges = arange(twoth_max + dpp, twoth_min - dpp, -dpp)
        output_twoth = output_twoth_bin_edges[:-1]
        
        #input_twoth_bin_edges = output_twoth_bin_edges.copy()
        #input_twoth_bin_edges[:-1] = twoth
        th_bin_edges = linspace(th_vector[0], th_vector[-1]+th_spacing, len(th_vector) + 1)
        new_info[1]['name'] = 'twotheta' # getting rid of pixel units: substitute twoth
        new_info[1]['values'] = output_twoth
        new_info[1]['units'] = 'degrees'
        new_data = MetaArray((len(th_vector), len(output_twoth), data.shape[2]), info=new_info) # create the output data object!
        # (still has to be filled with correct values)
                       
        if ( (det_angle.max() - det_angle.min() ) < instr_resolution ):
            #then the detector is fixed and we can pass a single 2theta vector to rebin2d
            input_twoth_bin_edges = empty(len(pixels) + 1)
            input_twoth_bin_edges[0] = twoth_max + 1.0/pixels_per_degree
            input_twoth_bin_edges[1:] = twoth + det_angle.min()
            data_cols = ['counts', 'pixels', 'monitor', 'count_time']
            for col in data_cols:
                array_to_rebin = data[:,:,col].view(ndarray).copy() 
                new_array = reb.rebin2d(th_bin_edges,input_twoth_bin_edges,array_to_rebin,th_bin_edges,output_twoth_bin_edges)
                new_data[:,:,col] = new_array
        else:
            #then the detector is not fixed, and we have to pass in each A4 value at a time to rebin
            tth_min = twoth.min()
            tth_max = twoth.max()
            for i, da in enumerate(det_angle):
                twoth_min = da + tth_min
                twoth_max = da + tth_max
                input_twoth_bin_edges = empty(len(pixels) + 1)
                input_twoth_bin_edges[0] = twoth_max + 1.0/pixels_per_degree
                input_twoth_bin_edges[1:] = twoth + da         
                data_cols = ['counts', 'pixels', 'monitor', 'count_time']
                for col in data_cols:
                    array_to_rebin = data[i,:,col].view(ndarray).copy()
                    new_array = reb.rebin(input_twoth_bin_edges,array_to_rebin,output_twoth_bin_edges)
                    new_data[i,:,col] = new_array
                
        return new_data

class Autogrid(Filter2D):
    """ take multiple datasets and create a grid which covers all of them
    - stepsize is smallest stepsize found in datasets
    returns an empty grid with units and labels
    
    if extra_grid_point is True, adds one point to the end of each axis
    so each dimension is incremented by one (makes edges for rebinning) """
    
    def apply(self, list_of_datasets, extra_grid_point = True, min_step = 1e-10):
        num_datasets = len( list_of_datasets )
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
            new_info[dim]["values"] = (arange(output_dims[dim], dtype='float')*final_stepsizes[dim]) + absolute_min[dim]
        output_grid = MetaArray(tuple(output_dims), info=new_info)
        return output_grid
        
    
    
class ICPDataFromFile(MetaArray):
    default_path = None
       
    def __new__(subtype, filename, path = None, auto_PolState=False, PolState=''):
        """ 
        loads a data file into a MetaArray and returns that.
        Checks to see if data being loaded is 2D; if not, quits
        
        Need to rebin and regrid if the detector is moving...
        """
        lookup = {"a":"--", "b":"+-", "c":"-+", "d":"++", "g": ""}
        if path == None:
            path = subtype.default_path
        if path == None:
            path = os.getcwd()
        subtype.default_path = path
        Filter2D.default_path = path
        
        def new_single(filename, path, auto_PolState, PolState):
            file_obj = red.load(os.path.join(path, filename))
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
            creation_story = "ICPDataFromFile('{fn}'".format(fn=filename)
            if not PolState == '':
                creation_story += ", PolState='{0}'".format(PolState)
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
            data_array[:,:,0] = file_obj.detector.counts
            data_array[:,:,1] = 1
            data_array[:,:,2] = mon
            data_array[:,:,3] = count_time
            # data_array[:,:,4]... I wish!!!  Have to do by hand.
            data = MetaArray(data_array, dtype='float', info=info)
            return data
        
        if type(filename) is types.ListType:
            result = [new_single(fn, path, auto_PolState, PolState) for fn in filename]
            return result
        else:
            return new_single(filename, path, auto_PolState, PolState)
        

def LoadICPData(filename, path = None, auto_PolState=False, PolState=''):
    """ 
    loads a data file into a MetaArray and returns that.
    Checks to see if data being loaded is 2D; if not, quits
    
    Need to rebin and regrid if the detector is moving...
    """
    lookup = {"a":"--", "b":"+-", "c":"-+", "d":"++", "g": ""}
    if path == None:
        path = os.getcwd()
    file_obj = red.load(os.path.join(path, filename))
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
    creation_story = "LoadICPData('{fn}'".format(fn=filename)
    if not PolState == '':
        creation_story += ", PolState='{0}'".format(PolState)
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
    data_array[:,:,0] = file_obj.detector.counts
    data_array[:,:,1] = 1
    data_array[:,:,2] = mon
    data_array[:,:,3] = count_time
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
    def apply(self, data, timestamp_file='end_times.json', regenerate_end_times = False, override_existing = False):
        # first of all, if there is already a timestamp, skip!
        if data.extrainfo.has_key('end_datetime') and not override_existing:
            return data
        path = data.extrainfo['path']
        fn = os.path.join(path, timestamp_file)
        if regenerate_end_times:
            timestamps = get_timestamps.load_timestamps()
        else:
            timestamps = simplejson.load(open(fn, 'r'))
            
        # now figure out which file was the source:
        new_info = data.infoCopy()
        source_filename = new_info[-1]['filename'][1:] # strip off leading 'I'
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
            he3cell = He3AnalyzerCollection(path = data.extrainfo['path'])
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
        new_data_array = zeros( data_array.shape[:-1] + (data_array.shape[-1] + 4,))
        new_data_array[:,:,0:-4] = data_array[:]
        PolState = new_info[-1]['PolState']
        flipper_on = (PolState[0] == '-') # check for flipper on in incoming polarization state
        He3_up = (PolState[1] == '+')
        for i in range(datalen):
            t = start_datetime + delta_t * i
            #print 't: ', t
            pol_corr = he3cell.getNTRow(t, flipper_on = flipper_on, He3_up = He3_up)
            monitor_row = data['Measurements':'monitor'][i].view(ndarray).copy()
            # NT is multiplied by I_0, or monitor in this case:
            new_data_array[i,:,-4:] = pol_corr[newaxis, :] * monitor_row[:,newaxis]
            
            
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
    def apply(self, list_of_datasets, grid = None):
        if grid == None:
            grid = Autogrid().apply(list_of_datasets)
        for dataset in list_of_datasets:
            grid = self.add_to_grid(dataset, grid)
        
        old_creation_stories = "[" + "".join([data.extrainfo['CreationStory']+", " for data in list_of_datasets]) + "]"
        name = self.__class__.__name__
        new_creation_story = "{fname}().apply({oldcs})".format(fname=name, oldcs = old_creation_stories)
        grid.extrainfo['CreationStory'] = new_creation_story
        # strip info that is meaningless in combined dataset: (filename, start_time, end_time)
        for key in ['filename', 'start_datetime', 'end_datetime']:
            if grid.extrainfo.has_key(key): grid.extrainfo.pop(key)
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
        cols_to_add += ['NT++','NT+-','NT-+','NT--'] # add in all the polarization correction matrices too!
        
        new_info = dataset.infoCopy()        
        for i, col in enumerate(new_info[2]['cols']):
            if col['name'] in cols_to_add:
                array_to_rebin = dataset[:,:,col['name']].view(ndarray) 
                new_array = reb.rebin2d(data_edges[0],data_edges[1],array_to_rebin,bin_edges[0],bin_edges[1])
                grid[:,:,col['name']] += new_array
                
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
            PolState = dataset.extrainfo.get('PolState', '')
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
                
    
    def apply(self, pol_datasets, grid = None):
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
        
        combined_datasets = {}
        for PolState in pol_datasets:
            # combined single polarization:
            csingle = Combine().apply(pol_datasets[PolState], deepcopy(grid))
            #print type(pol_datasets[PolState])
            csingle.extrainfo['PolState'] = PolState
            combined_datasets[PolState] = csingle
        # we end up with a dictionary set of datasets (e.g. {"++": data1, "--": data2} )
        
        return combined_datasets
              
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
        tilt_array = th_array - ( twotheta_array / 2.0 )
        qxOut = 2.0 * qLength * sin( ( pi / 180.0 ) * ( twotheta_array / 2.0 ) ) * sin( pi * tilt_array / 180.0 )
        qzOut = 2.0 * qLength * sin( ( pi / 180.0 ) * ( twotheta_array / 2.0 ) ) * cos( pi * tilt_array / 180.0 )
        
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
        target_qx = target_qx.clip(0, qx_array.shape[0]+1)
        target_qz = target_qz.clip(0, qz_array.shape[0]+1)
        
        for i, col in enumerate(outgrid_info[2]['cols']):
            framed_array[target_qz, target_qx, i] = data[:,:,col['name']]
            
        trimmed_array = framed_array[1:-1, 1:-1]
        output_grid[:,:] = trimmed_array
        
        creation_story = data.extrainfo['CreationStory']
        new_creation_story = creation_story + ".filter('{0}', {1})".format(self.__class__.__name__, output_grid.extrainfo['CreationStory'])
        #print new_creation_story
        output_grid.extrainfo = data.extrainfo.copy()
        output_grid.extrainfo['CreationStory'] = new_creation_story
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
        
    def check_grids(self, combined_data):
        """ Combined data will be dictionary of labeled datasets: 
        e.g. {"++": datapp, "+-": datapm} etc."""
        compatible = True
        datasets = combined_data.values()
        firstdata = datasets[0]
        for dataset in datasets[1:]:
            # allclose is the next best thing to "==" for a floating point array
            compatible &= allclose(dataset.axisValues(0), firstdata.axisValues(0))
            compatible &= allclose(dataset.axisValues(1), firstdata.axisValues(1))
        return compatible
    
    def guess_assumptions(self, combined_data):
        assumptions = None
        polstates = combined_data.keys()
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
            
        data_shape = combined_data.values()[0].shape
        polstates = combined_data.keys()
            
        NT = empty(data_shape[:2] + (4,4))
        alldata = empty(data_shape[:2] + (len(polstates),4))
        # recall order of I, R is different for the way we've set up NT matrix (not diagonal)
        # [Iuu, Iud, Idu, Idd] but [Ruu, Rud, Rdd, Rdu]
        #['NT++','NT+-','NT--','NT-+']
        for PolState in combined_data:
            NT[:,:,self.polstate_order[PolState]] = combined_data[PolState][:,:,['NT++','NT+-','NT-+','NT--']]
            alldata[:,:,self.polstate_order[PolState]] = combined_data[PolState][:,:,['counts','pixels', 'monitor', 'count_time']]
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
            NT = NT[:,:,[0,2,3],:] #remove +- (second) row
            NT[:,:,:,1] += NT[:,:,:,2] # add -+(column 3) to +- (column 2), (cols. 1 and 2 in zero-indexed)
            NT = NT[:,:,:,[0,1,4]] # drop column 3 (2 in zero-indexing)
            # should now be (th_len, 2th_len, 3, 3) matrix
            output_columns = {'++':0, '-+':1, '--':2} 
        
        elif assumptions == 2:
            NT = NT[:,:,[0,1,3],:] #remove -+ (third) row
            NT[:,:,:,1] += NT[:,:,:,2] # add -+ column 3 to +- column 2 (zero-indexed)
            NT = NT[:,:,:,[0,1,4]] # drop column 3 (2 in zero-indexing)
            # should now be (th_len, 2th_len, 3, 3) matrix
            output_columns = {'++':0, '+-':1, '--':2} 
            
        elif assumptions == 3:
            NT = NT[:,:,[0,3],:] #remove both middle rows
            NT = NT[:,:,:,[0,3]] # remove both middle columns (1,2 in zero-indexing)
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
                    invNT[i,j] = linalg.inv(NT[i,j])
                    normNT[i,j] = linalg.norm(invNT[i,j])
                    R[i,j,:,0] = dot(invNT[i,j], alldata[i,j,:,0]) # counts
                    R[i,j,:,1] = dot(invNT[i,j], alldata[i,j,:,1]) / normNT[i,j] # pixels (need unitary transform)
                    R[i,j,:,2] = 1.0 # monitor is set to one.  Not sure about this one
                    R[i,j,:,3] = 1.0 # count time is set to one also.
                except:
                    R[i,j,:,0] = 0.0 # counts
                    R[i,j,:,1] = 0.0 # pixels (need unitary transform)
                    R[i,j,:,2] = 1.0 # monitor is set to one.  Not sure about this one
                    R[i,j,:,3] = 1.0 # count time is set to one also.
                    # this leaves zeros where the inversion fails
                    # not sure what else to do!
                n += 1
                new_percent_done = (100 * n) / nmax
                if new_percent_done > percent_done:
                    self.progress_update(new_percent_done)
                    percent_done = new_percent_done
                    
        combined_R = {}
        for PolState in polstates:
            combined_R[PolState] = MetaArray(R[:,:,output_columns[PolState]], info=combined_data[PolState].infoCopy())
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
        cols_to_add += ['NT++','NT+-','NT-+','NT--'] # add in all the polarization correction matrices too!
        
        new_info = dataset.infoCopy()        
        for i, col in enumerate(new_info[2]['cols']):
            if col['name'] in cols_to_add:
                array_to_rebin = dataset[:,:,col['name']].view(ndarray) 
                new_array = reb.rebin2d(data_edges[0],data_edges[1],array_to_rebin,bin_edges[0],bin_edges[1])
                grid[:,:,col['name']] += new_array
                
        return grid

class wxPolarizationCorrect(PolarizationCorrect):
    
    def apply(self, *args, **kwargs):
        self.progress_meter = wx.ProgressDialog("Progress", "% done", parent=None, style=wx.PD_AUTO_HIDE|wx.PD_APP_MODAL) 
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
    def apply(self, list_of_datasets, grid = None):
        pass

from pylab import *
from plot_2d3 import *
import wx
#default_supervisor = Supervisor()

class filter_plot_2d_data(plot_2d_data):
    """overriding the context menus to add interaction with other objects known to supervisor"""
    supervisor = Supervisor()
    
    def __init__(self, *args, **kwargs):
        plot_2d_data.__init__(self, *args, **kwargs)
        self.supervisor.AddPlot2d(self, None, self.window_title)
    
    def get_all_plot_2d_instances(self):
        """get all other plots that are open (from supervisor?)"""

        supervisor = self.supervisor
        instances = []
        instance_names = []
        #for dataset in supervisor.rebinned_data_objects:
            ##instances.append(dataset)
            #for subkey in dataset.__dict__.keys():
                    #if isinstance(dataset.__dict__[subkey], plottable_2d_data):
            ##print('plottable_2d_data yes')
            #instance_names.append(str(dataset.number) + ': ' + subkey + ': ' + dataset.description)
            #instances.append(dataset.__dict__[subkey])
        instances = self.supervisor.plots2d_data_objects
        instance_names = self.supervisor.plots2d_names

        return instances, instance_names

    def other_plots_menu(self):
        other_plots, other_plot_names = self.get_all_plot_2d_instances()
        other_menu = wx.Menu()
        for op in other_plot_names:
            item = other_menu.Append(wx.ID_ANY, op, op)
        return other_menu

    def other_plots_dialog(self):
        other_plots, other_plot_names = self.get_all_plot_2d_instances()
        #selection_num = wx.GetSingleChoiceIndex('Choose other plot', '', other_plot_names)
        dlg = wx.SingleChoiceDialog(None, 'Choose other plot', '', other_plot_names)
        dlg.SetSize(wx.Size(640,480))
        if dlg.ShowModal() == wx.ID_OK:
            selection_num=dlg.GetSelection()
        dlg.Destroy()
        return other_plots[selection_num]

    def dummy(self, evt):
        print 'the event is: ' + str(evt)

    def area_context(self, mpl_mouseevent, evt):
        area_popup = wx.Menu()
        item1 = area_popup.Append(wx.ID_ANY,'&Grid on/off', 'Toggle grid lines')
        wx.EVT_MENU(self, item1.GetId(), self.OnGridToggle)
        cmapmenu = CMapMenu(self, callback = self.OnColormap, mapper=self.mapper, canvas=self.canvas)
        item2 = area_popup.Append(wx.ID_ANY,'&Toggle log/lin', 'Toggle log/linear scale')
        wx.EVT_MENU(self, item2.GetId(), lambda evt: self.toggle_log_lin(mpl_mouseevent))
        item3 = area_popup.AppendMenu(wx.ID_ANY, "Colourmaps", cmapmenu)
        #other_plots, other_plot_names = self.get_all_plot_2d_instances()
        #if not (other_plot_names == []):
            #other_menu = wx.Menu()
            #for op in other_plot_names:
                #item = other_menu.Append(wx.ID_ANY, op, op)
        #other_menu = self.other_plots_menu()
        item4 = area_popup.Append(wx.ID_ANY, "copy intens. scale from", '')
        wx.EVT_MENU(self, item4.GetId(), lambda evt: self.copy_intensity_range_from(self.other_plots_dialog()) )
        item5 = area_popup.Append(wx.ID_ANY, "copy slice region from", '')
        wx.EVT_MENU(self, item5.GetId(), lambda evt: self.sliceplot(self.other_plots_dialog().slice_xy_range) )
        self.PopupMenu(area_popup, evt.GetPositionTuple())

def ShowNormData(data, scale = 'log'):
    dnorm = (data[:,:,'counts'] / data[:,:,'monitor']).view(ndarray).T
    
    info = data.infoCopy()
    ext_y = [info[0]['values'].min(), info[0]['values'].max()]
    y_label = '{name} ({units})'.format(name = info[0]['name'], units =info[0].get('units', ''))
    ext_x = [info[1]['values'].min(), info[1]['values'].max()]
    x_label = '{name} ({units})'.format(name = info[1]['name'], units =info[1].get('units', ''))
    extent = ext_x + ext_y
    #figure()
    #if logscale:
    #    dnorm = log(dnorm + 1e-7)
    
    #imshow(dnorm, origin='lower', aspect='auto', extent = extent)
    #xlabel(label_x)
    #ylabel(label_y)
    pixel_mask = data[:,:,'pixels'].copy()
    plot_title = data.extrainfo['CreationStory']
    frame = filter_plot_2d_data(dnorm, extent, None, scale = scale, pixel_mask = pixel_mask, window_title = plot_title, plot_title = plot_title, x_label = x_label, y_label = y_label)
    frame.Show()
    return frame
    
    
        
