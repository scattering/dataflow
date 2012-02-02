"""
Module to convert pixels to two theta
"""

from ... import config
from ...core import Module

def pixels_two_theta_module(id=None, datatype=None, action=None,
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
        "pixels_per_degree": {
            "type":"float",
            "label": "pixels per degree",
            "name": "pixels_per_degree",
            "value": 80.0,
        },
        "qzero_pixel": {
            "type":"int",
            "label": "qzero pixel",
            "name": "qzero_pixel",
            "value": 309,
        }, 
        "instr_resolution": {
            "type":"float",
            "label": "instrument resolution",
            "name": "instr_resolution",
            "value": 1e-6,
        }
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Pixels to two theta',
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
