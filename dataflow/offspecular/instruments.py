"""
Offspecular reflectometry reduction modules
"""
import os, sys, math, numpy, simplejson, time, json
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(dir)
from pprint import pprint

# left here for testing purposes
# python uses __name__ for relative imports so I cannot use
# the ... in place of dataflow when testing
from dataflow.dataflow import config
from dataflow.dataflow.calc import run_template
from dataflow.dataflow.wireit import template_to_wireit_diagram, instrument_to_wireit_language
from dataflow.dataflow.core import Datatype, Instrument, Template, register_instrument
from dataflow.dataflow.modules.load import load_module
from dataflow.dataflow.modules.join import join_module
from dataflow.dataflow.modules.scale import scale_module
from dataflow.dataflow.modules.save import save_module
from dataflow.dataflow.modules.autogrid import autogrid_module
from dataflow.dataflow.modules.offset import offset_module
from dataflow.dataflow.modules.wiggle import wiggle_module
from dataflow.dataflow.modules.pixels_two_theta import pixels_two_theta_module
from dataflow.dataflow.modules.two_theta_qxqz import two_theta_qxqz_module
from dataflow.reduction.offspecular.filters import *
from dataflow.reduction.offspecular.FilterableMetaArray import FilterableMetaArray as MetaArray


#from ...dataflow import config
#from ...dataflow.calc import run_template
#from ...dataflow.wireit import template_to_wireit_diagram, instrument_to_wireit_language
#from ...dataflow.core import Datatype, Instrument, Template, register_instrument
#from ...dataflow.modules.load import load_module
#from ...dataflow.modules.join import join_module
#from ...dataflow.modules.scale import scale_module
#from ...dataflow.modules.save import save_module
#from ...dataflow.modules.autogrid import autogrid_module
#from ...dataflow.modules.offset import offset_module
#from ...dataflow.modules.wiggle import wiggle_module
#from ...dataflow.modules.pixels_two_theta import pixels_two_theta_module
#from ...dataflow.modules.two_theta_qxqz import two_theta_qxqz_module
#from ...reduction.offspecular.filters import *
#from ...reduction.offspecular.FilterableMetaArray import FilterableMetaArray as MetaArray


# Datatype
OSPEC_DATA = 'data2d.ospec'
data2d = Datatype(id=OSPEC_DATA,
                  name='2-D Offspecular Data',
                  plot='ospecplot')

# Convert FilterableMetaArrays to plotting specification
# plottable_data = {
#     'z':  [ [1, 2], [3, 4] ],
#     'title': 'This is the title',
#     'dims': {
#       'xmax': 1.0,
#       'xmin': 0.0, 
#       'ymin': 0.0, 
#       'ymax': 12.0,
#       'xdim': 2,
#       'ydim': 2,
#     }
#     'xlabel': 'This is my x-axis label',
#     'ylabel': 'This is my y-axis label',
#     'zlabel': 'This is my z-axis label',
# };

#def convert_to_plottable(result):
#    print "Starting new converter"
#    res = []
#    for data in result:
#        #print _plot_format(metaarray)
#        res.append(data.get_plottable())
#    #return dict(output=result)
#    #print "\n" * 10
#    #raw_input("I'm waiting...")
#    #print "Finished converting\n"
#    return dict(output=res)


#def _plot_format(data):
#    #[[[1,2,3,4],[5,6,7,8],[9,10,11,12]][[1,2,3,4],[3,4,2,4],[2,7,8,0]],...]
#    #data[x][:,0] is the counts
#    #print "\tWorking on output"
#    z = [arr[:, 0].tolist() for arr in data]
#    #print "\t\tFinished z conversion"
#    axis = ['x', 'y']
#    dims = {}
#    for index, label in enumerate(axis):
#        arr = data._info[index]['values']
#        dims[axis[index] + 'min'] = numpy.amin(arr)
#        dims[axis[index] + 'max'] = numpy.amax(arr)
#        dims[axis[index] + 'dim'] = numpy.alen(arr)
#    xlabel = data._info[0]['name']
#    ylabel = data._info[1]['name']
#    zlabel = data._info[2]['cols'][0]['name']
#    title = 'AND/R data' # That's creative enough, right?
#    dump = dict(z=z, title=title, dims=dims, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel)
##    print "lulzz"
##    timed = time.time()
#    res = simplejson.dumps(dump, sort_keys=True, indent=2)
##    res = simplejson.dumps(dump)
##    print time.time() - timed
#    return res
##    return json.dumps(dump)


