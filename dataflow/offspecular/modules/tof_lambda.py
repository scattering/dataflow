"""
Module to convert time of flight to wavelength
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def tof_lambda_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], xtype=None, **kwargs):
    """Creates a module for converting TOF to wavelength"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "tof_lambda_icon.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "tof_lambda_image.png",
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
             description='data with two theta',
             ),
    ]
    
    

    # pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6
    fields = {"wl_over_tof": 
        {
            "label": "Wavelength over Time-of-Flight", 
            "name": "wl_over_tof", 
            "type": "float", 
            "value": 1.9050372144288577e-5,
        },
    }


    # Combine everything into a module.
    module = Module(id=id,
                  name='TOF to Wavelength',
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

# Time of Flight to wavelength module
def tof_lambda_action(input=[], wl_over_tof=1.9050372144288577e-5, **kwargs):
    print "TOF to wavelength"
    return dict(output=filters.AsterixTOFToWavelength().apply(input, wl_over_tof=wl_over_tof))
tof_lambda = tof_lambda_module(id='ospec.tof_lambda', datatype=OSPEC_DATA, version='1.0', action=tof_lambda_action, filterModule=filters.AsterixTOFToWavelength)
