"""
Offspecular reflectometry reduction modules
"""
import os, sys, pickle, types
from django.utils import simplejson as json
#try: from collections import OrderedDict
#except ImportError: from dataflow.ordered_dict import OrderedDict

from reduction.offspecular import filters
from reduction.offspecular.he3analyzer import He3AnalyzerCollection
from reduction.offspecular.FilterableMetaArray import FilterableMetaArray

from .. import config
#from ..wireit import template_to_wireit_diagram, instrument_to_wireit_language
from ..modules.load import load_module
#from ..modules.load_saved import load_saved_module
from ..modules.save import save_module
from ..core import Data, Instrument, Template, register_instrument
from ..wireit import template_to_wireit_diagram, instrument_to_wireit_language
#from .modules.load_asterix import load_asterix_module
from .modules.load_asterix_spectrum import load_asterix_spectrum_module
from .modules.normalize_to_monitor import normalize_to_monitor_module
from .modules.asterix_correct_spectrum import asterix_correct_spectrum_module
from .modules.combine import combine_module
from .modules.subtract import subtract_module
from .modules.autogrid import autogrid_module
from .modules.offset import offset_module
from .modules.wiggle import wiggle_module
from .modules.smooth import smooth_module
from .modules.tof_lambda import tof_lambda_module
from .modules.shift_data import shift_data_module
from .modules.pixels_two_theta import pixels_two_theta_module
from .modules.asterix_pixels_two_theta import asterix_pixels_two_theta_module
from .modules.theta_two_theta_qxqz import theta_two_theta_qxqz_module
from .modules.twotheta_q import twotheta_q_module
from .modules.two_theta_lambda_qxqz import two_theta_lambda_qxqz_module
from .modules.load_he3_analyzer_collection import load_he3_module
from .modules.append_polarization_matrix import append_polarization_matrix_module
from .modules.combine_polarized import combine_polarized_module
from .modules.polarization_correct import polarization_correct_module
from .modules.timestamps import timestamp_module
from .modules.load_timestamps import load_timestamp_module
from .modules.empty_qxqz_grid import empty_qxqz_grid_module
from .modules.mask_data import mask_data_module
from .modules.slice_data import slice_data_module
from .modules.collapse_data import collapse_data_module


class PlottableDict(dict):
    def get_plottable(self):
        return json.dumps({})
    def dumps(self):
        return pickle.dumps(self)
    @classmethod
    def loads(cls, str):
        return pickle.loads(str)

use_File = True
def get_friendly_name(fh):
    if use_File:
        from apps.tracks.models import File
        return File.objects.get(name=str(fh)).friendly_name
    return fh

OSPEC_DATA = 'ospec.data2d'
data2d = Data(OSPEC_DATA, FilterableMetaArray, loaders=[
    {'function':filters.LoadICPMany, 'id':'LoadICPData'},
    {'function':filters.LoadAsterixMany, 'id':'LoadAsterix'},
    {'function':filters.LoadUXDMany, 'id': 'LoadUXD'}])
#ast_data2d = Data('ospec.asterix.data2d', FilterableMetaArray, loaders=[{'function':LoadAsterixMany, 'id':'LoadAsterix'}])
OSPEC_DATA_HE3 = OSPEC_DATA + '.he3'
datahe3 = Data(OSPEC_DATA_HE3, He3AnalyzerCollection, loaders=[{'function':He3AnalyzerCollection, 'id':'LoadHe3'}])
OSPEC_DATA_TIMESTAMP = OSPEC_DATA + '.timestamp'
datastamp = Data(OSPEC_DATA_TIMESTAMP, PlottableDict, loaders=[])

"""
import tarfile
import StringIO

tar = tarfile.TarFile("test.tar","w")

string = StringIO.StringIO()
string.write("hello")
string.seek(0)
info = tarfile.TarInfo(name="foo")
info.size=len(string.buf)
tar.addfile(tarinfo=info, fileobj=string)

tar.close()
"""

