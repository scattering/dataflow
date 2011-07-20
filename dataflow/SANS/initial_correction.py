"""
Does initial correction
"""

from .. import config
from ..core import Module
from ..SANS.map_pics import map_pics
def initial_correction_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """(SAM-BGD)-[tsam/temp](EMP-BGD)"""

    icon = {
        'URI': config.IMAGES + map_pics('initial'),
        'terminals': {
            #inputs
            'sample': (0, 10, -1, 0),
            'empty_cell': (0, 50, -1, 0),
            'blocked': (0, 90, -1, 0),
            #'trans': (0, 140, -1, 0),
            
            'COR': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='sample',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='empty_cell',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='blocked',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        #dict(id='trans',
             #datatype=datatype,
             #use='in',
             #description='data',
             #required=False,
             #multiple=True,
             #),
        
        
        dict(id='COR',
             datatype=datatype,
             use='out',
             description='correct',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='initial_correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module