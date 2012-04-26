"""
Load data sets.
"""

from .. import config
from ..core import Module

def load_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, xtype='WireIt.Container', **kwargs):
    """Module for loading a dataset"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
   
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    files_field = {
        "type":"files",
        "label": "Files",
        "name": "files",
        "value": [],
    }
    intent_field = {
        "type":"string",
        "label":"Intent",
        "name": "intent",
        "value": '',
    }
    
    fields.update({'files': files_field, 'intent': intent_field})
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype,
                  **kwargs
                  )

    return module