# load saved result:
def load_saved_action(results=[], intent='', **kwargs):
    print "loading saved results"
    import tarfile
    from apps.tracks.models import File
    Fileobj = File.objects.get(name=str(fh))
    fn = Fileobj.name
    fp = Fileobj.location
    tf = tarfile.open(os.path.join(fp, fn), 'r:gz')
    result_objs = [tf.extractfile(member) for member in tf.getmembers()]
    result = [FilterableMetaArray.loads(robj.read()) for robj in result_objs]
    return dict(output=result)

# Load module
def load_action(input=[], files=[], intent='', auto_PolState=False, PolStates=[], **kwargs):
    print "loading", files
    
    result = []
    for i, f in enumerate(files):
        subresult = _load_data(f, auto_PolState, (PolStates[i] if i<len(PolStates) else ""))
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    for subresult in input:
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)

def _load_data(name, auto_PolState, PolState):
    (dirName, fileName) = os.path.split(name)
    friendly_name = get_friendly_name(fileName)
    return filters.LoadICPData(fileName, friendly_name=friendly_name, path=dirName, auto_PolState=auto_PolState, PolState=PolState)

# Load UXD module
def load_uxd_action(input=[], files=[], intent='', **kwargs):
    print "loading", files
    
    result = []
    for i, f in enumerate(files):
        subresult = _load_uxd_data(f)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    for subresult in input:
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)

def _load_uxd_data(name):
    (dirName, fileName) = os.path.split(name)
    friendly_name = get_friendly_name(fileName)
    return filters.LoadUXDData(fileName, friendly_name=friendly_name, path=dirName)

def load_asterix_action(input=[], files=[], **kwargs):
    result = []
    for f in files:
        subresult = _load_asterix_data(f)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    for subresult in input:
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)
    
def _load_asterix_data(name):
    (dirName, fileName) = os.path.split(name)
    friendly_name = get_friendly_name(fileName)
    print "friendly_name:", friendly_name
    if friendly_name.endswith('hdf'):
        format = "HDF4"
    else: #h5
        format = "HDF5"
    return filters.LoadAsterixRawHDF(fileName, path=dirName, friendly_name=friendly_name, format=format )
    #return SuperLoadAsterixHDF(fileName, path=dirName, center_pixel=center_pixel, wl_over_tof=wl_over_tof, pixel_width_over_dist=pixel_width_over_dist, format=format )

def load_asterix_spectrum_action(files=[], **kwargs):
    filename = files[0]
    (dirName, fileName) = os.path.split(filename)
    return dict(output=[filters.LoadAsterixSpectrum(filename, path=dirName)])
    
auto_PolState_field = {
        "type":"boolean",
        "label": "Auto-polstate",
        "name": "auto_PolState",
        "value": False,
}
autochain_loader_field = {
        "type":"boolean",
        "label": "Cache individual files",
        "name": "autochain-loader",
        "value": False,
}

PolStates_field = {
        "type":"string",
        "label": "PolStates",
        "name": "PolStates",
        "value": "",
}

load = load_module(id='ospec.load', datatype=OSPEC_DATA,
                   version='1.0', 
                   #action=load_action, 
                   #fields=OrderedDict({'files': {}, 'autochain-loader':autochain_loader_field, 'auto_PolState': auto_PolState_field, 'PolStates': PolStates_field}), 
                   filterModule=filters.LoadICPData)

load_uxd = load_module(id='ospec.uxd.load', datatype=OSPEC_DATA, version='1.0', action=load_uxd_action, filterModule = filters.LoadUXDData)

#load_asterix = load_asterix_module(id='ospec.asterix.load', datatype=OSPEC_DATA,
#                   version='1.0', action=load_asterix_action, filterModule=LoadAsterixRawHDF)
load_asterix = load_module(id='ospec.asterix.load', datatype=OSPEC_DATA,
                   version='1.0', action=load_asterix_action, fields={'autochain-loader':autochain_loader_field}, filterModule=filters.LoadAsterixRawHDF)
                   
