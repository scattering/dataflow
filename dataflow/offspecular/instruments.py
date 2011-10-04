"""
Offspecular reflectometry reduction modules
"""
import os, sys, simplejson, pickle, types

# left here for testing purposes
# python uses __name__ for relative imports so I cannot use
# the ... in place of dataflow when testing
TESTING = 0
SERVER = 0
# modules = [ (source, module), ... ]
module_imports = [
    #("dataflow.wireit", ["template_to_wireit_diagram", "instrument_to_wireit_language"]),
    ("dataflow", "config"),
    ("dataflow.calc", ["run_template", "get_plottable", "calc_single"]),
    ("dataflow.core", ["Data", "Instrument", "Template", "register_instrument"]),
    ("dataflow.modules.load", "load_module"),
    ("dataflow.offspecular.modules.load_asterix", "load_asterix_module"),
    ("dataflow.offspecular.modules.load_asterix_spectrum", "load_asterix_spectrum_module"),
    ("dataflow.modules.save", "save_module"),
    ("dataflow.offspecular.modules.normalize_to_monitor", "normalize_to_monitor_module"),
    ("dataflow.offspecular.modules.asterix_correct_spectrum", "asterix_correct_spectrum_module"),
    ("dataflow.offspecular.modules.combine", "combine_module"),
    ("dataflow.offspecular.modules.autogrid", "autogrid_module"),
    ("dataflow.offspecular.modules.offset", "offset_module"),
    ("dataflow.offspecular.modules.wiggle", "wiggle_module"),
    ("dataflow.offspecular.modules.tof_lambda", "tof_lambda_module"),
    ("dataflow.offspecular.modules.shift_data", "shift_data_module"), 
    ("dataflow.offspecular.modules.pixels_two_theta", "pixels_two_theta_module"),
    ("dataflow.offspecular.modules.asterix_pixels_two_theta", "asterix_pixels_two_theta_module"),
    ("dataflow.offspecular.modules.theta_two_theta_qxqz", "theta_two_theta_qxqz_module"),
    ("dataflow.offspecular.modules.two_theta_lambda_qxqz", "two_theta_lambda_qxqz_module"),
    ("dataflow.offspecular.modules.load_he3_analyzer_collection", "load_he3_module"),
    ("dataflow.offspecular.modules.append_polarization_matrix", "append_polarization_matrix_module"),
    ("dataflow.offspecular.modules.combine_polarized", "combine_polarized_module"),
    ("dataflow.offspecular.modules.polarization_correct", "polarization_correct_module"),
    ("dataflow.offspecular.modules.timestamps", "timestamp_module"),
    ("dataflow.offspecular.modules.load_timestamps", "load_timestamp_module"),
    ("dataflow.offspecular.modules.empty_qxqz_grid", "empty_qxqz_grid_module"),
    ("dataflow.offspecular.modules.mask_data", "mask_data_module"),
    ("dataflow.offspecular.modules.slice_data", "slice_data_module"),
    ("reduction.offspecular.filters", ["LoadICPData", "LoadAsterixRawHDF", "LoadAsterixSpectrum", "Autogrid", "Combine", "CoordinateOffset", "AsterixShiftData", "MaskData", "SliceData", "WiggleCorrection", "NormalizeToMonitor", "AsterixCorrectSpectrum", "AsterixTOFToWavelength", "AsterixPixelsToTwotheta", "TwothetaLambdaToQxQz"]),
    ("reduction.offspecular.he3analyzer", "He3AnalyzerCollection"),
    ("reduction.offspecular.FilterableMetaArray", "FilterableMetaArray"),
]
if SERVER:
    from DATAFLOW.dataflow.wireit import template_to_wireit_diagram, instrument_to_wireit_language
    root_import = "DATAFLOW."
    
elif TESTING:
    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(dir)
    from dataflow.dataflow.wireit import template_to_wireit_diagram, instrument_to_wireit_language
    root_import = "dataflow."
    
else:
    root_import = "..."


for item in module_imports:
    loc = item[0]
    mods = item[1]
    print root_import + item[0], item[1]
    if type(mods) != types.ListType:
        mods = [mods]
    for mod in mods:
        exec("from %s import %s" % (root_import + loc, mod))
    #__import__(root_import + item[0], globals=globals(), fromlist=item[1], level=-1)

class PlottableDict(dict):
    def get_plottable(self):
        return simplejson.dumps({})
    def dumps(self):
        return pickle.dumps(self)
    @classmethod
    def loads(cls, str):
        return pickle.loads(str)

