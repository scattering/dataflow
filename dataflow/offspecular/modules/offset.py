"""
Shift data sets
"""
from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def offset_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], xtype=None):
    """Module for shifting a dataset"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "offset.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "offset_image.png",
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='shifted data',
             ),
    ]

    fields = { 
        "offsets": {
            "type":"Object", # maps a name to the offset
            "label": "Offset amount",
            "name": "offsets",
            "value": {'axis_name': {
                    "type": "string",
                    "label": "Axis name", 
                    "value": ""
                }, 
                "offset": { 
                    "type": "float",
                    "label": "offset",
                    "value": 0.0
                }
            }
        }
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Offset',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module

# Offset module
def offset_action(input=[], offsets={}, **kwargs):
    print "offsetting"
    offsets_dict = {offsets['axis_name']['value'] : offsets['offset']['value']}
    return dict(output=filters.CoordinateOffset().apply(input, offsets=offsets_dict))
offset = offset_module(id='ospec.offset', datatype=OSPEC_DATA, version='1.0', action=offset_action)
