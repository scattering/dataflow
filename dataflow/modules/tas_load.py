"""
Load a TripleAxis object from a datafile.
"""

from .. import config
from ..core import Module

def load_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for loading a TripleAxis object"""

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
             description='TripleAxis Object',
             ),
    ]

    files_field = {
        "type":"[file]",
        "label": "Files",
        "name": "files",
        "value": '',
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=[files_field] + fields,
                  action=action,
                  )

    return module
