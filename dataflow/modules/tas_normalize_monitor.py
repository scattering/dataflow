"""
For TripleAxis, normalize monitor
"""

from .. import config
from ..core import Module

def normalize_monitor_module(id=None, datatype=None, action=None,
                             version='0.0', fields=[],
                             description="apply TripleAxis monitor normalization"):
    """
    Return a module for normalizing a TripleAxis monitor
    """

    icon = {
        'URI': config.IMAGES + 'sum.png', #GET ICON IMAGE --> replace 'sum.png'
        'terminals': {
            'input': (-15, 1, -1, 0),
            'output': (15, 1, 1, 0),
        }
    }
    
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='TripleAxis object and target monitor input',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='TripleAxis object with normalized monitor',
             ),
    ]
    
    targetmonitor_field = {
        "type":"float",
        "label": "Target monitor",
        "name": "target_monitor",
        "value": 1.0,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Normalize Monitor',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=[targetmonitor_field] + fields,
                  action=action,
                  )

    return module
