"""
Normalize counts column to monitor
"""

from ... import config
from ...core import Module

def normalize_module(id=None, datatype=None, action=None,
                    version='0.0', fields=[], xtype=None, filterModule=None, **kwargs):
    """Module for normalizing counts to monitor"""
    
    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'normalize_icon.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'normalize_image.png',
        'terminals': {
            'input': (None, None, -1, 0),
            'output': (None, None, 1, 0)
        }
    }
    
    terminals = [
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
    
    module = Module(id=id,
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
