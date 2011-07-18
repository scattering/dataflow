"""
Combine polarized data sets
"""

from ... import config
from ...core import Module

def combine_polarized_module(id=None, datatype=None, action=None,
                version='0.0', fields=[],
                description="Combine multiple polarized datasets"):
    """
    Return a module for combining multiple polarized datasets
    """

    icon = {
        'URI': config.IMAGES + 'sum_polar.png',
        'terminals': {
            'input': (-15, 1, -1, 0),
            'grid': (-10, 1, -1, 0),
            'output': (15, 1, 1, 0),
        }
    }
    
    
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
    
    grid_field = {
        "type":"FilterableMetaArray",
        "label": "grid",
        "name": "grid",
        "value": None,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Combine polarized',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=[grid_field] + fields,
                  action=action,
                  )

    return module
