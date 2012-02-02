"""
Get the timestamps from the source file directory listing
and interpolate between the start time and the end time.
"""

from ... import config
from ...core import Module

def timestamp_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[], stamp_datatype=None, xtype=None):
    """Module for adding timestamps to a dataset"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "timestamp.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "timestamp_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'stamps': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=True,
             multiple=False,
             ),
        dict(id='stamps',
             datatype=stamp_datatype,
             use='in',
             description='JSON formatted timestamps',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='timestamped data',
             ),
    ]
    
    override_field = {
        "type":"bool",
        "label": "Override existing?",
        "name": "override_existing",
        "value": False,
    }
    
    fields = {"override_existing": override_field}

    # Combine everything into a module.
    module = Module(id=id,
                  name='Timestamp',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module
