"""
Module to convert pixels to two theta
"""

from .. import config
from ..core import Module

def pixels_two_theta_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for converting to two theta"""

    icon = {
        'URI': config.IMAGES + "twotheta.png",
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

    # Combine everything into a module.
    module = Module(id=id,
                  name='Pixels to two theta',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
