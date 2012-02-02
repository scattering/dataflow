"""
Combine polarized data sets
"""

from ... import config
from ...core import Module

def combine_polarized_module(id=None, datatype=None, action=None,
                version='0.0', fields={},
                description="Combine multiple polarized datasets", xtype=None):
    """
    Return a module for combining multiple polarized datasets
    """

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'sum_polar.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'sum_polar_image.png',
        'terminals': {
            'input': (-12, 4, -1, 0),
            'grid': (-12, 40, -1, 0),
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
        dict(id='grid',
             datatype=datatype,
             use='in',
             description='Output grid',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Combined data',
             ),
    ]
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Combine polarized',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module
