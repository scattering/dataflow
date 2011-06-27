"""
Subtracts the Background from Sample (SAM-BGD)
"""

from .. import config
from ..core import Module

def correct_background_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """SAM-BGD"""

    icon = {
        'URI': config.IMAGES + "correct_background.png",
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
             description='background correction',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='correct_background',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module

