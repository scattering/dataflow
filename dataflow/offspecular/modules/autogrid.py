"""
Grid data sets
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

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

# Autogrid module
def autogrid_action(input=[], extra_grid_point=True, min_step=1e-10, **kwargs):
    print "gridding"
    return dict(output=[filters.Autogrid().apply(input, extra_grid_point=extra_grid_point, min_step=min_step)])
autogrid = autogrid_module(id='ospec.grid', datatype=OSPEC_DATA,
                           version='1.0', action=autogrid_action)

