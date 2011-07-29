"""
For TripleAxis, volume correction
"""

from .. import config
from ..core import Module

def volume_correction_module(id=None, datatype=None, action=None,
                             version='0.0', fields=[],
                             description="apply TripleAxis volume correction"):
    """
    Return a module for correcting TripleAxis volume
    """

    icon = {
        'URI': config.IMAGES + 'TAS/volume_resolution_correction.png',
        'image': config.IMAGES + 'TAS/volume_resolution_correction.png',
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
             description='TripleAxis object with corrected volume',
             ),
    ]
    
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Volume Correction',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
