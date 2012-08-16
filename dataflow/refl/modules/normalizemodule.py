"""
Normalize counts column to monitor
"""

from ... import config
from ...core import Module

def normalize_module(id=None, datatype=None, action=None,  # normalize module constructor
                    version='0.0', fields=[], xtype=None, filterModule=None, **kwargs):
    """Module for normalizing counts to monitor"""
    
    icon = {  # how the module will look
        'URI': config.IMAGES + config.ANDR_FOLDER + 'normalize_icon.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'normalize_image.png',
        'terminals': {
            'input': (None, None, -1, 0),
            'output': (None, None, 1, 0)
        }
    }
    
    terminals = [  # terminals for the wires
        dict(id='input',
            datatype=datatype,
            use='in',
            description='original data',
            required=True,
            multiple=False,
            ),
        dict(id='output',
            datatype=datatype,
            use='out',
            description='normalized data'
            )
    ]
    
    # no fields needed because NormalizeToMonitor function does not require any arguments
    
    module = Module(id=id,  # creates NormalizeToMonitor module
                    name='Normalize to Monitor',
                    version=version,
                    description=action.__doc__,
                    icon=icon,
                    terminals=terminals,
                    fields=fields,
                    action=action,
                    xtype=xtype,
                    filterModule=filterModule,
                    **kwargs
                    )
    module.LABEL_WIDTH = 80
    return module
