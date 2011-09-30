"""
Module to convert time of flight to wavelength
"""

from ... import config
from ...core import Module

def shift_data_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Creates a module for shifting a block of 2d data from beginning to end"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "twotheta.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "twotheta_image.png",
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
             description='data with two theta',
             ),
    ]
    
    

    # pixels_per_degree=80.0, qzero_pixel=309, instr_resolution=1e-6
    fields.extend([
        {
          "label": "Edge Bin", 
          "name": "edge_bin", 
          "type": "int", 
          "value": 180,
        },
        {
          "label": "Axis",
          "name": "axis",
          "type": "int",
          "value": 0,
        },
      ])


    # Combine everything into a module.
    module = Module(id=id,
                  name='Shift Data',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
