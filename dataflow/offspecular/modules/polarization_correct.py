"""
Correct polarization
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def polarization_correct_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], xtype=None, **kwargs):
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
            "type":"float",
            "label": "Polarization assumptions",
            "name": "assumptions",
            "value": 0,
        },
        "auto_assumptions": {
            "type":"boolean", # maps a name to the offset
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
                  xtype=xtype,
                  **kwargs
                  )

    return module

# Polarization correction module
def polarization_correct_action(input=[], assumptions=0, auto_assumptions=True, **kwargs):
    print "polarization correction"
    return dict(output=filters.PolarizationCorrect().apply(input, assumptions=assumptions, auto_assumptions=auto_assumptions))
polarization_correct = polarization_correct_module(id='ospec.corr_polar', datatype=OSPEC_DATA,
                                                version='1.0', action=polarization_correct_action)
