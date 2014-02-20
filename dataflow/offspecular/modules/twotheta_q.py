"""
Module to convert two theta to QxQz
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module
try: 
    from collections import OrderedDict
except:
    from ...ordered_dict import OrderedDict

from ..datatypes import OSPEC_DATA

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


# Twotheta to q module
def twotheta_q_action(input=[], wavelength=5.0, ax_name='twotheta', **kwargs):
    print "converting twotheta to q"
    result = filters.TwothetaToQ().apply(input, wavelength, ax_name)
    return dict(output=result)
twotheta_q = twotheta_q_module(id='ospec.tth_q', datatype=OSPEC_DATA, version='1.0', action=twotheta_q_action)
