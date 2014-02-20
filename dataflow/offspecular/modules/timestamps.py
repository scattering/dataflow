"""
Get the timestamps from the source file directory listing
and interpolate between the start time and the end time.
"""
from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA, OSPEC_DATA_TIMESTAMP, get_friendly_name

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


def timestamp_action(input=[], stamps=None, override_existing=False, **kwargs):
    print "stamping times"
    if stamps == None:
        raise ValueError("No timestamps specified")
    timestamp_file = stamps[0] # only one timestamp
    return dict(output=[filters.InsertTimestamps().apply(datum, timestamp_file, override_existing=override_existing, filename=get_friendly_name(datum._info[-1]['filename'])) for datum in input])
timestamp = timestamp_module(id='ospec.timestamp', datatype=OSPEC_DATA,
                             version='1.0', action=timestamp_action, stamp_datatype=OSPEC_DATA_TIMESTAMP)
