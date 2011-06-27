"""
Module to convert two theta to QxQz
"""

from .. import config
from ..core import Module

def two_theta_qxqz_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for converting to Qx and Qz"""

    icon = {
        'URI': config.IMAGES + "qxqz.png",
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
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='scaled data',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Two theta to qxqz',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
