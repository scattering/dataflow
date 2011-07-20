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
        'URI': config.IMAGES + "SANS/deadtime.png",
        'terminals': {
            #Inputs
            'sample_in': (0, 10, -1, 0),
            'empty_cell_in': (0, 20, -1, 0),
            'empty_in': (0, 30, -1, 0),
            'blocked_in': (0, 40, -1, 0),
            #Outputs

            'sample_out': (20, 10, 1, 0),
            'empty_cell_out': (20, 20, 1, 0),
            'empty_out': (20,30, 1, 0),
            'blocked_out': (20, 40, 1, 0),

        }
    }
    
    terminals = [
        dict(id='sample_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='empty_cell_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='empty_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='blocked_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        
        
        dict(id='sample_out',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='empty_cell_out',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='empty_out',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='blocked_out',
             datatype=datatype,
             use='out',
             description='Dead Time',
             ),
    ]
    deadtime_cons_field = {
        'type' :'float',
        'label':'Deadtime Constant (default=3.4e-6)',
        'name' :'deadtime',
        'value':3.4e-6,
        }
    # Combine everything into a module.
    module = Module(id=id,
                  name='Dead time Correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[deadtime_cons_field]+fields,
                  action=action,
                  )

    return module
