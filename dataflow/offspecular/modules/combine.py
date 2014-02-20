"""
Combine data sets
"""
from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def combine_module(id=None, datatype=None, action=None,
                version='0.0', fields={},
                description="Combine multiple datasets", xtype='WireIt.ImageContainer'):
    """
    Return a module for combining multiple datasets
    """

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'sum.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'sum_image.png',
        'terminals': {
            'input_data': (-12, 4, -1, 0),
            'input_grid': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    
    terminals = [
        dict(id='input_data',
             datatype=datatype,
             use='in',
             description='Data parts',
             required=True,
             multiple=False,
             ),
        dict(id='input_grid',
             datatype=datatype,
             use='in',
             description='Output grid',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Combined data',
             ),
    ]
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Combine',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module


# Combine module
def combine_action(input_data=[], input_grid=None, **kwargs):
    print "joining"
    output_grid = None
    if input_grid != None:
        output_grid = input_grid[0]
    return dict(output=[filters.Combine().apply(input_data, grid=output_grid)])
combine = combine_module(id='ospec.combine', datatype=OSPEC_DATA, version='1.0', action=combine_action)

