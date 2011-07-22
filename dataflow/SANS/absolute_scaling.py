"""
Absolute Scaling
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics
def absolute_scaling_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Abs"""

    icon = {
        'URI': config.IMAGES + "SANS/abs_image.png",
        'terminals': {
            #inputs
            'DIV': (-16, 5, -1, 0),
            'empty': (-16, 25, -1, 0),
            'sensitivity': (-16, 40, -1, 0),
            
            'ABS': (48, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='DIV',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='empty',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),     
        dict(id='sensitivity',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        
        
        
        dict(id='ABS',
             datatype=datatype,
             use='out',
             description='Absolute Scaling',
             ),
    ]
    ins_name_field = {
        'type' :'string',
        'label':'Instrument Name (NG3,NG5,or NG7)',
        'name' :'instrument',
        'value':'',
        }
    # Combine everything into a module.
    module = Module(id=id,
                  name='absolute_scaling',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=[ins_name_field]+fields,
                  action=action,
                  )

    return module