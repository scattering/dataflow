"""
Deadtime Correction 
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module
from ..datatypes import SANS_DATA, xtype

def correct_dead_time_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Deadtime corrections - has a parameter"""

    icon = {
        'URI': config.IMAGES + "SANS/deadtime_image.png",
	'image': config.IMAGES + "SANS/deadtime.png",
        'terminals': {
            #Inputs
            'sample_in': (-16, 10, -1, 0),
            'empty_cell_in': (-16, 20, -1, 0),
            'empty_in': (-16, 30, -1, 0),
            'blocked_in': (-16, 40, -1, 0),
            #Outputs

            'sample_out': (48, 10, 1, 0),
            'empty_cell_out': (48, 20, 1, 0),
            'empty_out': (48,30, 1, 0),
            'blocked_out': (48, 40, 1, 0),

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
        dict(id='blocked_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        
        
        dict(id='sample_out',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='empty_cell_out',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='empty_out',
             datatype=datatype,
             use='out',
             description='Dead time',
             ),
        dict(id='blocked_out',
             datatype=datatype,
             use='out',
             description='Dead Time',
             ),
    ]
    fields['deadtimeConstant'] = {
        'type' :'float',
        'label':'Deadtime Constant (default=3.4e-6)',
        'name' :'deadtimeConstant',
        'value':3.4e-6,
        }
    # Combine everything into a module.
    module = Module(id=id,
                  name='Dead time Correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def correct_dead_time_action(sample_in, empty_cell_in, empty_in, blocked_in,
                             deadtimeConstant=3.4e-6, **kwargs):
    deadtimeConstant = float(deadtimeConstant)
    lis = [sample_in[0], empty_cell_in[0], empty_in[0], blocked_in[0]]
    print "List: ", lis
    #Enter DeadTime parameter eventually
    solidangle = [red.correct_solid_angle(f) for f in lis]
    det_eff = [red.correct_detector_efficiency(f) for f in solidangle]
    deadtime = [red.correct_dead_time(f, deadtimeConstant) for f in det_eff]
    result = deadtime
    return dict(sample_out=[result[0]], empty_cell_out=[result[1]],
                empty_out=[result[2]], blocked_out=[result[3]])


correct_dead_time = correct_dead_time_module(id='sans.correct_dead_time',
                                    datatype=SANS_DATA, version='1.0',
                                    action=correct_dead_time_action,
                                    xtype=xtype)
