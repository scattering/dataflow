"""
Triple Axis Spectrometer reduction and analysis filters
"""

from ..core import Instrument, Datatype, register_module
from ..modules.join import join_module
from ..modules.scale import scale_module
from ..modules.normalize import normalize_module
from ..modules.footprintmodule import footprint_module
from dataflow.reduction.reflectometry.filters import FootprintCorrection

#def join_action(input=None):
#    print "combining", input
#    result = None
#    return dict(output=result)
#join = join_module(id='refl.join', datatype='data1d.refl', \
#                   version='1.0', action=join_action)

#def scale_action(input=None, scale=None):
#    print "scale", input, "by", scale
#    result = None
#    return dict(output=result)
#scale = scale_module(id='refl.scale', datatype='data1d.refl',
#                     version='1.0', action=scale_action)

#def subtract_action(input=None):
#    result = None
#    return dict(output=result)
#subtract = scale_module(id='refl.subtract', datatype='data1d.refl',
#                     version='1.0', action=subtract_action)

#def normalize_action(input=None):
#    result = None
#    return dict(output=result)

# FootprintCorrection module
def footprint_action(input=[], start="", end="", slope="", intercept=""):
    print "applying footprint correction"
    return dict(output=FootprintCorrection().apply(input, start, end, slope, intercept)) 
footprint_data = footprint_module(id='refl.footprint', datatype='data1d.refl',
                    version='1.0', action=footprint_action, filterModule=FootprintCorrection)
    
#normalize = normalize_module(id='refl.normalize', datatype='data1d.refl',
#                             version='1.0', action=normalize_action)

data1d = Datatype(id='data1d.refl',
                  name='1-D Reflectometry Data',
                  plot='reflplot')

input = [load]
#reduction = [join, scale, subtract, normalize, footprint, polcor]
reduction = [footprint]

PBR = Instrument(id='ncnr.refl.pbr',
                 name='NCNR PBR',
                 archive='http://www.ncnr/nist.gov/data/pbr',
                 menu=[
                       ('Input', input),
                       ('Reduction', reduction),
                      ],
                 requires=[],
                 datatypes=[data1d],
                 )

instruments = [PBR]
