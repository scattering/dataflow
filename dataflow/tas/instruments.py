"""
Triple Axis Spectrometer reduction and analysis modules
"""

from ..core import Instrument, Datatype, register_module
from ..modules.load import load_module
from ..modules.join import join_module
from ..modules.scale import scale_module
from ..modules.save import save_module

def join_action(input=None, align=None):
    print "combining",input,"on", ", ".join(align)
    result = None
    return dict(output=result)
align_field = {
    "type":"[string]", 
    "label": "Align on", 
    "name": "align",
    "value": 1.0,
}

join = join_module(id='tas.join', datatype='data1d.tas', \
                   version='1.0', action=join_action)

def scale_action(input=None, scale=None):
    print "scale",input,"by",scale
    result = None
    return dict(output=result)
scale = scale_module(id='tas.scale', datatype='data1d.tas', 
                     version='1.0', action=scale_action)

def load_action(files=None):
    print "load",files
    result = None
    return dict(output=result)
load = load_module(id='tas.load', datatype='data1d.tas',
                   version='1.0', action=load_action)

def save_action(input=None):
    print "save",files
    result = None
    return dict(output=result)
save = save_module(id='tas.save', datatype='data1d.tas',
                   version='1.0', action=save_action)

data1d = Datatype(id='data1d.tas',
                  name='1-D Triple Axis Data',
                  plot='tasplot')

# Specify the modules available for the various instruments
BT7 = Instrument(id='ncnr.tas.bt7',
                 name='NCNR BT7',
                 archive='http://www.ncnr/nist.gov/data/bt7',
                 menu=[('Input',[load, save]),
                       ('Reduction', [join, scale])
                       ],
                 requires=['/media/tasplot.js'],
                 datatypes=[data1d],
                 )

# Return a list of triple axis instruments
instruments = [BT7]
