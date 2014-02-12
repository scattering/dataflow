"""
Example to show how to create and run a dataflow reduction routine.
"""
import os, math
import json
import logging

from numpy.random import random

from dataflow import config
from dataflow.core import Module, Instrument, Data, Template, register_instrument
from dataflow.modules.load import load_module
from dataflow.modules.save import save_module

# ========== Data definition ========


# the data id; used for datatype of modules and instrument
ROWAN_DATA = 'data1d.rowan'

class RowanData(object):
    def __init__(self, **kw):
        self.__dict__ = kw
    def dumps(self):
        return json.dumps(self.__dict__)
    def get_plottable(self):
        return self.dumps()

rowan1d = Data(id=ROWAN_DATA, cls=RowanData,
               loaders=[])

# ====== Define a new module =======

def random_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Module for adding random values to a dataset"""

    # Define the icon with proper location and terminal sizes
    # URI: the path to the icon
    # terminals: the input and output sizes (x, y, dx, dy)
    icon = {
        'URI': config.IMAGES + "random.png",
        'terminals': {
            'input': (0, 10, -1, 0),
            'output': (20, 10, 1, 0),
        }
    }
    
    # Define the terminal details
    # The required and multiple keys are used only on input terminals.
    # required: True if input is needed
    # multiple: True if multiple inputs are accepted
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

# helper methods
# as stated before, this module adds random values to the data:
# transformed_data - data| <= |max_change|
def _offset(max_change):
    return (1 if random() >= .5 else -1) * random()*(max_change + 1)
def _data_randomize(data, max_change):
    x = [v + _offset(max_change) for v in data.x]
    y = [v + _offset(max_change) for v in data.y]
    dy = [v + _offset(max_change) for v in data.dy]
    mon = [v + _offset(max_change) for v in data.monitor]
    basename = data.name
    outname = os.path.splitext(basename)[0] + '.random'
    result = {'name': outname, 'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    return RowanData(**result)

# the actual "action" for the rand module
def random_action(input=None, max_change=None):
    """Action that adds or subtracts random values under a given limit."""
    #print "randomize <=", max_change
    flat = []
    # operate on a bundle rather than individual input
    # because the multiple field is True
    for bundle in input: flat.extend(bundle)
    result = [_data_randomize(f, max_change) for f in flat]
    return dict(output=result)
rand = random_module(id='rowan.random', datatype=ROWAN_DATA,
                     version='1.0', action=random_action)

# ======== Actions for standard modules ==========

def load_action(files=None, intent=None):
    """Loads files for data manipulation"""
    #print "loading", files
    result = [load_data(f) for f in files]
    return dict(output=result)
load = load_module(id='rowan.load', datatype=ROWAN_DATA,
                   version='1.0', action=load_action)

def save_action(input=None, ext=None):
    """Saves files to another extension"""
    for f in input: _save_one(f, ext)
    return {}
def _save_one(input, ext):
    outname = input.name
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    logging.info("saving %r as %r"%(input.name, outname))
    save_data(input, name=outname)
save = save_module(id='rowan.save', datatype=ROWAN_DATA,
                   version='1.0', action=save_action)

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
    for f in f1, f2: FILES[f['name']] = RowanData(**f)
def save_data(data, name):
    FILES[name] = data
def load_data(name):
    return FILES.get(name, None)

# ========== Instrument definition ========
# it has three modules: load, save, and rand
# when the instrument is registered, these modules will also be registered
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
for instrument in instruments:
    register_instrument(instrument)


# ========== Run the reductions =========
def sample_diagram():
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
    # I'm unsure why config is needed currently if nothing needs to be supplied
    # However, it does need to be the same length as the modules list
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

    return template, config

def test():
    from dataflow import calc
    calc.verify_examples(__file__,
                         [('sample.test', sample_diagram())],
                         )

def test_template_copy():
    """
    handy place to test copy constructors for dataflow core
    """
    import copy
    template,config = sample_diagram()
    copy.copy(template)
    copy.copy(config)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import json
    from dataflow import calc
    from dataflow.wireit import instrument_to_wireit_language as wlang
    #print "=== Language ===\n", json.dumps(wlang(ROWAN26), indent=2)
    calc.run_example(*sample_diagram())

