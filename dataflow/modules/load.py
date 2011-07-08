"""
Load data sets.
"""

from dataflow import config
from dataflow.core import Module

def load_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for loading a dataset"""

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

    files_field = {
        "type":"[file]",
        "label": "Files",
        "name": "files",
        "value": '',
    }
    intent_field = {
        "type":"string",
        "label":"Intent",
        "name": "intent",
        "value": '',
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=[files_field, intent_field] + fields,
                  action=action,
                  )

    return module
