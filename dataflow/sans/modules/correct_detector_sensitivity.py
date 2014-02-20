"""
Correct Detector Sensitivity With .DIV file
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def correct_detector_sensitivity_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Uses .DIV to peform division in reduction steps"""

    icon = {
        'URI': config.IMAGES + "SANS/div.png",
	'image': config.IMAGES + "SANS/div_image.png",
        'terminals': {
            #inputs
            'COR': (-16, 10, -1, 0),
            'DIV_in': (-16, 30, -1, 0),
            
            #outputs
            'DIV_out': (48, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='COR',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),
        dict(id='DIV_in',
             datatype=datatype,
             use='in',
             description='data',
             required=False,
             multiple=False,
             ),        
        
        
        dict(id='DIV_out',
             datatype=datatype,
             use='out',
             description='correct',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Correct Detector Sensitivity',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module


def correct_detector_sensitivity_action(COR, DIV_in, **kwargs):
    lis = [COR[0], DIV_in[0]]
    print "####################DIV#############"
    print lis[1]
    CORRECT = lis[0]
    sensitivity = lis[-1]
    DIVV = red.correct_detector_sensitivity(CORRECT, sensitivity)
    DIVV.Tsam = COR[0].Tsam
    result = DIVV
    return dict(DIV_out=[result])
correct_detector_sensitivity = correct_detector_sensitivity_module(
    id='sans.correct_detector_sensitivity', datatype=SANS_DATA, version='1.0',
    action=correct_detector_sensitivity_action, xtype=xtype,
    filterModule=red.correct_detector_sensitivity)

