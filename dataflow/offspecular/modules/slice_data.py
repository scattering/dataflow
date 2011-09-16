"""
Slice the data
"""

from ... import config
from ...core import Module

def slice_data_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for masking 2D data"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'autogrid.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'autogrid_image.png',
        'terminals': {
            'input' : (-16, 10, -1, 0),
            'output_x' : (48, 4, 1, 0),
            'output_y': (48, 40, 1, 0),
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
        dict(id='output_x',
             datatype=datatype,
             use='out',
             description='x data slice',
             ),
        dict(id='output_y',
             datatype=datatype,
             use='out',
             description='y data slice',
             ),
    ]
  

    # qxmin, qxmax, qxbins, qzmin, qzmax, qzbins
    # (-0.003, 0.003, 201, 0, 0.1, 201)
   
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Slice Data',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )
    module.LABEL_WIDTH = 80
    return module
