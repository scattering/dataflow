"""
Triple Axis Spectrometer reduction and analysis modules
"""
import math
import os
from pprint import pprint

import numpy

from .. import config
from ..core import Instrument, Datatype
from ..modules.load import load_module
from ..modules.join import join_module
from ..modules.scale import scale_module
from ..modules.save import save_module

TAS_DATA = 'data1d.tas'

# ==== Fake data store ===
FILES = {}
def init_data():
    global FILES
    f1 = {'name': 'f1.bt7',
          'x': [1, 2, 3, 4, 5., 6, 7, 8],
          'y': [20, 40, 60, 80, 60, 40, 20, 6],
          'monitor': [100]*8,
          }
    f2 = {'name': 'f2.bt7',
          'x': [4, 5, 6, 7, 8, 9],
          'y': [37, 31, 18, 11, 2, 1],
          'monitor': [50]*6,
          }
    f1['dy'] = [math.sqrt(v) for v in f1['y']]
    f2['dy'] = [math.sqrt(v) for v in f2['y']]
    for f in f1,f2: FILES[f['name']] = f
def save_data(data, name):
    FILES[name] = data
def load_data(name):
    return FILES.get(name, None)

# === Fake reduction pacakge ===
#
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
        for x,y,dy,mon in zip(f['x'],f['y'],f['dy'],f['monitor']):
            if x not in new: new['x'] = (0,0,0)
            Sy,Sdy,Smon = new['x']
            new[x] = (y+Sy,dy**2+Sdy,mon+Smon)
    points = []
    for xi in sorted(new.keys()):
        Sy,Sdy,Smon = new[xi]
        points.append((xi,Sy,math.sqrt(Sdy),Smon))
    x,y,dy,mon = zip(*points)

    basename = min(f['name'] for f in files)
    outname = os.path.splitext(basename)[0] + '.join'
    result = {'name': outname,'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    return result

def data_scale(data, scale):
    x = data['x']
    y = [v*scale for v in data['y']]
    dy = [v*scale for v in data['dy']]
    mon = [v*scale for v in data['monitor']]
    basename = data['name']
    outname = os.path.splitext(basename)[0] + '.scale'
    result = {'name': outname,'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    return result



# ==== Data types ====

data1d = Datatype(id=TAS_DATA,
                  name='1-D Triple Axis Data',
                  plot='tasplot')



# === Component binding ===

def load_action(files=None, intent=None):
    print "loading",files
    result = [load_data(f) for f in files]
    #print "loaded"; pprint(result)
    return dict(output=result)
load = load_module(id='tas.load', datatype=TAS_DATA,
                   version='1.0', action=load_action)

def save_action(input=None, ext=None):
    # Note that save does not accept inputs from multiple components, so
    # we only need to deal with the bundle, not the list of bundles.
    # This is specified by terminal['multiple'] = False in modules/save.py
    for f in input: _save_one(f,ext)
    return {}
def _save_one(input, ext):
    #pprint(input)
    outname = input['name']
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0],ext])
    print "saving",input['name'],'as',outname
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


def join_action(input=None, align=None):
    # This is confusing because load returns a bundle and join, which can
    # link to multiple loads, has a list of bundles.  So flatten this list.
    # The confusion between bundles and items will bother us continuously,
    # and it is probably best if every filter just operates on and returns
    # bundles, which I do in this example.
    flat = []
    for bundle in input: flat.extend(bundle)
    print "joining on",", ".join(align)
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

def scale_action(input=None, scale=None):
    # operate on a bundle; need to resolve confusion between bundles and
    # individual inputs
    print "scale by",scale
    if numpy.isscalar(scale): scale = [scale]*len(input)
    flat = []
    for bundle in input: flat.extend(bundle)
    result = [data_scale(f, s) for f,s in zip(flat,scale)]
    return dict(output=result)
scale = scale_module(id='tas.scale', datatype=TAS_DATA, 
                     version='1.0', action=scale_action)





# ==== Instrument definitions ====
BT7 = Instrument(id='ncnr.tas.bt7',
                 name='NCNR BT7',
                 archive=config.NCNR_DATA+'/bt7',
                 menu=[('Input',[load, save]),
                       ('Reduction', [join, scale])
                       ],
                 requires=[config.JSCRIPT+'/tasplot.js'],
                 datatypes=[data1d],
                 )

# Return a list of triple axis instruments
init_data()
instruments = [BT7]

