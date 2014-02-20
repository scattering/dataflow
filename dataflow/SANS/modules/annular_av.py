"""
Make 1D Data through Annular Average
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def annular_av_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Using Annular averaging, make 1D sans data (Q vs I)"""

    icon = {
        'URI': config.IMAGES + "SANS/circular_avg_image.png",
	'image': config.IMAGES + "SANS/circular_avg.png", 
        'terminals': {
            #inputs
            'ABS': (-16, 10, -1, 0),
            
            #Outputs
            'OneD': (48, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='ABS',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        
        
        dict(id='OneD',
             datatype=datatype,
             use='out',
             description='1D Average',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Circular Average',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module


def annular_av_action(ABS, **kwargs):
    correct = red.convert_q(ABS[0])
    AVG = red.annular_av(correct)
    result = [AVG]
    print "Done Red"
    return dict(OneD=result)
annular_av = annular_av_module(id='sans.annular_av', datatype=SANS_DATA,
                             version='1.0', action=annular_av_action,
                             xtype=xtype, filterModule=red.annular_av)

