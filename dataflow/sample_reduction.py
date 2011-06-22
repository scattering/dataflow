"""
Example to show how to create and run a reduction routine.
"""
import os, sys, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataflow import config
from dataflow.calc import run_template
from dataflow.core import Module, Datatype, Instrument, Template, register_instrument
from dataflow.modules.load import load_module
from dataflow.modules.save import save_module
from numpy.random import random
from pprint import pprint

ROWAN_DATA = 'data1d.rowan'

# ====== Define the module =======

def random_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Module for adding random values to a dataset"""

    # Define the icon with proper location and terminal sizes
    icon = {
        'URI': config.IMAGES + "random.png",
        'terminals': {
            'input': (0, 10, -1, 0),
            'output': (20, 10, 1, 0),
        }
    }
    
    # Define the terminal details
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='transformed data',
             ),
    ]

    # One field: the largest amount of displacement from the given data
    # |transformed_data - data| <= |max_change|
    random_field = {
        "type":"int",
        "label": "Maximum offset",
        "name": "max_change",
        "value": 1.0,
    }

    # Combine everything into a module
    module = Module(id=id,
                  name='Random',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[random_field] + fields,
                  action=action,
                  )
    return module

# ======== Define the action and declare the module =======

def _offset(max_change):
    return (1 if random() >= .5 else -1) * random()*(max_change + 1)
def _data_randomize(data, max_change):
    x = [v + offset(max_change) for v in data['x']]
    y = [v + offset(max_change) for v in data['y']]
    dy = [v + offset(max_change) for v in data['dy']]
    mon = [v + offset(max_change) for v in data['monitor']]
    basename = data['name']
    outname = os.path.splitext(basename)[0] + '.random'
    result = {'name': outname, 'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    return result
def random_action(input=None, max_change=None):
    """Action that adds or subtracts random values under a given limit."""
    print "randomize <=", max_change
    flat = []
    # operate on a bundle rather than individual input
    # because the multiple field is True
    for bundle in input: flat.extend(bundle)
    result = [data_randomize(f, max_change) for f in flat]
    return dict(output=result)
rand = random_module(id='rowan.random', datatype=ROWAN_DATA,
                     version='1.0', action=random_action)

# ======== Other modules ==========

def load_action(files=None, intent=None):
    print "loading", files
    result = [load_data(f) for f in files]
    return dict(output=result)
load = load_module(id='rowan.load', datatype=ROWAN_DATA,
                   version='1.0', action=load_action)

def save_action(input=None, ext=None):
    for f in input: _save_one(f, ext)
    return {}
def _save_one(input, ext):
    outname = input['name']
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", input['name'], 'as', outname
    save_data(input, name=outname)
save_ext = {
    "type":"[string]",
    "label": "Save extension",
    "name": "ext",
    "value": "",
}
save = save_module(id='rowan.save', datatype=ROWAN_DATA,
                   version='1.0', action=save_action,
                   fields=[save_ext])

# ========== Fake data store =============
FILES = {}
def init_data():
    global FILES
    f1 = {'name': 'f1.rowan26',
          'x': [1, 2, 3, 4, 5., 6, 7, 8],
          'y': [20, 40, 60, 80, 60, 40, 20, 6],
          'monitor': [100] * 8,
          }
    f2 = {'name': 'f2.rowan26',
          'x': [4, 5, 6, 7, 8, 9],
          'y': [37, 31, 18, 11, 2, 1],
          'monitor': [50] * 6,
          }
    f1['dy'] = [math.sqrt(v) for v in f1['y']]
    f2['dy'] = [math.sqrt(v) for v in f2['y']]
    for f in f1, f2: FILES[f['name']] = f
def save_data(data, name):
    FILES[name] = data
def load_data(name):
    return FILES.get(name, None)

# ========== Data and instrument definitions ========

rowan1d = Datatype(id=ROWAN_DATA,
                  name='1-D Rowan Data',
                  plot='rowanplot')
ROWAN26 = Instrument(id='ncnr.rowan26',
                 name='NCNR ROWAN26',
                 archive=config.NCNR_DATA + '/rowan26',
                 menu=[('Input', [load, save]),
                       ('Reduction', [rand])
                       ],
                 requires=[config.JSCRIPT + '/rowanplot.js'],
                 datatypes=[rowan1d],
                 )
init_data()
instruments = [ROWAN26]


# ========== Run the reductions =========
register_instrument(ROWAN26)
modules = [
    dict(module="rowan.load", position=(5, 20),
         config={'files': ['f1.rowan26'], 'intent': 'signal'}),
    dict(module="rowan.random", position=(160, 20), config={'max_change': 50}),
    dict(module="rowan.save", position=(280, 40), config={'ext': 'dat'}),
    ]
wires = [
    dict(source=[0, 'output'], target=[1, 'input']),
    dict(source=[1, 'output'], target=[2, 'input']),
    ]
# I'm unsure why config is needed currently
config = [
    {},
    {},
    {},
    ]
template = Template(name='test rowan',
                    description='example ROWAN diagram',
                    modules=modules,
                    wires=wires,
                    instrument=ROWAN26.id,
                    )
result = run_template(template, config)
pprint(result)

