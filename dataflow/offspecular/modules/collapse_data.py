"""
Collapse the data
"""
import types

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def collapse_data_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, xtype=None, **kwargs):
    """Module for collapsing 2D data to 1D"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'autogrid.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'collapse_image.png',
        'terminals': {
            'input' : (-16, 10, -1, 0),
            'output_x' : (48, 4, 0, 1),
            'output_y': (48, 40, 1, 0),
        }
    }
    
    xtype  = 'AutosizeImageContainer'
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
             ),
        dict(id='output_y',
             datatype=datatype,
             use='out',
             description='y data sum',
             ),
    ]
  

    # qxmin, qxmax, qxbins, qzmin, qzmax, qzbins
    # (-0.003, 0.003, 201, 0, 0.1, 201)
   
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Collapse Data',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype,
                  **kwargs
                  )
    module.LABEL_WIDTH = 80
    return module


# Collapse module
def collapse_action(input=[], **kwargs):
    print "collapsing"
    output = filters.CollapseData().apply(input)

    if type(input) == types.ListType:
        xslice = []
        yslice = []
        for i in xrange(len(input)):
            xslice.append(output[i][0])
            yslice.append(output[i][1])
    else:
        xslice, yslice = output
    return dict(output_x = xslice, output_y = yslice)
collapse_data = collapse_data_module(id='ospec.collapse', datatype=OSPEC_DATA, version='1.0', action=collapse_action,filterModule=filters.CollapseData)

