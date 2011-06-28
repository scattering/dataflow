"""
Return transmission based on bottom left and top right coordinates
"""

from .. import config
from ..core import Module

def generate__transmission_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Return transmission based on bottom left and top right coordinates"""

    icon = {
        'URI': config.IMAGES + "generate__transmission.png",
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
             description='correct',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='generate__transmission',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