load_asterix_spectrum = load_asterix_spectrum_module(id='ospec.asterix.load_spectrum', datatype=OSPEC_DATA,
                    version='1.0', action=load_asterix_spectrum_action)

# Save module
def save_action(input=[], ext=None, **kwargs):
    for index, f in enumerate(input): _save_one(f, ext, index) # not bundles
    return {}
def _save_one(input, ext, index):
    default_filename = "default.cg1"
    # modules like autogrid return MetaArrays that don't have filenames
    outname = initname = input._info[-1]["path"] + "/" + input._info[-1].get("filename", default_filename)
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0] + str(index), ext])
    print "saving", initname, 'as', outname
    input.write(outname)
    
save = save_module(id='ospec.save', datatype=OSPEC_DATA,
                   version='1.0', action=None)
save.xtype = 'SaveContainer'
save.image = config.IMAGES + config.ANDR_FOLDER + "save_image.png"

# Autogrid module
def autogrid_action(input=[], extra_grid_point=True, min_step=1e-10, **kwargs):
    print "gridding"
    return dict(output=[filters.Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)])
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                   version='1.0', action=autogrid_action)

# Combine module
def combine_action(input_data=[], input_grid=None, **kwargs):
    print "joining"
    output_grid = None
    if input_grid != None:
        output_grid = input_grid[0]
    return dict(output=[filters.Combine().apply(input_data, grid=output_grid)])
combine = combine_module(id='ospec.combine', datatype=OSPEC_DATA, version='1.0', action=combine_action)

# Subtract module
def subtract_action(minuend=[], subtrahend=None, **kwargs):
    print "subtracting"
    return dict(output=filters.Subtract().apply(minuend, subtrahend))
subtract = subtract_module(id='ospec.subtract', datatype=OSPEC_DATA, version='1.0', action=subtract_action)

# Offset module
def offset_action(input=[], offsets={}, **kwargs):
    print "offsetting"
    offsets_dict = {offsets['axis_name']['value'] : offsets['offset']['value']}
    return dict(output=filters.CoordinateOffset().apply(input, offsets=offsets_dict))
offset = offset_module(id='ospec.offset', datatype=OSPEC_DATA, version='1.0', action=offset_action)

# Correct spectrum module
def asterix_correct_spectrum_action(input=[], spectrum=[], **kwargs):
    print "correcting spectrum"
    # There should only be one entry into spectrum... more than that doesn't make sense
    # grabbing the first item from the spectrum list:
    return dict(output=filters.AsterixCorrectSpectrum().apply(input, spectrum=spectrum[0]))
asterix_correct_spectrum = asterix_correct_spectrum_module(id='ospec.asterix.corr_spectrum', datatype=OSPEC_DATA, 
                                            version='1.0', action=asterix_correct_spectrum_action)

# Shift data module
def shift_action(input=[], edge_bin = 180, axis=0, **kwargs):
    print "shifting data"
    return dict(output=filters.AsterixShiftData().apply(input, edge_bin=edge_bin, axis=axis))
shift_data = shift_data_module(id='ospec.asterix.shift', datatype=OSPEC_DATA, version='1.0', action=shift_action, filterModule=filters.AsterixShiftData)

# Normalize to Monitor module
def normalize_to_monitor_action(input=[], **kwargs):
    print "normalizing to monitor"
    return_val = dict(output=filters.NormalizeToMonitor().apply(input))
    print return_val
    return return_val
    
normalize_to_monitor = normalize_to_monitor_module(id='ospec.normalize_monitor', datatype=OSPEC_DATA, version='1.0', action=normalize_to_monitor_action, filterModule=filters.NormalizeToMonitor)

# smooth module
window_field = {'name': 'window', 'type': 'List', 'value': 0, 'choices': ['hanning', 'hamming', 'boxcar']}

# Mask module
def mask_action(input=[], xmin="0", xmax="", ymin="0", ymax="", invert_mask=False, **kwargs):
    print "masking"
    return dict(output=filters.MaskData().apply(input, xmin, xmax, ymin, ymax, invert_mask))
