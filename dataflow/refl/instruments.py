"""
Triple Axis Spectrometer reduction and analysis filters
"""

from ..core import Instrument, Datatype, register_module
from ..modules.join import join_module
from ..modules.scale import scale_module
from ..modules.normalize import normalize_module
from ..modules.footprint import footprint

def join_action(input=None):
    print "combining", input
    result = None
    return dict(output=result)
join = join_module(id='refl.join', datatype='data1d.refl', \
                   version='1.0', action=join_action)

def scale_action(input=None, scale=None):
    print "scale", input, "by", scale
    result = None
    return dict(output=result)
scale = scale_module(id='refl.scale', datatype='data1d.refl',
                     version='1.0', action=scale_action)

def subtract_action(input=None):
    result = None
    return dict(output=result)
subtract = scale_module(id='refl.subtract', datatype='data1d.refl',
                     version='1.0', action=subtract_action)

def normalize_action(input=None):
    result = None
    return dict(output=result)
normalize = normalize_module(id='refl.normalize', datatype='data1d.refl',
                             version='1.0', action=normalize_action)

data1d = Datatype(id='data1d.refl',
                  name='1-D Reflectometry Data',
                  plot='reflplot')

input = [load]
reduction = [join, scale, subtract, normalize, footprint, polcor]

NG1 = Instrument(id='ncnr.refl.ng1',
                 name='NCNR NG1',
                 archive='http://www.ncnr/nist.gov/data/ng1',
                 menu=[
                       ('Input', input),
                       ('Reduction', reduction),
                      ],
                 requires=['/media/tasplot.js'],
                 datatypes=[data1d],
                 )

instruments = [NG1]