use_File = True
def get_friendly_name(fh):
    if use_File:
        from ...apps.tracks.models import File
        return File.objects.get(name=str(fh)).friendly_name
    return fh

OSPEC_DATA = 'data2d.ospec'
data2d = Data(OSPEC_DATA, FilterableMetaArray)
OSPEC_DATA_HE3 = OSPEC_DATA + '.he3'
datahe3 = Data(OSPEC_DATA_HE3, He3AnalyzerCollection)
OSPEC_DATA_TIMESTAMP = OSPEC_DATA + '.timestamp'
datastamp = Data(OSPEC_DATA_TIMESTAMP, PlottableDict)

# Load module
def load_action(files=[], intent='', auto_PolState=False, PolStates={}, **kwargs):
    print "loading", files
    
    PolStates = dict((file, state.replace(' ', '+')) for file, state in PolStates.items())
    result = []
    for f in files:
        subresult = _load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), ''))
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)   
    #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)

def _load_data(name, auto_PolState, PolState):
    (dirName, fileName) = os.path.split(name)
    friendlyName = get_friendly_name(fileName)
    return LoadICPData(fileName, path=dirName, auto_PolState=auto_PolState, PolState=PolState)


def load_asterix_action(files=[], center_pixel = 145.0, wl_over_tof=1.9050372144288577e-5, pixel_width_over_dist =0.00034113856493630764, **kwargs):
    result = []
    for f in files:
        subresult = _load_asterix_data(f, center_pixel, wl_over_tof, pixel_width_over_dist)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)   
    #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)
    
def _load_asterix_data(name, center_pixel, wl_over_tof, pixel_width_over_dist):
    (dirName, fileName) = os.path.split(name)
    friendlyName = get_friendly_name(fileName)
    if friendlyName.endswith('hdf'):
        format = "HDF4"
    else: #h5
        format = "HDF5"
    return LoadAsterixRawHDF(fileName, path=dirName, center_pixel=center_pixel, wl_over_tof=wl_over_tof, pixel_width_over_dist=pixel_width_over_dist, format=format )
    #return SuperLoadAsterixHDF(fileName, path=dirName, center_pixel=center_pixel, wl_over_tof=wl_over_tof, pixel_width_over_dist=pixel_width_over_dist, format=format )

def load_asterix_spectrum_action(files=[], **kwargs):
    filename = files[0]
    (dirName, fileName) = os.path.split(filename)
    return dict(output=[LoadAsterixSpectrum(filename, path=dirName)])
    
auto_PolState_field = {
        "type":"boolean",
        "label": "Auto-polstate",
        "name": "auto_PolState",
        "value": False,
}
PolStates_field = {
        "type":"dict:string:string",
        "label": "PolStates",
        "name": "PolStates",
        "value": {},
}
load = load_module(id='ospec.load', datatype=OSPEC_DATA,
                   version='1.0', action=load_action, fields=[auto_PolState_field, PolStates_field])

load_asterix = load_asterix_module(id='ospec.asterix.load', datatype=OSPEC_DATA,
                   version='1.0', action=load_asterix_action)
                   
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
                   version='1.0', action=save_action)
save.xtype = 'SaveContainer'
save.image = config.IMAGES + config.ANDR_FOLDER + "save_image.png"

# Autogrid module
def autogrid_action(input=[], extra_grid_point=True, min_step=1e-10, **kwargs):
    print "gridding"
    return dict(output=[Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)])
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                   version='1.0', action=autogrid_action)

# Combine module
def combine_action(input_data=[], input_grid=None, **kwargs):
    print "joining"
    output_grid = None
    if input_grid != None:
        output_grid = input_grid[0]
    return dict(output=[Combine().apply(input_data, grid=output_grid)])
combine = combine_module(id='ospec.combine', datatype=OSPEC_DATA, version='1.0', action=combine_action)

# Offset module
def offset_action(input=[], offsets={}, **kwargs):
    print "offsetting"
    return dict(output=CoordinateOffset().apply(input, offsets=offsets))
offset = offset_module(id='ospec.offset', datatype=OSPEC_DATA, version='1.0', action=offset_action)

# Correct spectrum module
def asterix_correct_spectrum_action(input=[], spectrum=[], **kwargs):
    print "correcting spectrum"
    # There should only be one entry into spectrum... more than that doesn't make sense
    # grabbing the first item from the spectrum list:
    return dict(output=AsterixCorrectSpectrum().apply(input, spectrum=spectrum[0]))
asterix_correct_spectrum = asterix_correct_spectrum_module(id='ospec.asterix.corr_spectrum', datatype=OSPEC_DATA, 
                                            version='1.0', action=asterix_correct_spectrum_action)

