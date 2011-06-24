"""
Save data sets.
"""

from .. import config
from ..core import Module

def save_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for saving a dataset"""

    icon = {
        'URI': config.IMAGES + "save.png",
        'terminals': {
            'input': (0, 10, -1, 0),
        }
    }
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             multiple=False,
             required=True,
             ),
    ]

    intent_field = {
        "type":"string",
        "label":"Intent",
        "name": "intent",
        "value": '',
    }
    
    save_ext = {
    "type":"[string]",
    "label": "Save extension",
    "name": "ext",
    "value": "",
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Save',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=[intent_field, save_ext] + fields,
                  action=action,
                  )

    return module
