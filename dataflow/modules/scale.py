"""
Scale data sets
"""

from .. import config
from ..core import Module

def scale_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Module for scaling a dataset"""

    icon = {
        'URI': config.IMAGES + "scale.png",
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
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='scaled data',
             ),
    ]

    scale_field = {
        "type":"float",
        "label": "Scale factor",
        "name": "scale",
        "value": 1.0,
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Scale',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[scale_field] + fields,
                  action=action,
                  )

    return module
