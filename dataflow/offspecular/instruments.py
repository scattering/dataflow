"""
Offspecular reflectometry reduction modules
"""
import os, sys, math, numpy
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir)
from pprint import pprint

from dataflow import config
from dataflow.calc import run_template
from dataflow.core import Datatype, Instrument, Template, register_instrument
from dataflow.modules.load import load_module
from dataflow.modules.join import join_module
from dataflow.modules.scale import scale_module
from dataflow.modules.save import save_module
from dataflow.modules.autogrid import autogrid_module
from dataflow.modules.offset import offset_module
from dataflow.modules.wiggle import wiggle_module
from dataflow.modules.pixels_two_theta import pixels_two_theta_module
from dataflow.modules.two_theta_qxqz import two_theta_qxqz_module
from reduction.offspecular.filters import *


# Datatype
OSPEC_DATA = 'data1d.ospec'
data2d = Datatype(id=OSPEC_DATA,
                  name='2-D Offspecular Data',
                  plot='ospecplot')


# Load module
def load_action(files=None, intent=None):
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
    outname = initname = input.extrainfo["path"] + "/" + input.extrainfo.get("filename", default_filename)
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    input.write(outname)
save = save_module(id='ospec.save', datatype=OSPEC_DATA,
                   version='1.0', action=save_action)


# Autogrid module
def autogrid_action(input=None):
    print "gridding"
    result = [_autogrid(bundle) for bundle in input]
    return dict(output=result)
def _autogrid(input, extra_grid_point=True, min_step=1e-10):
    return Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                   version='1.0', action=autogrid_action)


# Join module
def join_action(input=None):
    print "joining"
    result = [_join(bundle) for bundle in input]
    return dict(output=result)
def _join(list_of_datasets, grid=None):
    return Combine().apply(list_of_datasets, grid=grid)
join = join_module(id='ospec.join', datatype=OSPEC_DATA, version='1.0', action=join_action)


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
def pixels_two_theta_action(input=None):
    print "converting pixels to two theta"
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_pixels_two_theta(f) for f in flat]
    return dict(output=result)
def _pixels_two_theta(data):
    return PixelsToTwotheta().apply(data)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action)


# Two theta to qxqz module
def two_theta_qxqz_action(input=None):
    print "converting theta and two theta to qx and qz"
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_two_theta_qxqz(f) for f in flat]
    return dict(output=result)
def _two_theta_qxqz(data):
    return ThetaTwothetaToQxQz().apply(data)
two_theta_qxqz = two_theta_qxqz_module(id='ospec.qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_qxqz_action)

#Instrument definitions
ANDR = Instrument(id='ncnr.ospec.andr',
                 name='NCNR ANDR',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, save]),
                       ('Reduction', [autogrid, join, offset, wiggle, pixels_two_theta, two_theta_qxqz])
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d],
                 )
instruments = [ANDR]

# Testing
if __name__ == '__main__':
    for instrument in instruments:
        register_instrument(instrument)
    path, ext = dir + '/sampledata/ANDR/sabc/Isabc20', '.cg1'
    files = [path + str(i + 1).zfill(2) + ext for i in range(1, 12)]
    modules = [
        dict(module="ospec.load", position=(5, 20),
             config={'files': files, 'intent': 'signal'}),
        dict(module="ospec.save", position=(280, 40), config={'ext': 'dat'}),
        dict(module="ospec.grid", position=(360 , 60), config={}),
        dict(module="ospec.join", position=(400 , 80), config={}),
        dict(module="ospec.offset", position=(420 , 100), config={'offsets':{'theta':0.1}}),
        dict(module="ospec.wiggle", position=(440 , 120), config={}),
        dict(module="ospec.twotheta", position=(460 , 140), config={}),
        dict(module="ospec.qxqz", position=(480 , 160), config={}),
        ]
    wires = [
        dict(source=[0, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
        dict(source=[5, 'output'], target=[6, 'input']),
        dict(source=[6, 'output'], target=[7, 'input']),
        dict(source=[7, 'output'], target=[1, 'input']),
        ]
    config = [d['config'] for d in modules]
    template = Template(name='test ospec',
                        description='example ospec diagram',
                        modules=modules,
                        wires=wires,
                        instrument=ANDR.id,
                        )
    result = run_template(template, config)
    
    # output of the qxqz: result[7]['output'][0]
    data = result[7]['output'][0]
    intensity = [numpy.amin(data[0], axis=0)[0], numpy.amax(data[0], axis=0)[0]]
    print "Min intensity:", intensity[0]
    print "Max intensity:", intensity[1]
    qx = [numpy.amin(data._info[0]['values']), numpy.amax(data._info[0]['values'])]
    print "Min qx:", qx[0]
    print "Max qx:", qx[1]
    qz = [numpy.amin(data._info[1]['values']), numpy.amax(data._info[1]['values'])]
    print "Min qz:", qz[0]
    print "Max qz:", qz[1]
    dimensions = [len(data._info[0]['values']), len(data._info[1]['values'])]
    print "Dimensions:", dimensions
    counts = data[0][:, 0].tolist()
    print "Intensities:", counts
    import json
    print json.dumps(dict(intensity=intensity, qx=qx, qz=qz, dimensions=dimensions, counts=counts))
#    print numpy.ravel(result[7]['output'][0])
#    print result[7]['output'][0]._info
#    data = result[7]['output'][0] # output of the qxqz conversion
#    assert data.all() == eval(data.extrainfo["CreationStory"]).all() # verify the creation story (will this have much use?)
