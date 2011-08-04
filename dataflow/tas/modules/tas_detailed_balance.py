"""
For TripleAxis, detailed balance
"""

from ... import config
from ...core import Module

def detailed_balance_module(id=None, datatype=None, action=None,
                             version='0.0', fields=[],
                             description="apply TripleAxis detailed balance"):
    """
    Return a module for performing a detailed balance on a TripleAxis object
    """

    icon = {
        'URI': config.IMAGES + 'TAS/detailed_balance.png', 
        'image': config.IMAGES + 'TAS/detailed_balance.png',
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
             description='TripleAxis object',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='TripleAxis object after detailed balance',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Detailed Balance',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
