"""
Correct polarization
"""

from ... import config
from ...core import Module

def polarization_correct_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], xtype=None):
    """Module for correcting polarization"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "polar_correct.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "polar_correct_image.png",
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='corrected data',
             ),
    ]
    fields = {
        "assumptions": {
            "type":"int",
            "label": "Polarization assumptions",
            "name": "assumptions",
            "value": 0,
        },
        "auto_assumptions": {
            "type":"bool", # maps a name to the offset
            "label": "Auto assumptions",
            "name": "auto_assumptions",
            "value": True,
        }
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Polarization correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module
