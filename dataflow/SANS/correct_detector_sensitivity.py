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
                  name='Correct Detector Sensitivity',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module