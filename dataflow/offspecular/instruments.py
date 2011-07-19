"""
Offspecular reflectometry reduction modules
"""
import os, sys
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(dir)

# left here for testing purposes
# python uses __name__ for relative imports so I cannot use
# the ... in place of dataflow when testing
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
from dataflow.reduction.offspecular.filters import *
from dataflow.reduction.offspecular.he3analyzer import *
from dataflow.reduction.offspecular.FilterableMetaArray import FilterableMetaArray

OSPEC_DATA = 'data2d.ospec'
data2d = Data(OSPEC_DATA, FilterableMetaArray)
OSPEC_DATA_HE3 = OSPEC_DATA + '.he3'
datahe3 = Data(OSPEC_DATA_HE3, He3AnalyzerCollection)

# Load module
def load_action(files=[], intent=''):
    print "loading", files
    result = [_load_data(f) for f in files] # not bundles
    return dict(output=result)
def _load_data(name):
    (dirName, fileName) = os.path.split(name)
    return LoadICPData(fileName, path=dirName, auto_PolState=True)
load = load_module(id='ospec.load', datatype=OSPEC_DATA,
                   version='1.0', action=load_action)

# Save module
def save_action(input=[], ext=None):
    for f in input: _save_one(f, ext) # not bundles
    return {}
def _save_one(input, ext):
    default_filename = "default.cg1"
    # modules like autogrid return MetaArrays that don't have filenames
    outname = initname = input._info[-1]["path"] + "/" + input._info[-1].get("filename", default_filename)
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    input.write(outname)
save = save_module(id='ospec.save', datatype=OSPEC_DATA,
                   version='1.0', action=save_action)

# Autogrid module
def autogrid_action(input=[], extra_grid_point=True, min_step=1e-10):
    print "gridding"
    return dict(output=[Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)])
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                   version='1.0', action=autogrid_action)

# Combine module
def combine_action(input=[], grid=None):
    print "joining"
    output_grid = None
    if grid != None:
        output_grid = grid[0]
    return dict(output=[Combine().apply(input, grid=output_grid)])
combine = combine_module(id='ospec.combine', datatype=OSPEC_DATA, version='1.0', action=combine_action)

# Offset module
def offset_action(input=[], offsets={}):
    print "offsetting"
    result = CoordinateOffset().apply(input, offsets=offsets)
    return dict(output=result)
offset = offset_module(id='ospec.offset', datatype=OSPEC_DATA, version='1.0', action=offset_action)

# Wiggle module
def wiggle_action(input=[], amp=0.14):
    print "wiggling"
    result = WiggleCorrection().apply(input, amp=amp)
    return dict(output=result)
wiggle = wiggle_module(id='ospec.wiggle', datatype=OSPEC_DATA, version='1.0', action=wiggle_action)

# Pixels to two theta module
def pixels_two_theta_action(input=[], pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6):
    print "converting pixels to two theta"
    result = PixelsToTwotheta().apply(input, pixels_per_degree=pixels_per_degree, qzero_pixel=qzero_pixel, instr_resolution=instr_resolution)
    return dict(output=result)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action)

# Two theta to qxqz module
def two_theta_qxqz_action(input=[], output_grid=None, wavelength=5.0):
    print "converting theta and two theta to qx and qz"
    grid = None
    if output_grid != None:
        grid = output_grid[0]
    result = ThetaTwothetaToQxQz().apply(input, output_grid=grid, wavelength=wavelength)
    return dict(output=result)
