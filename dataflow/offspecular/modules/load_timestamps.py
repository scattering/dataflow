"""
Load a timestamp file (strictly just a json object)
"""

from ... import config
from ...core import Module

def load_timestamp_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, xtype=None):
    """Module for loading a timestamp file"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "load_timestamp.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "load_timestamp_image.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    xtype = 'WireIt.Container'
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields['files'] = {
        "type":"files",
        "label": "Timestamp files",
        "name": "files",
        "value": [],
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load stamps',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module
