"""
Offspecular reflectometry reduction modules
"""
import os, sys, simplejson, pickle

# left here for testing purposes
# python uses __name__ for relative imports so I cannot use
# the ... in place of dataflow when testing
TESTING = 1
SERVER = 0
if SERVER:
    from DATAFLOW.dataflow.wireit import template_to_wireit_diagram, instrument_to_wireit_language
    from DATAFLOW.dataflow import config
    from DATAFLOW.dataflow.calc import run_template, get_plottable, calc_single
    from DATAFLOW.dataflow.core import Data, Instrument, Template, register_instrument
    from DATAFLOW.dataflow.modules.load import load_module
    from DATAFLOW.dataflow.modules.save import save_module
    from DATAFLOW.dataflow.offspecular.modules.combine import combine_module
    from DATAFLOW.dataflow.offspecular.modules.autogrid import autogrid_module
    from DATAFLOW.dataflow.offspecular.modules.offset import offset_module
    from DATAFLOW.dataflow.offspecular.modules.wiggle import wiggle_module
    from DATAFLOW.dataflow.offspecular.modules.pixels_two_theta import pixels_two_theta_module
    from DATAFLOW.dataflow.offspecular.modules.two_theta_qxqz import two_theta_qxqz_module
    from DATAFLOW.dataflow.offspecular.modules.load_he3_analyzer_collection import load_he3_module
    from DATAFLOW.dataflow.offspecular.modules.append_polarization_matrix import append_polarization_matrix_module
    from DATAFLOW.dataflow.offspecular.modules.combine_polarized import combine_polarized_module
    from DATAFLOW.dataflow.offspecular.modules.polarization_correct import polarization_correct_module
    from DATAFLOW.dataflow.offspecular.modules.timestamps import timestamp_module
    from DATAFLOW.dataflow.offspecular.modules.load_timestamps import load_timestamp_module
    from DATAFLOW.dataflow.offspecular.modules.empty_qxqz_grid import empty_qxqz_grid_module
    from DATAFLOW.reduction.offspecular.filters import *
    from DATAFLOW.reduction.offspecular.he3analyzer import *
    from DATAFLOW.reduction.offspecular.FilterableMetaArray import FilterableMetaArray
elif TESTING:
    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(dir)
    from dataflow.dataflow.wireit import template_to_wireit_diagram, instrument_to_wireit_language
    from dataflow.dataflow import config
    from dataflow.dataflow.calc import run_template, get_plottable, calc_single
    from dataflow.dataflow.core import Data, Instrument, Template, register_instrument
    from dataflow.dataflow.modules.load import load_module
    from dataflow.dataflow.modules.save import save_module
    from dataflow.dataflow.offspecular.modules.combine import combine_module
    from dataflow.dataflow.offspecular.modules.autogrid import autogrid_module
    from dataflow.dataflow.offspecular.modules.offset import offset_module
    from dataflow.dataflow.offspecular.modules.wiggle import wiggle_module
    from dataflow.dataflow.offspecular.modules.pixels_two_theta import pixels_two_theta_module
    from dataflow.dataflow.offspecular.modules.two_theta_qxqz import two_theta_qxqz_module
    from dataflow.dataflow.offspecular.modules.load_he3_analyzer_collection import load_he3_module
    from dataflow.dataflow.offspecular.modules.append_polarization_matrix import append_polarization_matrix_module
    from dataflow.dataflow.offspecular.modules.combine_polarized import combine_polarized_module
    from dataflow.dataflow.offspecular.modules.polarization_correct import polarization_correct_module
    from dataflow.dataflow.offspecular.modules.timestamps import timestamp_module
    from dataflow.dataflow.offspecular.modules.load_timestamps import load_timestamp_module
    from dataflow.dataflow.offspecular.modules.empty_qxqz_grid import empty_qxqz_grid_module
    from dataflow.reduction.offspecular.filters import *
    from dataflow.reduction.offspecular.he3analyzer import *
    from dataflow.reduction.offspecular.FilterableMetaArray import FilterableMetaArray
