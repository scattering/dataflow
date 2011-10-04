"""
Clear part of the data
"""

from ... import config
from ...core import Module

def mask_data_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for masking 2D data"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'autogrid.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'autogrid_image.png',
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
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
    fields.extend([
        {
            "label": "invert mask (true sets values outside range to zero, false acts on values inside)", 
            "name": "invert_mask", 
            "type": "boolean", 
            "value": False,
        },
        {
            "type":"string",
            "label": "xmin pixel",
            "name": "xmin",
            "value": "0",
        },
        {
            "type":"string",
            "label": "xmax pixel",
            "name": "xmax",
            "value": "",
        },
        {
            "type":"string",
            "label": "ymin pixel",
            "name": "ymin",
            "value": "0",
        },
        {
            "type":"string",
            "label": "ymax pixel",
            "name": "ymax",
            "value": "",
        },
    ])
   
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Mask Data',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )
    module.LABEL_WIDTH = 150
    return module
