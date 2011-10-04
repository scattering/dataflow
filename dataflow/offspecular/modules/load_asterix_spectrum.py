"""
Load spectrum data sets from Asterix.
"""

from ... import config
from ...core import Module

def load_asterix_spectrum_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for loading an Asterix spectrum dataset"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields.extend([
    {
        "type":"[file]",
        "label": "Files",
        "name": "files",
        "value": [],
    },
    ])
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='LoadAsterixSpectrum',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
