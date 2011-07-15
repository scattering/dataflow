"""
Module to convert two theta to QxQz
"""

from ... import config
from ...core import Module

def two_theta_qxqz_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for converting theta and two theta to qx and qz"""

    icon = {
        'URI': config.IMAGES + "qxqz.png",
        'terminals': {
            'input': (0, 10, -1, 0),
            'output_grid': (10, 10, -1, 0),
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

    # output_grid=None, wavelength=5.0
    output_grid_field = {
        "type":"MetaArray",
        "label": "output_grid",
        "name": "output grid",
        "value": None,
    }
    
    wavelength_field = {
        "type":"float",
        "label": "wavelength",
        "name": "wavelength",
        "value": 5.0,
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Two theta to qxqz',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[output_grid_field, wavelength_field] + fields,
                  action=action,
                  )

    return module
