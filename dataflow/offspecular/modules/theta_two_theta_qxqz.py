"""
Module to convert two theta to QxQz
"""

from ... import config
from ...core import Module

def theta_two_theta_qxqz_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for converting theta and two theta to qx and qz"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "qxqz.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "qxqz_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'output_grid': (-12, 40, -1, 0),
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
        dict(id='output_grid',
             datatype=datatype,
             use='in',
             description='output grid',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data with qxqz',
             ),
    ]
    
    wavelength_field = {
        "type":"float",
        "label": "wavelength",
        "name": "wavelength",
        "value": 5.0,
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Theta two theta to qxqz',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[wavelength_field] + fields,
                  action=action,
                  )

    return module
