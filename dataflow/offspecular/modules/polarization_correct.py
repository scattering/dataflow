"""
Correct polarization
"""

from ... import config
from ...core import Module

def polarization_correct_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Module for correcting polarization"""

    icon = {
        'URI': config.IMAGES + "polar_correct.png",
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
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='corrected data',
             ),
    ]

    assumptions_field = {
        "type":"int",
        "label": "Polarization assumptions",
        "name": "assumptions",
        "value": 0,
    }
    
    auto_assumptions_field = {
        "type":"bool", # maps a name to the offset
        "label": "Auto assumptions",
        "name": "auto_assumptions",
        "value": True,
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Polarization correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[assumptions_field, auto_assumptions_field] + fields,
                  action=action,
                  )

    return module
