"""
Offspecular reflectometry reduction modules
"""
import os, sys, math
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir)
from pprint import pprint

from numpy import zeros, arange, resize, ndarray

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
from reduction.offspecular.filters import *
#from reduction.offspecular.FilterableMetaArray import FilterableMetaArray as MetaArray
#from reduction.offspecular.reduction.formats import load as load_icp
#import reduction.offspecular.reduction.rebin as reb


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
    outname = initname = input._info[-1]["path"] + "/" + input._info[-1].get("filename", default_filename)
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    input.write(outname)
save = save_module(id='ospec.save', datatype=OSPEC_DATA,
                   version='1.0', action=save_action)


# Autogrid module
def autogrid_action(input=None):
    result = [_autogrid(bundle) for bundle in input]
    return dict(output=result)
def _autogrid(input, extra_grid_point=True, min_step=1e-10):
    return Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                   version='1.0', action=autogrid_action)


# Join module
def join_action(input=None):
    result = [_join(bundle) for bundle in input]
    return dict(output=result)
def _join(list_of_datasets, grid=None):
    return Combine().apply(list_of_datasets, grid=grid)
join = join_module(id='ospec.join', datatype=OSPEC_DATA, version='1.0', action=join_action)


# Offset module
def offset_action(input=None, offsets={}):
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
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [_pixels_two_theta(f) for f in flat]
    return dict(output=result)
def _pixels_two_theta(data):
    return PixelsToTwotheta().apply(data)
pixels_two_theta = pixels_two_theta_module(id='ospec.twotheta', datatype=OSPEC_DATA, version='1.0', action=pixels_two_theta_action)

#Instrument definitions
ANDR = Instrument(id='ncnr.ospec.andr',
                 name='NCNR ANDR',
                 archive=config.NCNR_DATA + '/andr',
                 menu=[('Input', [load, save]),
                       ('Reduction', [autogrid, join, offset, wiggle, pixels_two_theta])
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
        ]
    wires = [
        dict(source=[0, 'output'], target=[3, 'input']),
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
    result = run_template(template, config)
    #pprint(result)
    data = result[6]['output'][0] # output of the twotheta conversion
    assert data.all() == eval(data._info[-1]["CreationStory"]).all()
