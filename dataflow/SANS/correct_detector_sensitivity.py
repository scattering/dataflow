"""
Correct Detector Sensitivity With .DIV file
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics

def correct_detector_sensitivity_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Uses .DIV to peform division in reduction steps"""

    icon = {
        'URI': config.IMAGES + "SANS/div.png",
	'image': config.IMAGES + "SANS/div_image.png",
        'terminals': {
            #inputs
            'COR': (-16, 10, -1, 0),
            'DIV_in': (-16, 30, -1, 0),
            
            #outputs
            'DIV_out': (48, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='COR',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='DIV_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),        
        
        
        dict(id='DIV_out',
             datatype=datatype,
             use='out',
             description='correct',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Correct Detector Sensitivity',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module
