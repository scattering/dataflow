"""
Clear part of the data
"""
from reduction.offspecular import filters

from ... import config
from ...core import Module
try:
    from collections import OrderedDict
except:
    from ...ordered_dict import OrderedDict

from ..datatypes import OSPEC_DATA

def mask_data_module(id=None, datatype=None, action=None,
                version='0.0', fields=[], xtype=None, filterModule=None):
    """Module for masking 2D data"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'autogrid.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'mask_image.png',
        'terminals': {
            'input': (None, None, -1, 0),
            'output': (20, 10, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='original data',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='masked data',
             ),
    ]
  

    # qxmin, qxmax, qxbins, qzmin, qzmax, qzbins
    # (-0.003, 0.003, 201, 0, 0.1, 201)
    fields = OrderedDict()
    fields["invert_mask"] = {
        "label": "invert mask (true sets values outside range to zero, false acts on values inside)", 
        "name": "invert_mask", 
        "type": "boolean", 
        "value": False,
    }
    fields["xmin"] = {
        "type":"string",
        "label": "xmin pixel",
        "name": "xmin",
        "value": "0",
    }
    fields["xmax"] = {
        "type":"string",
        "label": "xmax pixel",
        "name": "xmax",
        "value": "",
    }
    fields["ymin"] = {
        "type":"string",
        "label": "ymin pixel",
        "name": "ymin",
        "value": "0",
    }
    fields["ymax"] =  {
        "type":"string",
        "label": "ymax pixel",
        "name": "ymax",
        "value": "",
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Mask Data',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  filterModule=filterModule,
                  xtype=xtype,
                  )
    module.LABEL_WIDTH = 150
    return module


# Mask module
def mask_action(input=[], xmin="0", xmax="", ymin="0", ymax="", invert_mask=False, **kwargs):
    print "masking"
    return dict(output=filters.MaskData().apply(input, xmin, xmax, ymin, ymax, invert_mask))
mask_data = mask_data_module(id='ospec.mask', datatype=OSPEC_DATA, version='1.0', action=mask_action, filterModule=filters.MaskData)
