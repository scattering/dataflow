"""
For TripleAxis, subtract
"""

from ... import config
from ...core import Module

def subtract_module(id=None, datatype=None, action=None,
                             version='0.0', fields={},
                             description="subtract a TripleAxis's detectors from another TripleAxis's detectors", **kwargs):
    """
    Return a module for normalizing a TripleAxis monitor
    """

    icon = {
        'URI': config.IMAGES + 'TAS/subtract.png', 
        'image': config.IMAGES + 'TAS/subtract.png',
        'width': 'auto', 
        'terminals': {
            'signal': (-12, 14, -1, 0),
            'background': (-12, 18, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    
    terminals = [
        dict(id='signal',
             datatype=datatype,
             use='in',
             description="TripleAxis object after subtracting another TripleAxis's detector counts",
             required=True,
             multiple=False,
             ),
        dict(id='background',
             datatype=datatype,
             use='in',
             description="TripleAxis object after subtracting another TripleAxis's detector counts",
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description="TripleAxis object after subtracting another TripleAxis's detector counts",
             ),
    ]
    
    fields['scan_variable'] = {
        "type": "string",
        "label": "Independent (scan) variable to subract across",
        "name": "scan_variable",
        "value": None,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Subtract',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module