two_theta_qxqz = two_theta_qxqz_module(id='ospec.qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_qxqz_action)

# ======== Polarization modules ===========

# Load he3 module
def load_he3_action(files=[], cells=[]):
    print "loading he3", files
    if cells == []:
        cells = [[]] * len(files)
    result = [_load_he3_data(f, cell) for f, cell in zip(files, cells)] # not bundles
    return dict(output=result)
def _load_he3_data(name, cells):
    (dirName, fileName) = os.path.split(name)
    return He3AnalyzerCollection(filename=fileName, path=dirName, cells=cells)
load_he3 = load_he3_module(id='ospec.loadhe3', datatype=OSPEC_DATA_HE3,
                   version='1.0', action=load_he3_action)

# Append polarization matrix module
def append_polarization_matrix_action(input=[], he3cell=None):
    print "appending polarization matrix"
    he3analyzer = None
    if he3cell != None:
        he3analyzer = he3cell[0]
    return dict(output=[AppendPolarizationMatrix().apply(input, he3cell=he3analyzer)])
append_polarization = append_polarization_matrix_module(id='ospec.append', datatype=OSPEC_DATA,
                    cell_datatype=OSPEC_DATA_HE3, version='1.0', action=append_polarization_matrix_action)

# Combine polarized module
def combine_polarized_action(input=[], grid=None):
    print "combining polarized"
    output_grid = None
    if grid != None:
        output_grid = grid[0]
    return dict(output=[CombinePolarized().apply(input, grid=output_grid)])
combine_polarized = combine_polarized_module(id='ospec.comb_polar', datatype=OSPEC_DATA,
                                             version='1.0', action=combine_polarized_action)

# Polarization correction module
def polarization_correct_action(input=[], assumptions=0, auto_assumptions=True):
    print "polarization correction"
    return dict(output=[PolarizationCorrect().apply(polar_dict, assumptions=assumptions, auto_assumptions=auto_assumptions) for polar_dict in input])
correct_polarized = polarization_correct_module(id='ospec.correct_polar', datatype=OSPEC_DATA,
                                             version='1.0', action=polarization_correct_action)

#Instrument definitions
ANDR = Instrument(id='ncnr.ospec.andr',
                 name='NCNR ANDR',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, save]),
                       ('Reduction', [autogrid, combine, offset, wiggle, pixels_two_theta, two_theta_qxqz]),
                       ('Polarization reduction', [load_he3, append_polarization, combine_polarized, correct_polarized]),
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d, datahe3],
                 )
instrmnts = [ANDR]
for instrument in instrmnts:
    register_instrument(instrument)

# Testing
if __name__ == '__main__':
    path, ext = dir + '/dataflow/sampledata/ANDR/sabc/Isabc20', '.cg1'
    files = [path + str(i + 1).zfill(2) + ext for i in range(1, 12)]
    modules = [
        dict(module="ospec.load", position=(50, 50),
             config={'files': files, 'intent': 'signal'}),
        dict(module="ospec.save", position=(650, 350), config={'ext': 'dat'}),
        dict(module="ospec.combine", position=(150, 100), config={}),
        dict(module="ospec.offset", position=(250, 150), config={'offsets':{'theta':0}}),
        dict(module="ospec.wiggle", position=(350, 200), config={}),
        dict(module="ospec.twotheta", position=(450, 250), config={}),
        dict(module="ospec.qxqz", position=(550, 300), config={}),
        dict(module="ospec.grid", position=(600, 350), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[5, 'input']),
        dict(source=[5, 'output'], target=[2, 'input']),
        dict(source=[5, 'output'], target=[7, 'input']),
        dict(source=[7, 'output'], target=[2, 'grid']),
        dict(source=[2, 'output'], target=[6, 'input']),
        dict(source=[6, 'output'], target=[1, 'input']),
    ]
    config = [d['config'] for d in modules]
    template = Template(name='test ospec',
                        description='example ospec diagram',
                        modules=modules,
                        wires=wires,
                        instrument=ANDR.id,
                        )
    #result = run_template(template, config)
    #print "Starting again. This time should be A LOT quicker (if the server was empty at runtime)."
    #result2 = run_template(template, config)
    result = get_plottable(template, config, template.order()[-2], 'output')
    #print "Writing to files"
    #for nodenum, plottable in result.items():
    #    for terminal_id, plot in plottable.items():
    #        with open('data/' + terminal_id + "_" + str(nodenum) + ".txt", "w") as f:
    #            for format in plot:
    #                f.write(format + "\n")
    print "Done"
