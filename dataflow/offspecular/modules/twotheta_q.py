"""
Module to convert two theta to QxQz
"""

from ... import config
from ...core import Module
try: 
    from collections import OrderedDict
except:
    from ...ordered_dict import OrderedDict

def twotheta_q_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, xtype=None, **kwargs):
    """Creates a module for converting twotheta to q"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "qxqz.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "qxqz_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype='AutosizeImageContainer'
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
             description='data in q',
             ),
    ]
    
    fields = OrderedDict(fields)
    fields["wavelength"] = {
            "type":"float",
            "label": "wavelength",
            "name": "wavelength",
            "value": 5.0,
        }
    fields["ax_name"] = {
            "type": "List",
            "label": "Name of twotheta axis",
            "name": "ax_name",
            "value": 'twotheta',
            "choices": ['twotheta', 'twotheta_y']
        }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Twotheta to q',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype,
                  **kwargs
                  )

    return module