# ========= Module definitions ===========

# Load module
def load_action(files=None, intent=None, position=None):
    print "loading", files
    result = [_load_data(f) for f in files] # not bundles
    return dict(output=result)
def _load_data(name):
    (dirName, fileName) = os.path.split(name)
    return LoadICPData(fileName, path=dirName, auto_PolState=True)
load = load_module(id='ospec.load', datatype=OSPEC_DATA,
                   version='1.0', action=load_action)


# Save module
def save_action(input=None, ext=None):
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
def autogrid_action(input=None, extra_grid_point=True, min_step=1e-10):
    print "gridding"
    result = [_autogrid(bundle, extra_grid_point, min_step) for bundle in input]
    return dict(output=result)
def _autogrid(input, extra_grid_point, min_step):
    return Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                   version='1.0', action=autogrid_action)


# Join module
def join_action(input=None, grid=None):
    print "joining"
    result = [_join(bundle, grid) for bundle in input]
    return dict(output=result)
def _join(list_of_datasets, grid):
    return Combine().apply(list_of_datasets, grid=grid)
grid_field = {
        "type":"MetaArray",
        "label": "grid",
        "name": "grid",
        "value": None,
}
join = join_module(id='ospec.join', datatype=OSPEC_DATA, version='1.0', action=join_action, fields=[grid_field])


# Offset module
def offset_action(input=None, offsets={}):
    print "offsetting"
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_offset(f, offsets) for f in flat]
    return dict(output=result)
def _offset(data, offsets):
    return CoordinateOffset().apply(data, offsets=offsets)
offset = offset_module(id='ospec.offset', datatype=OSPEC_DATA, version='1.0', action=offset_action)


# Wiggle module
def wiggle_action(input=None, amp=0.14):
    print "wiggling"
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_wiggle(f, amp) for f in flat]
    return dict(output=result)
def _wiggle(data, amp):
    return WiggleCorrection().apply(data, amp=amp)
wiggle = wiggle_module(id='ospec.wiggle', datatype=OSPEC_DATA, version='1.0', action=wiggle_action)


# Pixels to two theta module
def pixels_two_theta_action(input=None, pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6):
    print "converting pixels to two theta"
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_pixels_two_theta(f, pixels_per_degree, qzero_pixel, instr_resolution) for f in flat]
    return dict(output=result)
def _pixels_two_theta(data, pixels_per_degree, qzero_pixel, instr_resolution):
    return PixelsToTwotheta().apply(data, pixels_per_degree=pixels_per_degree, qzero_pixel=qzero_pixel, instr_resolution=instr_resolution)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action)


# Two theta to qxqz module
def two_theta_qxqz_action(input=None, output_grid=None, wavelength=5.0):
    print "converting theta and two theta to qx and qz"
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_two_theta_qxqz(f, output_grid, wavelength) for f in flat]
    return dict(output=result)
def _two_theta_qxqz(data, output_grid, wavelength):
    return ThetaTwothetaToQxQz().apply(data, output_grid=output_grid, wavelength=wavelength)
two_theta_qxqz = two_theta_qxqz_module(id='ospec.qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_qxqz_action)

#Instrument definitions
ANDR = Instrument(id='ncnr.ospec.andr',
                 name='NCNR ANDR',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, save]),
                       ('Reduction', [autogrid, join, offset, wiggle, pixels_two_theta, two_theta_qxqz]),
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d],
                 )
