"""
Triple Axis Spectrometer reduction and analysis modules
"""
import math, os, sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pprint import pprint
from dataflow.reduction.tripleaxis.data_abstraction import TripleAxis, filereader
from dataflow.dataflow.calc import run_template
import numpy

#Running this as __name__="__main__" will require direct instead of relative imports
#TODO - change to relative imports when this code is incorporated in project

from dataflow.dataflow import config
from dataflow.dataflow.core import Instrument, Datatype, Template, register_instrument

#from dataflow.dataflow.modules.load import load_module
from dataflow.dataflow.modules.join import join_module
from dataflow.dataflow.modules.scale import scale_module
from dataflow.dataflow.modules.save import save_module
from dataflow.dataflow.modules.tas_normalize_monitor import normalize_monitor_module
from dataflow.dataflow.modules.tas_detailed_balance import detailed_balance_module
from dataflow.dataflow.modules.tas_monitor_correction import monitor_correction_module
from dataflow.dataflow.modules.tas_volume_correction import volume_correction_module
from dataflow.dataflow.modules.tas_load import load_module

TAS_DATA = 'data1d.tas'

# Reduction operations may refer to data from other objects, but may not
# modify it.  Instead of modifying, first copy the data and then work on
# the copy.
#
def data_join(files, align):
    # Join code: belongs in reduction.tripleaxis
    #if align != 'x': raise TypeError("Can only align on x for now")
    align = 'x' # Ignore align field for now since our data only has x,y,dy
    new = {}
    #print "files"; pprint(files)
    for f in files:
        for x, y, dy, mon in zip(f['x'], f['y'], f['dy'], f['monitor']):
            if x not in new: new['x'] = (0, 0, 0)
            Sy, Sdy, Smon = new['x']
            new[x] = (y + Sy, dy ** 2 + Sdy, mon + Smon)
    points = []
    for xi in sorted(new.keys()):
        Sy, Sdy, Smon = new[xi]
        points.append((xi, Sy, math.sqrt(Sdy), Smon))
    x, y, dy, mon = zip(*points)

    basename = min(f['name'] for f in files)
    outname = os.path.splitext(basename)[0] + '.join'
    result = {'name': outname, 'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    return result

def data_scale(data, scale):
    x = data['x']
    y = [v * scale for v in data['y']]
    dy = [v * scale for v in data['dy']]
    mon = [v * scale for v in data['monitor']]
    basename = data['name']
    outname = os.path.splitext(basename)[0] + '.scale'
    result = {'name': outname, 'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    return result

# ==== Data types ====

data1d = Datatype(id=TAS_DATA,
                  name='1-D Triple Axis Data',
                  plot='tasplot')



# === Component binding ===

def load_action(files=None, intent=None, position=None, xtype=None):
    print "loading", files
    result = [filereader(f) for f in files]
    return dict(output=result)
load = load_module(id='tas.load', datatype=TAS_DATA,
                   version='1.0', action=load_action)

def save_action(input=None, ext=None,xtype=None, position=None):
    # Note that save does not accept inputs from multiple components, so
    # we only need to deal with the bundle, not the list of bundles.
    # This is specified by terminal['multiple'] = False in modules/save.py
    for f in input: _save_one(f, ext)
    return {}
def _save_one(input, ext):
    #pprint(input)
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
save = save_module(id='tas.save', datatype=TAS_DATA,
                   version='1.0', action=save_action,
                   fields=[save_ext])


def join_action(input=None, align=None, xtype=None, position=None):
    # This is confusing because load returns a bundle and join, which can
    # link to multiple loads, has a list of bundles.  So flatten this list.
    # The confusion between bundles and items will bother us continuously,
    # and it is probably best if every filter just operates on and returns
    # bundles, which I do in this example.
    flat = []
    for bundle in input: flat.extend(bundle)
    print "joining on", ", ".join(align)
    #pprint(flat)
    result = [data_join(flat, align)]
    return dict(output=result)
align_field = {
    "type":"[string]",
    "label": "Align on",
    "name": "align",
    "value": "",
}
join = join_module(id='tas.join', datatype=TAS_DATA,
                   version='1.0', action=join_action,
                   fields=[align_field])

def scale_action(input=None, scale=None, xtype=None, position=None):
    # operate on a bundle; need to resolve confusion between bundles and
    # individual inputs
    print "scale by", scale
    if numpy.isscalar(scale): scale = [scale] * len(input)
    flat = []
    for bundle in input: flat.extend(bundle)
    result = [data_scale(f, s) for f, s in zip(flat, scale)]
    return dict(output=result)
scale = scale_module(id='tas.scale', datatype=TAS_DATA,
                     version='1.0', action=scale_action)

#All TripleAxis reductions below require that:
#  'input' be a TripleAxis object (see data_abstraction.py)
def detailed_balance_action(input):
    for tasinstrument in input:
        tasinstrument.detailed_balance()
    return dict(output=input)

def normalize_monitor_action(input, target_monitor):
    #Requires the target monitor value
    for tasinstrument in input:
        tasinstrument.normalize_monitor(target_monitor)
    return dict(output=input)

def monitor_correction_action(input, instrument_name):
    #Requires instrument name, e.g. 'BT7'.  
    #Check monitor_correction_coordinates.txt for available instruments
    for tasinstrument in input:
        tasinstrument.harmonic_monitor_correction()
    return dict(ouput=input)
    
def volume_correction_action(input):
    for tasinstrument in input:
        tasinstrument.resolution_volume_correction()
    return dict(output=input)

normalizemonitor = normalize_monitor_module(id='tas.normalize_monitor', datatype=TAS_DATA,
                                            version='1.0', action=normalize_monitor_action)

detailedbalance = detailed_balance_module(id='tas.detailed_balance', datatype=TAS_DATA,
                                          version='1.0', action=detailed_balance_action)

monitorcorrection = monitor_correction_module(id='tas.monitor_correction', datatype=TAS_DATA,
                                          version='1.0', action=monitor_correction_action)

volumecorrection = volume_correction_module(id='tas.volume_correction', datatype=TAS_DATA,
                                          version='1.0', action=volume_correction_action)


# ==== Instrument definitions ====
BT7 = Instrument(id='ncnr.tas.bt7',
                 name='NCNR BT7',
                 archive=config.NCNR_DATA + '/bt7',
                 menu=[('Input', [load, save]),
                       ('Reduction', [join, scale, normalizemonitor, detailedbalance, 
                                      monitorcorrection, volumecorrection])
                       ],
                 requires=[config.JSCRIPT + '/tasplot.js'],
                 datatypes=[data1d],
                 )


# Return a list of triple axis instruments
instruments = [BT7]
for instrument in instruments:
    register_instrument(instrument)

modules = [
    dict(module="tas.load"),
    dict(module="tas.normalize_monitor"),
    #dict(module="tas.detailed_balance"),
    #dict(module="tas.monitor_correction"),
    #dict(module="tas.volume_correction"),
    ]
wires = [
    dict(source=[0, 'output'], target=[1, 'input']),
    #dict(source=[1, 'output'], target=[2, 'input']),
    ]
config = [
    {'files':['/home/alex/Desktop/dataflow/reduction/tripleaxis/EscanQQ7HorNSF91831.bt7']},
    {'target_monitor': 900000},
    #{},
    #{'instrument_name': 'BT7'},
    #{}
    ]
template = Template(name='test reduction',
                    description='example reduction diagram',
                    modules=modules,
                    wires=wires,
                    instrument=BT7.id,
                    )
# the actual call to perform the reduction
result = run_template(template, config)
print "done"