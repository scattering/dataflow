"""
Specular reflectometry reduction and analysis filters
"""

from ..core import Instrument, Data, Template, register_instrument, register_module
from ..modules.load import load_module
from ..modules.save import save_module
#from ..modules.join import join_module
#from ..modules.scale import scale_module
#from ..modules.normalize import normalize_module
from .modules.footprintmodule import footprint_module
from .modules.backgroundmodule import background_module
from .modules.normalizemodule import normalize_module
from .modules.normalizetimemodule import normalize_time_module
#from .filters import FootprintCorrection
from reduction.reflectometry.FilterableMetaArray import FilterableMetaArray
from reduction.reflectometry.filters import LoadICPMany, LoadICPData
from reduction.reflectometry.filters import FootprintCorrection
from reduction.reflectometry.filters import BackgroundSubtraction
from reduction.reflectometry.filters import NormalizeToMonitor
from reduction.reflectometry.filters import NormalizeToTime
#from reduction.offspecular.FilterableMetaArray import FilterableMetaArray
#from reduction.offspecular.filters import LoadICPMany, LoadICPData

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

SPEC_DATA = 'refl.data1d'
data1d = Data(SPEC_DATA, FilterableMetaArray, loaders=[{'function':LoadICPMany, 'id':'LoadICPData'}])

# FootprintCorrection module
def footprint_action(input=[], start="0.0", end="3.0", slope="1.0", intercept="0.0", **kwargs): # executes the FootprintCorrection function
    print "applying footprint correction"
    return dict(output=FootprintCorrection(input, start=start, end=end, slope=slope, intercept=intercept))
    
footprint = footprint_module(id='refl.footprint', datatype='refl.data1d',  # adds FootprintCorrection module option to menu
                    version='1.0', action=footprint_action, filterModule=FootprintCorrection)

footprint.xtype = 'FootprintCorrectContainer' # indicates what module box to use for this module

# BackgroundSubtraction module
def background_action(input=[], background="1.0", **kwargs): # executes BackgroundSubtract function
    print "applying background subtraction"
    return dict(output=BackgroundSubtraction(input, background=background))

background = background_module(id='refl.background', datatype='refl.data1d', # adds Background module option to menu
                    version='1.0', action=background_action, filterModule=BackgroundSubtraction)
                    
background.xtype = 'BackgroundSubtractContainer' # indicates which module box to use for this module

# NormalizeToMonitor module
def normalize_action(input=[], **kwargs):
    print "normalizing"
    return dict(output=NormalizeToMonitor(input))
    
normalize = normalize_module(id='refl.normalize', datatype='refl.data1d',
                             version='1.0', action=normalize_action)
# NormalizeToTime module
def normalize_time_action(input=[], **kwargs):
    print "normalizing"
    return dict(output=NormalizeToTime(input))
    
normalize_time = normalize_time_module(id='refl.normalizetime', datatype='refl.data1d',
                             version='1.0', action=normalize_time_action)

# Load module
load = load_module(id='refl.load', datatype=SPEC_DATA,
                   version='1.0', 
                   #action=load_action, 
                   #fields=OrderedDict({'files': {}, 'autochain-loader':autochain_loader_field, 'auto_PolState': auto_PolState_field, 'PolStates': PolStates_field}), 
                   filterModule=LoadICPData)

# Save module
save = save_module(id='refl.save', datatype=SPEC_DATA,
                   version='1.0', action=None)
save.xtype = 'SaveContainer'

input = [load, save] # places Load and Save module options in one list



#reduction = [join, scale, subtract, normalize, footprint, polcor]
reduction = [footprint, background, normalize, normalize_time]

PBR = Instrument(id='ncnr.refl.pbr', # creates instrument with module option lists 'Input' and 'Reduction'
                 name='refl',
                 archive='http://www.ncnr/nist.gov/data/pbr',
                 menu=[  # takes 'input' and 'reduction' lists and places both in menu for PBR instrument
                       ('Input', input),
                       ('Reduction', reduction),
                      ],
                 requires=[],
                 datatypes=[data1d],
                 )

instruments = [PBR]
for instrument in instruments:
        register_instrument(instrument) # instrument is registered
