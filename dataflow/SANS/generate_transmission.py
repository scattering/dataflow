"""
Return transmission based on bottom left and top right coordinates
"""

from .. import config
from ..core import Module

def generate_transmission_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Return transmission based on bottom left and top right coordinates"""

    icon = {
        'URI': config.IMAGES + "generate_transmission.png",
        'terminals': {
            #inputs
            'sample': (0, 10, -1, 0),
            'empty_cell': (0, 40, -1, 0),
            #'empty': (0, 70, -1, 0),
            'Tsam': (0, 100, -1, 0),
            'Temp': (0, 130, -1, 0),
            
            'sample': (20, 10, 1, 0),
            'empty_cell': (20, 10, 1, 0),
            #'empty': (20, 10, 1, 0),
            'trans': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='sample',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='empty_cell',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        #dict(id='empty',
             #datatype=datatype,
             #use='in',
             #description='data',
             #required=False,
             #multiple=True,
             #),
        dict(id='Tsam',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='Temp',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        
        
        dict(id='sample',
             datatype=datatype,
             use='out',
             description='correct',
             ),
        dict(id='empty_cell',
             datatype=datatype,
             use='out',
             description='correct',
             ),
        #dict(id='empty',
             #datatype=datatype,
             #use='out',
             #description='correct',
             #),
        dict(id='trans',
             datatype=datatype,
             use='out',
             description='correct',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='generate_transmission',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
