"""
Correct Detector Sensitivity With .DIV file
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics
def correct_detector_sensitivity_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Uses .DIV to peform division in reduction steps"""

    icon = {
        'URI': config.IMAGES + map_pics('div'),
        'terminals': {
            #inputs
            'COR': (0, 10, -1, 0),
            'DIV': (0, 20, -1, 0),
            
            'DIV': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='COR',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='DIV',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),        
        
        
        dict(id='DIV',
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
                  )

    return module