mask_data = mask_data_module(id='ospec.mask', datatype=OSPEC_DATA, version='1.0', action=mask_action, filterModule=filters.MaskData)

# Slice module
def slice_action(input=[], xmin="", xmax="", ymin="", ymax="", **kwargs):
    print "slicing"
    output = filters.SliceData().apply(input, xmin, xmax, ymin, ymax)
    
    if type(input) == types.ListType:
        xslice = []
        yslice = []
        for i in xrange(len(input)):
            xslice.append(output[i][0])
            yslice.append(output[i][1])
    else:
        xslice, yslice = output
    return dict(output_x = xslice, output_y = yslice)
slice_data = slice_data_module(id='ospec.slice', datatype=OSPEC_DATA, version='1.0', action=slice_action, filterModule=filters.SliceData)


# Collapse module
def collapse_action(input=[], **kwargs):
    print "collapsing"
    output = filters.CollapseData().apply(input)
    
    if type(input) == types.ListType:
        xslice = []
        yslice = []
        for i in xrange(len(input)):
            xslice.append(output[i][0])
            yslice.append(output[i][1])
    else:
        xslice, yslice = output
    return dict(output_x = xslice, output_y = yslice)
collapse_data = collapse_data_module(id='ospec.collapse', datatype=OSPEC_DATA, version='1.0', action=collapse_action,filterModule=filters.CollapseData)

# Wiggle module
def wiggle_action(input=[], amp=0.14, **kwargs):
    print "wiggling"
    return dict(output=filters.WiggleCorrection().apply(input, amp=amp))
wiggle = wiggle_module(id='ospec.wiggle', datatype=OSPEC_DATA, version='1.0', action=wiggle_action, filterModule=filters.WiggleCorrection)

# smooth module
window_field = {'name': 'window', 'type': 'List', 'value': 0, 'choices': ['hanning', 'hamming', 'boxcar']}
def smooth_action(input=[], window='flat', window_len=5, axis=0, **kwargs):
    print "smoothing"
    return dict(output=filters.SmoothData().apply(input, window=window, width=window_len, axis=axis))
smooth = smooth_module(id='ospec.smooth', datatype=OSPEC_DATA, version='1.0', action=smooth_action, filterModule=filters.SmoothData)

# Time of Flight to wavelength module
def tof_lambda_action(input=[], wl_over_tof=1.9050372144288577e-5, **kwargs):
    print "TOF to wavelength"
    return dict(output=filters.AsterixTOFToWavelength().apply(input, wl_over_tof=wl_over_tof))
tof_to_wavelength = tof_lambda_module(id='ospec.tof_lambda', datatype=OSPEC_DATA, version='1.0', action=tof_lambda_action, filterModule=filters.AsterixTOFToWavelength)

# Pixels to two theta module
def pixels_two_theta_action(input=[], pixels_per_degree=52.8, qzero_pixel=358, instr_resolution=1e-6, ax_name='xpixel', **kwargs):
    print "converting pixels to two theta"
    result = filters.PixelsToTwotheta().apply(input, pixels_per_degree=pixels_per_degree, qzero_pixel=qzero_pixel, instr_resolution=instr_resolution, ax_name=ax_name)
    return dict(output=result)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action, filterModule=filters.PixelsToTwotheta)


# Asterix Pixels to two theta module
def asterix_pixels_two_theta_action(input=[], qzero_pixel = 145., twotheta_offset=0.0, pw_over_d=0.0003411385649, **kwargs):
    print "converting pixels to two theta (Asterix)"
    result = filters.AsterixPixelsToTwotheta().apply(input, pw_over_d=pw_over_d, qzero_pixel=qzero_pixel, twotheta_offset=twotheta_offset)
    return dict(output=result)
asterix_pixels_two_theta = asterix_pixels_two_theta_module(id='ospec.asterix.twotheta', datatype=OSPEC_DATA, version='1.0', action=asterix_pixels_two_theta_action)

