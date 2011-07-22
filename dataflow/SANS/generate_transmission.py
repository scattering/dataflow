"""
Return transmission based on bottom left and top right coordinates
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics
def generate_transmission_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Return transmission based on bottom left and top right coordinates"""

    icon = {
        'URI': config.IMAGES + "SANS/gen_trans_image.png",
        'terminals': {
            #inputs
            'sample_in': (-16, 5, -1, 0),
            'empty_cell_in': (-16, 15, -1, 0),
            'empty_in': (-16, 25, -1, 0),
            'Tsam_in': (-16, 35, -1, 0),
            'Temp_in': (-16, 45, -1, 0),
            
            'sample_out': (48, 10, 1, 0),
            'empty_cell_out': (48, 30, 1, 0),
            #'empty_out': (20, 10, 1, 0),
            #'trans': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='sample_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='empty_cell_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='empty_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='Tsam_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='Temp_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        
        
        dict(id='sample_out',
             datatype=datatype,
             use='out',
             description='correct',
             ),
        dict(id='empty_cell_out',
             datatype=datatype,
             use='out',
             description='correct',
             ),
        #dict(id='empty_out',
             #datatype=datatype,
             #use='out',
             #description='correct',
             #),
        #dict(id='trans',
             #datatype=datatype,
             #use='out',
             #description='correct',
             #),
    ]
    monitorNormalize_field ={
        'type' :'float',
        'label':'Monitor Normalization Value (default=1e8)',
        'name' :'mon0',
        'value':1e8,
        
        }
    bottomLeftCord_field = {
        'type' :'dict',
        'label':'Bottom Left Coordinate',
        'name' :'coords_bottom_left',
        'value':{},
        }
    topRightCord_field = {
        'type' :'dict',
        'label':'Top Right Coordinate',
        'name' :'coords_upper_right',
        'value':{},
        }
    # Combine everything into a module.
    module = Module(id=id,
                  name='generate_transmission',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[monitorNormalize_field,bottomLeftCord_field,topRightCord_field]+fields,
                  action=action,
                  )

    return module