else:
    from .. import config
    from ..calc import run_template, get_plottable, calc_single
    from ..core import Data, Instrument, Template, register_instrument
    from ..modules.load import load_module
    from ..modules.save import save_module
    from ..offspecular.modules.combine import combine_module
    from ..offspecular.modules.autogrid import autogrid_module
    from ..offspecular.modules.offset import offset_module
    from ..offspecular.modules.wiggle import wiggle_module
    from ..offspecular.modules.pixels_two_theta import pixels_two_theta_module
    from ..offspecular.modules.two_theta_qxqz import two_theta_qxqz_module
    from ..offspecular.modules.load_he3_analyzer_collection import load_he3_module
    from ..offspecular.modules.append_polarization_matrix import append_polarization_matrix_module
    from ..offspecular.modules.combine_polarized import combine_polarized_module
    from ..offspecular.modules.polarization_correct import polarization_correct_module
    from ..offspecular.modules.timestamps import timestamp_module
    from ..offspecular.modules.load_timestamps import load_timestamp_module
    from ..offspecular.modules.empty_qxqz_grid import empty_qxqz_grid_module
    from ...reduction.offspecular.filters import *
    from ...reduction.offspecular.he3analyzer import *
    from ...reduction.offspecular.FilterableMetaArray import FilterableMetaArray

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
    result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)
def _load_data(name, auto_PolState, PolState):
    (dirName, fileName) = os.path.split(name)
    print "Loading:", name, PolState
    return LoadICPData(fileName, path=dirName, auto_PolState=auto_PolState, PolState=PolState)
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

# Wiggle module
def wiggle_action(input=[], amp=0.14, **kwargs):
    print "wiggling"
    return dict(output=WiggleCorrection().apply(input, amp=amp))
wiggle = wiggle_module(id='ospec.wiggle', datatype=OSPEC_DATA, version='1.0', action=wiggle_action)

# Pixels to two theta module
def pixels_two_theta_action(input=[], pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6, **kwargs):
    print "converting pixels to two theta"
    result = PixelsToTwotheta().apply(input, pixels_per_degree=pixels_per_degree, qzero_pixel=qzero_pixel, instr_resolution=instr_resolution)
    return dict(output=result)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action)

# Two theta to qxqz module
def two_theta_qxqz_action(input=[], output_grid=None, wavelength=5.0, **kwargs):
    print "converting theta and two theta to qx and qz"
    grid = None
    if output_grid != None:
        grid = output_grid[0]
    result = ThetaTwothetaToQxQz().apply(input, output_grid=grid, wavelength=wavelength)
    return dict(output=result)
two_theta_qxqz = two_theta_qxqz_module(id='ospec.qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_qxqz_action)

def empty_qxqz_grid_action(qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201):
    return dict(output=[EmptyQxQzGrid(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)])
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
                 menu=[('Input', [load, load_he3, load_stamp, save]),
                       ('Reduction', [autogrid, combine, offset, wiggle, pixels_two_theta, two_theta_qxqz, empty_qxqz]),
                       ('Polarization reduction', [timestamp, append_polarization, combine_polarized, correct_polarized]),
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d, datahe3, datastamp],
                 )
instrmnts = [ANDR]
for instrument in instrmnts:
    register_instrument(instrument)

# Testing
if __name__ == '__main__':
    polarized = True
    if not polarized:
        path, ext = dir + '/dataflow/sampledata/ANDR/sabc/Isabc20', '.cg1'
        files = [path + str(i + 1).zfill(2) + ext for i in range(1, 12)]
        modules = [
            dict(module="ospec.load", position=(50, 50),
                 config={'files': files, 'intent': 'signal'}),
            dict(module="ospec.save", position=(650, 350), config={'ext': 'dat'}),
            dict(module="ospec.combine", position=(452, 390), config={}),
            dict(module="ospec.offset", position=(321, 171), config={'offsets':{'theta':0}}),
            dict(module="ospec.wiggle", position=(204, 92), config={}),
            dict(module="ospec.twotheta", position=(450, 250), config={}),
            dict(module="ospec.qxqz", position=(560, 392), config={}),
            dict(module="ospec.grid", position=(350, 390), config={}),
        ]
        wires = [
            dict(source=[0, 'output'], target=[4, 'input']),
            dict(source=[4, 'output'], target=[3, 'input']),
            dict(source=[3, 'output'], target=[5, 'input']),
            dict(source=[5, 'output'], target=[2, 'input_data']),
            dict(source=[5, 'output'], target=[7, 'input']),
            dict(source=[7, 'output'], target=[2, 'input_grid']),
            dict(source=[2, 'output'], target=[6, 'input']),
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