# Two theta Lambda to qxqz module
def two_theta_lambda_qxqz_action(input=[], theta=None, qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201,**kwargs):
    print "converting two theta and lambda to qx and qz"
    result = filters.TwothetaLambdaToQxQz().apply(input, theta, qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
    return dict(output=result)
two_theta_lambda_qxqz = two_theta_lambda_qxqz_module(id='ospec.tth_wl_qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_lambda_qxqz_action)


# Theta Two theta to qxqz module
def theta_two_theta_qxqz_action(input=[], output_grid=None, wavelength=5.0, qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201,**kwargs):
    print "converting theta and two theta to qx and qz"
    grid = None
    if output_grid != None:
        grid = output_grid[0]
    result = filters.ThetaTwothetaToQxQz().apply(input, grid, wavelength, qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
    return dict(output=result)
theta_two_theta_qxqz = theta_two_theta_qxqz_module(id='ospec.th_tth_qxqz', datatype=OSPEC_DATA, version='1.0', action=theta_two_theta_qxqz_action)

# Twotheta to q module
def twotheta_q_action(input=[], wavelength=5.0, ax_name='twotheta', **kwargs):
    print "converting twotheta to q"
    result = filters.TwothetaToQ().apply(input, wavelength, ax_name)
    return dict(output=result)
twotheta_q = twotheta_q_module(id='ospec.tth_q', datatype=OSPEC_DATA, version='1.0', action=twotheta_q_action)

def empty_qxqz_grid_action(qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201, **kwargs):
    print "creating an empty QxQz grid"
    return dict(output=[filters.EmptyQxQzGridPolarized(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)])
empty_qxqz = empty_qxqz_grid_module(id='ospec.emptyqxqz', datatype=OSPEC_DATA, version='1.0', action=empty_qxqz_grid_action)


# ======== Polarization modules ===========

# Load he3 module
def load_he3_action(files=[], **kwargs):
    print "loading he3", files
    result = [_load_he3_data(f) for f in files]
    return dict(output=result)
def _load_he3_data(name):
    (dirName, fileName) = os.path.split(name)
    return He3AnalyzerCollection(filename=fileName, path=dirName)
load_he3 = load_he3_module(id='ospec.loadhe3', datatype=OSPEC_DATA_HE3,
                   version='1.0', action=load_he3_action)

# Load timestamps
def load_timestamp_action(files=[], **kwargs):
    print "loading timestamps", files
    result = [PlottableDict(json.load(open(f, 'r'))) for f in files]
    return dict(output=result)
load_stamp = load_timestamp_module(id='ospec.loadstamp', datatype=OSPEC_DATA_TIMESTAMP,
                   version='1.0', action=load_timestamp_action)

def LoadTimestamps(filename, friendly_name="", path=""):
    fn = os.path.join(dirName, filename)
    return PlottableDict(json.load(open(fn, 'r')))

datastamp.loaders.append({'function':LoadTimestamps, 'id':'LoadTimeStamps'})
    
# Append polarization matrix module
def append_polarization_matrix_action(input=[], he3cell=None, **kwargs):
    print "appending polarization matrix"
    he3analyzer = None
    if he3cell != None: # should always be true; he3cell is now required
        he3analyzer = he3cell[0]
    return dict(output=filters.AppendPolarizationMatrix().apply(input, he3cell=he3analyzer))
append_polarization = append_polarization_matrix_module(id='ospec.append', datatype=OSPEC_DATA,
                    cell_datatype=OSPEC_DATA_HE3, version='1.0', action=append_polarization_matrix_action)

# Combine polarized module
def combine_polarized_action(input=[], grid=None, **kwargs):
    print "combining polarized"
    output_grid = None
    if grid != None:
        output_grid = grid[0]
    return dict(output=filters.CombinePolarized().apply(input, grid=output_grid))
combine_polarized = combine_polarized_module(id='ospec.comb_polar', datatype=OSPEC_DATA,
                                             version='1.0', action=combine_polarized_action)

# Polarization correction module
def polarization_correct_action(input=[], assumptions=0, auto_assumptions=True, **kwargs):
    print "polarization correction"
    return dict(output=filters.PolarizationCorrect().apply(input, assumptions=assumptions, auto_assumptions=auto_assumptions))
correct_polarized = polarization_correct_module(id='ospec.corr_polar', datatype=OSPEC_DATA,
                                             version='1.0', action=polarization_correct_action)

def timestamp_action(input=[], stamps=None, override_existing=False, **kwargs):
    print "stamping times"
    if stamps == None:
        sys.exit("No timestamps specified; exiting")
    timestamp_file = stamps[0] # only one timestamp
    return dict(output=[filters.InsertTimestamps().apply(datum, timestamp_file, override_existing=override_existing, filename=get_friendly_name(datum._info[-1]['filename'])) for datum in input])
timestamp = timestamp_module(id='ospec.timestamp', datatype=OSPEC_DATA,
                             version='1.0', action=timestamp_action, stamp_datatype=OSPEC_DATA_TIMESTAMP)

#Instrument definitions
ANDR = Instrument(id='ncnr.ospec.andr',
                 name='andr',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, load_he3, load_stamp, save]),
                       ('Reduction', [autogrid, combine, subtract, offset, wiggle, smooth, pixels_two_theta, theta_two_theta_qxqz, twotheta_q, empty_qxqz, mask_data, slice_data, collapse_data, normalize_to_monitor]),
                       ('Polarization reduction', [timestamp, append_polarization, combine_polarized, correct_polarized]),
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d, datahe3, datastamp],
                 )

