"""
Make 1D Data through Annular Average
"""

from .. import config
from ..core import Module

def annular_av_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Using Annular averaging, make 1D sans data (Q vs I)"""

    icon = {
        'URI': config.IMAGES + "SANS/circular_avg_image.png",
	'image': config.IMAGES + "SANS/circular_avg.png", 
        'terminals': {
            #inputs
            'ABS': (-16, 10, -1, 0),
            
            #Outputs
            'OneD': (48, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='ABS',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        
        
        dict(id='OneD',
             datatype=datatype,
             use='out',
             description='1D Average',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Circular Average',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module