# Shift data module
def shift_action(input=[], edge_bin = 180, axis=0, **kwargs):
    print "shifting data"
    return dict(output=AsterixShiftData().apply(input, edge_bin=edge_bin, axis=axis))
shift_data = shift_data_module(id='ospec.asterix.shift', datatype=OSPEC_DATA, version='1.0', action=shift_action)

# Normalize to Monitor module
def normalize_to_monitor_action(input=[], **kwargs):
    print "normalizing to monitor"
    return_val = dict(output=NormalizeToMonitor().apply(input))
    print return_val
    return return_val
    
normalize_to_monitor = normalize_to_monitor_module(id='ospec.normalize_monitor', datatype=OSPEC_DATA, version='1.0', action=normalize_to_monitor_action)

# Mask module
def mask_action(input=[], xmin="0", xmax="", ymin="0", ymax="", invert_mask=False, **kwargs):
    print "masking"
    return dict(output=MaskData().apply(input, xmin, xmax, ymin, ymax, invert_mask))
mask_data = mask_data_module(id='ospec.mask', datatype=OSPEC_DATA, version='1.0', action=mask_action)

# Slice module
def slice_action(input=[], **kwargs):
    print "slicing"
    output = SliceData().apply(input)
    
    if type(input) == types.ListType:
        xslice = []
        yslice = []
        for i in xrange(len(input)):
            xslice.append(output[i][0])
            yslice.append(output[i][1])
    else:
        xslice, yslice = output
    return dict(output_x = xslice, output_y = yslice)
slice_data = slice_data_module(id='ospec.slice', datatype=OSPEC_DATA, version='1.0', action=slice_action) 

# Wiggle module
def wiggle_action(input=[], amp=0.14, **kwargs):
    print "wiggling"
    return dict(output=WiggleCorrection().apply(input, amp=amp))
wiggle = wiggle_module(id='ospec.wiggle', datatype=OSPEC_DATA, version='1.0', action=wiggle_action)

# Time of Flight to wavelength module
def tof_lambda_action(input=[], wl_over_tof=1.9050372144288577e-5, **kwargs):
    print "TOF to wavelength"
    return dict(output=AsterixTOFToWavelength().apply(input, wl_over_tof=wl_over_tof))
tof_to_wavelength = tof_lambda_module(id='ospec.tof_lambda', datatype=OSPEC_DATA, version='1.0', action=tof_lambda_action)

# Pixels to two theta module
def pixels_two_theta_action(input=[], pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6, **kwargs):
    print "converting pixels to two theta"
    result = PixelsToTwotheta().apply(input, pixels_per_degree=pixels_per_degree, qzero_pixel=qzero_pixel, instr_resolution=instr_resolution)
    return dict(output=result)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action)

# Asterix Correct Spectrum Module
def correct_spectrum_action(data=[], spectrum=None):
    print "multiplying monitor counts by spectrum"
    polarizations = ["down_down", "down_up", "up_down", "up_up"]
    passthrough_cols = ["counts_%s" % (pol,) for pol in polarizations]
    passthrough_cols.extend(["pixels", "count_time"])
    expressions = [{"name":col, "expression":"data1_%s" % (col,)} for col in passthrough_cols]

    expressions.extend([{"name":"monitor_%s" % (pol,), "expression":"data1_monitor_%s * data2_column0" % (pol,)} for pol in polarizations])
    expressions.extend([{"name":"pixels", "expression":"data1_pixels"} for pol in polarizations])
    result = Algebra()

# Asterix Pixels to two theta module
def asterix_pixels_two_theta_action(input=[], qzero_pixel = 145., twotheta_offset=0.0, pw_over_d=0.0003411385649, **kwargs):
    print "converting pixels to two theta (Asterix)"
    result = AsterixPixelsToTwotheta().apply(input, pw_over_d=pw_over_d, qzero_pixel=qzero_pixel, twotheta_offset=twotheta_offset)
    return dict(output=result)
asterix_pixels_two_theta = asterix_pixels_two_theta_module(id='ospec.asterix.twotheta', datatype=OSPEC_DATA, version='1.0', action=asterix_pixels_two_theta_action)

