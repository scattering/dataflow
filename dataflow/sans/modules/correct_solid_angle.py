"""
Solid Angle Correction 
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def correct_solid_angle_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """(cos(sansdata.theta)**3)"""

    icon = {
        'URI': config.IMAGES + "correct_solid_angle.png",
        'terminals': {
            'input': (0, 10, -1, 0),
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='solid_angle correction',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='correct_solid_angle',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def correct_solid_angle_action(input=None):

    print "input#########: ",input
    result = [red.correct_solid_angle(input[0][0])]
    return dict(output=result)
correct_solid_angle = correct_solid_angle_module(id='sans.correct_solid_angle', datatype=SANS_DATA, version='1.0', action=correct_solid_angle_action, xtype=xtype)
