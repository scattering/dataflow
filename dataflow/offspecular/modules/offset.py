"""
Shift data sets
"""

from ... import config
from ...core import Module

def offset_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Module for shifting a dataset"""

    icon = {
        'URI': config.IMAGES + "offset.png",
        'terminals': {
            'input': (0, 10, -1, 0),
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='shifted data',
             ),
    ]

    offset_field = {
        "type":"dict", # maps a name to the offset
        "label": "Offset amount",
        "name": "offsets",
        "value": {},
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Offset',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[offset_field] + fields,
                  action=action,
                  )

    return module