# Two theta Lambda to qxqz module
def two_theta_lambda_qxqz_action(input=[], theta=None, qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201,**kwargs):
    print "converting two theta and lambda to qx and qz"
    result = TwothetaLambdaToQxQz().apply(input, theta, qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
    return dict(output=result)
two_theta_lambda_qxqz = two_theta_lambda_qxqz_module(id='ospec.tth_wl_qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_lambda_qxqz_action)


# Theta Two theta to qxqz module
def theta_two_theta_qxqz_action(input=[], output_grid=None, wavelength=5.0, **kwargs):
    print "converting theta and two theta to qx and qz"
    grid = None
    if output_grid != None:
        grid = output_grid[0]
    result = ThetaTwothetaToQxQz().apply(input, output_grid=grid, wavelength=wavelength)
    return dict(output=result)
theta_two_theta_qxqz = theta_two_theta_qxqz_module(id='ospec.th_tth_qxqz', datatype=OSPEC_DATA, version='1.0', action=theta_two_theta_qxqz_action)

def empty_qxqz_grid_action(qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201, **kwargs):
    print "creating an empty QxQz grid"
    return dict(output=[EmptyQxQzGridPolarized(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)])
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
    result = [PlottableDict(simplejson.load(open(f, 'r'))) for f in files]
    return dict(output=result)
load_stamp = load_timestamp_module(id='ospec.loadstamp', datatype=OSPEC_DATA_TIMESTAMP,
                   version='1.0', action=load_timestamp_action)

# Append polarization matrix module
def append_polarization_matrix_action(input=[], he3cell=None, **kwargs):
    print "appending polarization matrix"
    he3analyzer = None
    if he3cell != None: # should always be true; he3cell is now required
        he3analyzer = he3cell[0]
    return dict(output=AppendPolarizationMatrix().apply(input, he3cell=he3analyzer))
append_polarization = append_polarization_matrix_module(id='ospec.append', datatype=OSPEC_DATA,
                    cell_datatype=OSPEC_DATA_HE3, version='1.0', action=append_polarization_matrix_action)

# Combine polarized module
def combine_polarized_action(input=[], grid=None, **kwargs):
    print "combining polarized"
    output_grid = None
    if grid != None:
        output_grid = grid[0]
    return dict(output=CombinePolarized().apply(input, grid=output_grid))
combine_polarized = combine_polarized_module(id='ospec.comb_polar', datatype=OSPEC_DATA,
                                             version='1.0', action=combine_polarized_action)

# Polarization correction module
def polarization_correct_action(input=[], assumptions=0, auto_assumptions=True, **kwargs):
    print "polarization correction"
    return dict(output=PolarizationCorrect().apply(input, assumptions=assumptions, auto_assumptions=auto_assumptions)) 
correct_polarized = polarization_correct_module(id='ospec.corr_polar', datatype=OSPEC_DATA,
                                             version='1.0', action=polarization_correct_action)

def timestamp_action(input=[], stamps=None, override_existing=False, **kwargs):
    print "stamping times"
    if stamps == None:
        sys.exit("No timestamps specified; exiting")
    timestamp_file = stamps[0] # only one timestamp
    return dict(output=[InsertTimestamps().apply(datum, timestamp_file, override_existing=override_existing, filename=get_friendly_name(datum._info[-1]['filename'])) for datum in input])
timestamp = timestamp_module(id='ospec.timestamp', datatype=OSPEC_DATA,
                             version='1.0', action=timestamp_action, stamp_datatype=OSPEC_DATA_TIMESTAMP)

#Instrument definitions
ANDR = Instrument(id='ncnr.ospec.andr',
                 name='NCNR ANDR',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, load_asterix, load_he3, load_stamp, save]),
                       ('Reduction', [autogrid, combine, offset, wiggle, pixels_two_theta, theta_two_theta_qxqz, two_theta_lambda_qxqz, empty_qxqz, mask_data, slice_data]),
                       ('Polarization reduction', [timestamp, append_polarization, combine_polarized, correct_polarized]),
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d, datahe3, datastamp],
                 )

ASTERIX = Instrument(id='lansce.ospec.asterix',
                 name='LANSCE ASTERIX',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load_asterix, load_asterix_spectrum, save]),
                       ('Reduction', [autogrid, combine, offset, shift_data, tof_to_wavelength, asterix_pixels_two_theta, two_theta_lambda_qxqz, mask_data, slice_data, normalize_to_monitor, asterix_correct_spectrum]),
                       ('Polarization reduction', [correct_polarized]),
                       ],
                 requires=[],
                 datatypes=[data2d],
                 )
                 
instrmnts = [ANDR,ASTERIX]
for instrument in instrmnts:
    register_instrument(instrument)
    
# Testing
if __name__ == '__main__':
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
        pols = simplejson.load(open(dir + '/dataflow/sampledata/ANDR/cshape_121609/file_catalog.json', 'r'))
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
    ins = simplejson.dumps(instrument_to_wireit_language(ANDR), sort_keys=True, indent=2)
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
    result = get_plottable(template, config, nodenum, terminal)
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
