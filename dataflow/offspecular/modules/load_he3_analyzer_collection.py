"""
Load an he3 analyzer collection
"""

from ... import config
from ...core import Module

def load_he3_module(id=None, datatype=None, action=None,
                version='0.0', fields=[], xtype=None):
    """Module for loading an he3 analyzer collection"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "load_he3.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "load_he3_image.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    xtype = "WireIt.Container"
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields = {"files": {
        "type":"[file]",
        "label": "Files",
        "name": "files",
        "value": []
        }
    }
    
    # uses user define types - not acceptable
    #cells_field = {
    #    "type":"list:user",
    #    "label": "Cells",
    #    "name": "cells",
    #    "value": [],
    #}
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load he3',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module