instrmnts = [ANDR]

# Testing
if __name__ == '__main__':
    # introspection
    #from inspect import getsource
    #from dataflow.dataflow.offspecular import instruments
    #print getsource(instruments)
    #print run_template.__code__
    #sys.exit()
    for instrument in instrmnts:
        register_instrument(instrument)
    path, ext = dir + '/dataflow/sampledata/ANDR/sabc/Isabc20', '.cg1'
    files = [path + str(i + 1).zfill(2) + ext for i in range(1, 12)]
    modules = [
        dict(module="ospec.load", position=(50, 50),
             config={'files': files, 'intent': 'signal'}),
        dict(module="ospec.save", position=(650, 350), config={'ext': 'dat'}),
        #dict(module="ospec.grid", position=(360 , 60), config={}),
        dict(module="ospec.join", position=(150, 100), config={}),
        dict(module="ospec.offset", position=(250, 150), config={'offsets':{'theta':1}}),
        dict(module="ospec.wiggle", position=(350, 200), config={}),
        dict(module="ospec.twotheta", position=(450, 250), config={}),
        dict(module="ospec.qxqz", position=(550, 300), config={}),
        ]
    wires = [
        dict(source=[0, 'output'], target=[2, 'input']),
        dict(source=[2, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
        dict(source=[5, 'output'], target=[6, 'input']),
        dict(source=[6, 'output'], target=[1, 'input']),
        ]
    config = [d['config'] for d in modules]
    template = Template(name='test ospec',
                        description='example ospec diagram',
                        modules=modules,
                        wires=wires,
                        instrument=ANDR.id,
                        )
    #template and instrument tests
    #print json.dumps(instrument_to_wireit_language(ANDR), sort_keys=True, indent=2)
    #print json.dumps(template_to_wireit_diagram(template)) # need name!
    #sys.exit()


    result = run_template(template, config)
    print "Starting again. This time should be A LOT quicker."
    result2 = run_template(template, config)
    #result = [convert_to_plottable(value['output'])  if 'output' in value else {} for key, value in result.items()]
    #assert result[6]['output'][0].all() == result2[6]['output'][0].all()
    #print result2[6]
    #result = [convert_to_plottable(value['output'])  if 'output' in value else {} for key, value in result.items()]
    print "WRITING TO FILE"
    for index, plottable in enumerate(result):
        with open('new_data' + str(index) + '.txt', 'w') as f:
            for format in plottable.get('output', []):
                f.write(format + "\n")
    print "DONE"

    #pprint(result)
    #raw_input("Done looking at formatted output? ")
    #output of the qxqz: result[7]['output'][0]
    #data = result[6]['output'][0]
    #print "\n" * 10, _plot_format(data), "\n" * 10
    #intensity = [numpy.amin(data[0], axis=0)[0], numpy.amax(data[0], axis=0)[0]]
    #print "Min intensity:", intensity[0]
    #print "Max intensity:", intensity[1]
    #qx = [numpy.amin(data._info[0]['values']), numpy.amax(data._info[0]['values'])]
    #print "Min qx:", qx[0]
    #print "Max qx:", qx[1]
    #qz = [numpy.amin(data._info[1]['values']), numpy.amax(data._info[1]['values'])]
    #print "Min qz:", qz[0]
    #print "Max qz:", qz[1]
    #dimensions = [len(data._info[0]['values']), len(data._info[1]['values'])]
    #print "Dimensions:", dimensions
    #counts = data[0][:, 0].tolist()
    #print "Intensities:", counts
    #print json.dumps(dict(intensity=intensity, qx=qx, qz=qz, dimensions=dimensions, counts=counts))
    #print numpy.ravel(result[7]['output'][0])
    #print result[7]['output'][0]._info
    #data = result[7]['output'][0] # output of the qxqz conversion
    #assert data.all() == eval(data._info[-1]["CreationStory"]).all() # verify the creation story (will this have much use?)