ASTERIX = Instrument(id='lansce.ospec.asterix',
                 name='asterix',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, load_asterix_spectrum, save]),
                       ('Reduction', [autogrid, combine, offset, shift_data, tof_to_wavelength, asterix_pixels_two_theta, two_theta_lambda_qxqz, mask_data, collapse_data, slice_data, normalize_to_monitor, asterix_correct_spectrum]),
                       ('Polarization reduction', [correct_polarized]),
                       ],
                 requires=[],
                 datatypes=[data2d],
                 )
                 
for instrument in [ANDR, ASTERIX]:
    register_instrument(instrument)
    
# Testing
def demo():
    from ..calc import get_plottable, memory_cache
    polarized = False
    if not polarized:
        path, ext = dir + '/dataflow/sampledata/ANDR/sabc/Isabc20', '.cg1'
        files = [path + str(i + 1).zfill(2) + ext for i in range(1, 12)]
        modules = [
            dict(module="ospec.load", position=(50, 50),
                 config={'files': files, 'intent': 'signal'}),
            dict(module="ospec.save", position=(650, 350), config={'ext': 'dat'}),
            dict(module="ospec.combine", position=(452, 390), config={}),
            dict(module="ospec.offset", position=(321, 171), config={'offsets':{'theta':0, 'xpixel':10}}),
            dict(module="ospec.wiggle", position=(204, 92), config={}),
            dict(module="ospec.twotheta", position=(450, 250), config={}),
            dict(module="ospec.th_tth_qxqz", position=(560, 392), config={}),
            dict(module="ospec.grid", position=(350, 390), config={}),
            dict(module="ospec.emptyqxqz", position=(350, 470), config={}),
        ]
        wires = [
            dict(source=[0, 'output'], target=[4, 'input']),
            dict(source=[4, 'output'], target=[3, 'input']),
            dict(source=[3, 'output'], target=[5, 'input']),
            dict(source=[5, 'output'], target=[2, 'input_data']),
            dict(source=[5, 'output'], target=[7, 'input']),
            dict(source=[7, 'output'], target=[2, 'input_grid']),
            dict(source=[2, 'output'], target=[6, 'input']),
            dict(source=[8, 'output'], target=[6, 'output_grid']),
            dict(source=[6, 'output'], target=[1, 'input']),
        ]
    else:
        path, ext = dir + '/dataflow/sampledata/ANDR/cshape_121609/Iremun00', ['.ca1', '.cb1']
        files = [path + str(i + 1) + extension for i in range(0, 9) for extension in ext if i != 2]
        pols = json.load(open(dir + '/dataflow/sampledata/ANDR/cshape_121609/file_catalog.json', 'r'))
        pol_states = dict((os.path.split(file)[-1], pols[os.path.split(file)[-1]]['polarization']) for file in files)
        modules = [
            dict(module="ospec.load", position=(50, 25),
                 config={'files': files, 'intent': 'signal', 'PolStates':pol_states}),
            dict(module="ospec.timestamp", position=(100, 125), config={}),
            dict(module="ospec.loadhe3", position=(50, 375), config={'files':[dir + '/dataflow/sampledata/ANDR/cshape_121609/He3Cells.json']}),
            dict(module="ospec.save", position=(700, 175), config={'ext': 'dat'}),
            dict(module="ospec.comb_polar", position=(450, 180), config={}),
            dict(module="ospec.append", position=(300, 225), config={}),
            dict(module="ospec.corr_polar", position=(570, 125), config={}),
            dict(module="ospec.grid", position=(350, 375), config={}),
            dict(module="ospec.loadstamp", position=(50, 250), config={'files':[dir + '/dataflow/sampledata/ANDR/cshape_121609/end_times.json']}),
        ]
        wires = [
            dict(source=[0, 'output'], target=[1, 'input']),
            dict(source=[8, 'output'], target=[1, 'stamps']),
            dict(source=[1, 'output'], target=[5, 'input']),
            dict(source=[2, 'output'], target=[5, 'he3cell']),
            dict(source=[5, 'output'], target=[4, 'input']),
            dict(source=[5, 'output'], target=[7, 'input']),
            dict(source=[7, 'output'], target=[4, 'grid']),
            dict(source=[4, 'output'], target=[6, 'input']),
            dict(source=[6, 'output'], target=[3, 'input']),
        ]
    config = dict((n, d['config']) for (n, d) in enumerate(modules))
    template = Template(name='test ospec',
                        description='example ospec diagram',
                        modules=modules,
                        wires=wires,
                        instrument=ANDR.id,
                        )
    
    print template_to_wireit_diagram(template)
    ins = json.dumps(instrument_to_wireit_language(ANDR), sort_keys=True, indent=2)
    with open(dir + '/dataflow/static/wireit_test/ANDRdefinition2.js', 'w') as f:
        f.write('var andr2 = ' + ins + ';')
        f.write("\n\nSaveContainer = function(opts, layer) {\
\n    SaveContainer.superclass.constructor.call(this, opts, layer);\
\n    var content = document.createElement('div')\
\n    content.innerHTML = 'Click here to save:';\
\n    var saveButton = document.createElement('img');\
\n    saveButton.src = this.image;\
\n    content.appendChild(saveButton);    \
\n    this.setBody(content);\
\n\
\n    YAHOO.util.Event.addListener(saveButton, 'click', this.Save, this, true);\
\n};\
\n\nYAHOO.lang.extend(SaveContainer, WireIt.Container, {\
\n    xtype: 'SaveContainer',\
\n    Save: function(e) {\
\n        console.log('save click:', e);\
\n        alert('I am saving!');\
\n    }\
\n});")
    sys.exit()
    
    nodenum = template.order()[-2]
    terminal = 'output'
    result = get_plottable(template, config, nodenum, terminal, memory_cache())
    #print "Writing to files"
    #for nodenum, plottable in result.items():
    #    for terminal_id, plot in plottable.items():
    #        with open('data/' + terminal_id + "_" + str(nodenum) + ".txt", "w") as f:
    #            for format in plot:
    #                f.write(format + "\n")
    with open('data/' + terminal + "_" + str(nodenum) + ".txt", "w") as f:
        print "Writing:", f.name
        for format in result:
            f.write(format + "\n")
    print "Done"

if __name__ == '__main__':
    demo()
