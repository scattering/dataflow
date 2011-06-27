"""
Normalize Monitors (not blocked beam file)
"""

from .. import config
from ..core import Module

def monitor_normalize_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Normalize Monitors"""

    icon = {
        'URI': config.IMAGES + "monitor_normalize.png",
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
             description='monitor normalized',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='monitor_normalize',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module

