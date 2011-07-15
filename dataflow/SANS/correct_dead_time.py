"""
Deadtime Correction 
"""

from .. import config
from ..core import Module

def correct_dead_time_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Deadtime corrections - has a parameter"""

    icon = {
        'URI': config.IMAGES + "deadtime.png",
        'terminals': {
            #Inputs
            'Sample': (0, 10, -1, 0),
            'Empty Cell': (0, 20, -1, 0),
            'Empty': (0, 30, -1, 0),
            'Blocked': (0, 40, -1, 0),
            #Outputs
            'Sample': (20, 10, 1, 0),
            'Empty Cell': (20, 20, 1, 0),
            'Empty': (20,30, 1, 0),
            'Blocked': (20, 40, 1, 0),
        }
    }
    
    terminals = [
        dict(id='Sample',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='Empty Cell',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='Empty',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='Blocked',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        
        
        dict(id='Sample',
             datatype='SANS Data',
             use='out',
             description='Dead time',
             ),
        dict(id='Empty Cell',
             datatype='SANS Data',
             use='out',
             description='Dead time',
             ),
        dict(id='Empty',
             datatype='SANS Data',
             use='out',
             description='Dead time',
             ),
        dict(id='Blocked',
             datatype='SANS Data',
             use='out',
             description='Tsam, Temp',
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