"""
Get the timestamps from the source file directory listing
and interpolate between the start time and the end time.
"""

from ... import config
from ...core import Module

def timestamp_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Module for adding timestamps to a dataset"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "timestamp.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "timestamp_image.png",
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='timestamped data',
             ),
    ]
    
    #timestamp_file='end_times.json', override_existing=False
    filename_field = {
        "type":"string",
        "label": "Filename",
        "name": "timestamp_file",
        "value": 'end_times.json',
    }
    override_field = {
        "type":"bool",
        "label": "Override existing?",
        "name": "override_existing",
        "value": False,
    }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Timestamp',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[filename_field, override_field] + fields,
                  action=action,
                  )

    return module
