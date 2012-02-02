"""
Grid data sets
"""

from ... import config
from ...core import Module

def autogrid_module(id=None, datatype=None, action=None,
                version='0.0', fields=[],
                description="Autogrid multiple datasets", xtype=None):
    """
    Return a module for that makes a grid to cover all of the data sets
    """

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'autogrid.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'autogrid_image.png',
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
             description='Data parts',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Newly-gridded data',
             ),
    ]
    
    # extra_grid_point=True, min_step=1e-10
    fields = {
        "grid_point": {
            "type":"boolean",
            "label": "extra grid point",
            "name": "extra_grid_point",
            "value": True,
        },
        "step": {
            "type":"float",
            "label": "minimum step",
            "name": "min_step",
            "value": 1e-10,
        }
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Autogrid',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module
