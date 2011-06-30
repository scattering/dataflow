"""
Convert qx and qy, so that they can be plotted in javascript
"""

from .. import config
from ..core import Module

def convert_qxqy_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Convert qx and qy for javascript plotting"""

    icon = {
        'URI': config.IMAGES + "convert_qxqy.png",
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
                  name='convert_qxqy',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module