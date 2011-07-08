"""
For TripleAxis, normalize monitor
"""

from dataflow import config
from dataflow.core import Module

def normalize_monitor_module(id=None, datatype=None, action=None,
                             version='0.0', fields=[],
                             description="normalize TripleAxis monitor"):
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
    
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Join',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
