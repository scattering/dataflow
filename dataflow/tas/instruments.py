"""
Triple Axis Spectrometer reduction and analysis modules
"""
import os, sys
import types
import json

from reduction.tas import data_abstraction

from .. import config
from ..core import Instrument, Data, Template, register_instrument
    
from .modules.join import join
from .modules.subtract import subtract
from .modules.save import save
from .modules.load import load
from .modules.extract import extract
from .modules.load_chalk import load_chalk
from .modules.normalize_monitor import normalize_monitor
from .modules.detailed_balance import detailed_balance
from .modules.monitor_correction import monitor_correction
from .modules.volume_correction import volume_correction

from .datatypes import data1d


# Reduction operations may refer to data from other objects, but may not
# modify it.  Instead of modifying, first copy the data and then work on
# the copy.
#
#def data_join(files, align):
    ## Join code: belongs in reduction.tas
    ##if align != 'x': raise TypeError("Can only align on x for now")
    #align = 'x' # Ignore align field for now since our data only has x,y,dy
    #new = {}
    ##print "files"; pprint(files)
    #for f in files:
        #for x, y, dy, mon in zip(f['x'], f['y'], f['dy'], f['monitor']):
            #if x not in new: new['x'] = (0, 0, 0)
            #Sy, Sdy, Smon = new['x']
            #new[x] = (y + Sy, dy ** 2 + Sdy, mon + Smon)
    #points = []
    #for xi in sorted(new.keys()):
        #Sy, Sdy, Smon = new[xi]
        #points.append((xi, Sy, math.sqrt(Sdy), Smon))
    #x, y, dy, mon = zip(*points)

    #basename = min(f['name'] for f in files)
    #outname = os.path.splitext(basename)[0] + '.join'
    #result = {'name': outname, 'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    #return result


#All TripleAxis reductions below require that:
#  'input' be a TripleAxis object (see data_abstraction.py)


# ==== Instrument definitions ====
TAS = Instrument(id='ncnr.tas',
                 name='tas',
                 archive=config.NCNR_DATA + '/tas',
                 menu=[('Input', [load, save]),
                       ('Reduction', [join, subtract, normalize_monitor,
                                      detailed_balance,
                                      monitor_correction, volume_correction])
                       ],
                 #requires=[config.JSCRIPT + '/tasplot.js'],
                 datatypes=[data1d],
                 )

# Register the list of triple axis instruments
for instrument in [TAS]:
        register_instrument(instrument)


# ==== Example reductions ====
def bt7_example():
    import reduction.tas
    DATA_ROOT = os.path.dirname(reduction.tas.__file__)
    modules = [
        dict(module="tas.load", position=(10, 150), config={}),
        dict(module="tas.normalize_monitor", position=(270, 20), config={}),
        dict(module="tas.detailed_balance", position=(270, 120), config={}),
        dict(module="tas.monitor_correction", position=(270, 220),
             config={'instrument_name':'BT7'}),
        dict(module="tas.volume_correction", position=(270, 320), config={}),
        dict(module="tas.save", position=(500, 150), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[1, 'input']),
        dict(source=[1, 'output'], target=[2, 'input']),
        dict(source=[2, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
    ]

    config = [
        {'files':[os.path.join(DATA_ROOT,'EscanQQ7HorNSF91831.bt7')]},
        {'target_monitor': 165000},
        {}, {}, {}, {},
    ]

    template = Template(name='test reduction presentation',
                        description='example reduction diagram',
                        modules=modules,
                        wires=wires,
                        instrument=TAS.id,
                        )
    return template, config

def spins_example():
    #for loading spins files 59-71 for plotting
    modules = [
        dict(module="tas.load", position=(10, 40), config={}),
        dict(module="tas.join", position=(250, 40), config={}),
        dict(module="tas.save", position=(400, 40), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[1, 'input']),
        dict(source=[1, 'output'], target=[2, 'input']),
    ]
    config = [{}]*3

    template = Template(name='test reduction presentation',
                        description='example reduction diagram',
                        modules=modules,
                        wires=wires,
                        instrument=TAS.id,
                        )
    return template, config

def test():
    from ..calc import verify_examples
    tests = [
        ('bt7.out', bt7_example()),
        #('spins.out', spins_example()),
    ]
    verify_examples(__file__, tests)

def demo():
    import logging; logging.basicConfig(level=logging.DEBUG)
    from .. import wireit
    from ..calc import run_example
    #print 'language', json.dumps(wireit.instrument_to_wireit_language(TAS), indent=2)
    run_example(*bt7_example(), verbose=False)
    #run_example(*spins_example())

if __name__ == "__main__":
    demo()
