"""
Join data sets
"""

from ... import config
from ...core import Module

def join_module(id=None, datatype=None, action=None,
                version='0.0', fields={},
                description="Combine multiple datasets", **kwargs):
    """
    Return a module for combining multiple datasets
    """

    icon = {
        'URI': config.IMAGES + 'TAS/join.png',
        'image': config.IMAGES + 'TAS/join.png',
        'width': 'auto', 
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='Data parts',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Combined data',
             ),
    ]
    
    fields = {'xaxis': {
        "type":"string",
        "label": "X axis for 2D plotting",
        "name": "xaxis",
        "value": '',
        }, 
        'yaxis': {
            "type":"string",
            "label": "Y axis for 2D plotting",
            "name": "yaxis",
            "value": '',
        },
        'num_bins': {
            "type": "float",
            "label": "Number of bins (optional)",
            "name": "num_bins",
            "value": 0.0,
        },
        'xstep': {
            "type": "float",
            "label": "X bin spacing/step (optional)",
            "name": "xstep",
            "value": None,
        },
        'ystep': {
            "type": "float",
            "label": "Y bin spacing/step (optional)",
            "name": "ystep",
            "value": None,
        }        
    }    
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Join',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module
