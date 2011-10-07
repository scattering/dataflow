"""
Load data sets from Asterix.
"""

from ... import config
from ...core import Module

def load_asterix_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for loading an Asterix dataset"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields.extend([
    {
        "type":"[file]",
        "label": "Files",
        "name": "files",
        "value": [],
    },
#    center_pixel_field = {
#        "label": "Center Pixel", 
#        "name": "center_pixel", 
#        "type": "float", 
#        "value": 145.0,        
#    }
#    wl_over_tof_field = {
#        "label": "Wavelength over Time-of-Flight", 
#        "name": "wl_over_tof", 
#        "type": "scientific", 
#        "value": 1.9050372144288577e-5,
#    }    
#    pw_over_d_field = {
#        "label": "Pixel width/distance (to sample)", 
#        "name": "pixel_width_over_dist", 
#        "type": "float", 
#        "value":  0.00034113856493630764,
#    }
    ])
      
    # Combine everything into a module.
    module = Module(id=id,
                  name='LoadAsterix',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
