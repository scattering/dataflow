"""
Module to convert pixels to two theta
"""

from ... import config
from ...core import Module

def pixels_two_theta_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for converting to two theta"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "twotheta.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "twotheta_image.png",
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 1, 0),
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
             description='data with two theta',
             ),
    ]
    
    # pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6
    pixs_per_degree_field = {
        "type":"float",
        "label": "pixels_per_degree",
        "name": "pixels per degree",
        "value": 80.0,
    }
    
    qzero_pixel_field = {
        "type":"int",
        "label": "qzero_pixel",
        "name": "qzero pixel",
        "value": 309,
    }
    
    resolution_field = {
        "type":"float",
        "label": "instr_resolution",
        "name": "instrument resolution",
        "value": 1e-6,
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Pixels to two theta',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[pixs_per_degree_field, qzero_pixel_field, resolution_field] + fields,
                  action=action,
                  )

    return module
