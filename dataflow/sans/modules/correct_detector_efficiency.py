"""
Correct Detector Efficiency With .DIV file
"""

import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def correct_detector_efficiency_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Uses .DIV to peform division in reduction steps"""

    icon = {
        'URI': config.IMAGES + "correct_detector_efficiency.png",
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
             description='correct',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='correct_detector_efficiency',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def correct_detector_efficiency_action(input=None):
    print "input: ",input
    sensitivity = red.read_div('div')
    DIV = red.correct_detector_efficiency(input[0][0])
    result = [DIV]
    return dict(output=result)
correct_detector_efficiency = correct_detector_efficiency_module(id='sans.correct_detector_efficiency', datatype=SANS_DATA, version='1.0', action=correct_detector_efficiency_action, xtype=xtype)
