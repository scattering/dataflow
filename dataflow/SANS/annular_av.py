"""
Make 1D Data through Annular Average
"""

from .. import config
from ..core import Module

def annular_av_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Using Annular averaging, make 1D sans data (Q vs I)"""

    icon = {
        'URI': config.IMAGES + "annular_av.png",
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
             description='1D Average',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='annular_av',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module