"""
Module to convert two theta to QxQz
"""

from ... import config
from ...core import Module

def two_theta_lambda_qxqz_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for converting two theta and lambda to qx and qz"""

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
    
    theta_field = {
        "type":"string",
        "label": "Sample angle (theta)",
        "name": "theta",
        "value": "",
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Two theta lambda to qxqz',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[theta_field] + fields,
                  action=action,
                  )

    return module
