"""
Smooth data along one axis
"""

from ... import config
from ...core import Module

def smooth_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], xtype=None, **kwargs):
    """Module for smoothing data along one axis"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "smooth_icon.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "smooth_image.png",
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
             description='smoothed data',
             ),
    ]

    fields = { 
        "window": {
            "type": "List",
            "label": "Window type",
            "name": "window",
            "value": "flat",
            "choices": ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
        }, 
        "window_len": {
            "type": "float",
            "label": "Smoothing width",
            "name": "window_len",
            "value": 5
        }, 
        "axis": {
            "type": "float",
            "label": "axis to be smoothed (0 or 1)",
            "name": "axis",
            "value": 0
        }
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Smooth',
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
