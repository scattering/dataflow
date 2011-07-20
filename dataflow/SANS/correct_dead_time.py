"""
Deadtime Correction 
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics
def correct_dead_time_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Deadtime corrections - has a parameter"""

    icon = {
        'URI': config.IMAGES + map_pics('deadtime'),
        'terminals': {
            #Inputs
            'sample': (0, 10, -1, 0),
            'empty_cell': (0, 20, -1, 0),
            #'empty': (0, 30, -1, 0),
            'blocked': (0, 40, -1, 0),
            #Outputs
            'sample': (20, 10, 1, 0),
            'empty_cell': (20, 20, 1, 0),

            #'empty': (20,30, 1, 0),
           # 'empty': (20,30, 1, 0),
            'blocked': (20, 40, 1, 0),
        }
    }
    
    terminals = [
        dict(id='sample',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='empty_cell',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        #dict(id='empty',
             #datatype=datatype,
             #use='in',
             #description='data',
             #required=False,
             #multiple=True,
             #),
        dict(id='blocked',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        
        
        dict(id='sample',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='empty_cell',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        #dict(id='empty',
             #datatype=datatype,
             #use='out',
             #description='Dead time',
             #),
        dict(id='blocked',
             datatype=datatype,
             use='out',
             description='Dead Time',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Dead time Correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
