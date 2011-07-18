"""
Absolute Scaling
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics
def absolute_scaling_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Abs"""

    icon = {
        'URI': config.IMAGES + map_pics('abs'),
        'terminals': {
            #inputs
            'DIV': (0, 10, -1, 0),
            'empty': (0, 10, -1, 0),
            'sensitivity': (0, 10, -1, 0),
            
            'ABS': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='DIV',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='empty',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),     
        dict(id='sensitivity',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        
        
        
        dict(id='ABS',
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