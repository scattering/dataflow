"""
Absolute Scaling
"""

from .. import config
from ..core import Module

def absolute_scaling_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Abs"""

    icon = {
        'URI': config.IMAGES + "absolute_scaling.png",
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
             description='Absolute Scaling',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='absolute_scaling',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module