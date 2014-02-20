"""
Module to convert pixels to two theta
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def asterix_pixels_two_theta_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], xtype=None, **kwargs):
    """Creates a module for converting to two theta"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "twotheta.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "twotheta_image.png",
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
    fields = { 
        "pw_over_d": {
            "label": "pixel width over d", 
            "name": "pw_over_d", 
            "type": "float", 
            "value": 0.0003411385649,
        },
    
        "qzero_pixel": {
            "label": "qzero pixel", 
            "name": "qzero_pixel", 
            "type": "float", 
            "value": 145.0,
        },
    
        "twotheta_offset": {
            "label": "twotheta offset", 
            "name": "twotheta_offset", 
            "type": "float", 
            "value": 0.0,
        }
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Asterix Pixels to two theta',
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

def asterix_pixels_two_theta_action(input=[], qzero_pixel = 145., twotheta_offset=0.0, pw_over_d=0.0003411385649, **kwargs):
    print "converting pixels to two theta (Asterix)"
    result = filters.AsterixPixelsToTwotheta().apply(input, pw_over_d=pw_over_d, qzero_pixel=qzero_pixel, twotheta_offset=twotheta_offset)
    return dict(output=result)
asterix_pixels_two_theta = asterix_pixels_two_theta_module(id='ospec.asterix.twotheta', datatype=OSPEC_DATA, version='1.0', action=asterix_pixels_two_theta_action)

