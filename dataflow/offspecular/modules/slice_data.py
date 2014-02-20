"""
Slice the data, according to internally defined mask
"""
import types

from reduction.offspecular import filters

from ... import config
from ...core import Module
try: 
    from collections import OrderedDict
except:
    from ...ordered_dict import OrderedDict

from ..datatypes import OSPEC_DATA

def slice_data_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, xtype=None, filterModule=None):
    """Module for masking 2D data"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'autogrid.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'autogrid_image.png',
        'terminals': { 
            'input': (None, None, -1, 0),
            'output_x': (None, None, 0, 1),
            'output_y': (None, None, 1, 0),
        }
    }
    
    xtype = "SliceContainer"
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='original data',
             required=True,
             multiple=False,
             ),
        dict(id='output_x',
             datatype=datatype,
             use='out',
             description='x data sum',
             direction=[0,1]
             ),
        dict(id='output_y',
             datatype=datatype,
             use='out',
             description='y data sum',
             direction=[1,0]
             )
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
                  name='Slice Data',
                  version=version,
                  description=action.__doc__, 
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  filterModule=filterModule,
                  xtype=xtype
                  )
    module.LABEL_WIDTH = 150
    return module

# Slice module
def slice_action(input=[], xmin="", xmax="", ymin="", ymax="", **kwargs):
    print "slicing"
    output = filters.SliceData().apply(input, xmin, xmax, ymin, ymax)

    if type(input) == types.ListType:
        xslice = []
        yslice = []
        for i in xrange(len(input)):
            xslice.append(output[i][0])
            yslice.append(output[i][1])
    else:
        xslice, yslice = output
    return dict(output_x = xslice, output_y = yslice)
slice_data = slice_data_module(id='ospec.slice', datatype=OSPEC_DATA, version='1.0', action=slice_action, filterModule=filters.SliceData)
