"""
Absolute Scaling
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def absolute_scaling_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Abs"""

    icon = {
        'URI': config.IMAGES + "SANS/Abs.png",
	'image': config.IMAGES + 'SANS/abs_image.png',
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
    
    fields['ins_name'] = {
        'type' :'string',
        'label':'Instrument Name (NG3,NG5,or NG7)',
        'name' :'ins_name',
        'value':'',
        }
    fields['bottomLeftCoord'] = {
        'type' :'dict',
        'label':'Bottom Left Coordinate',
        'name' :'bottomLeftCoord',
        'value':{
            'X': {'label': 'X',
                  'type': 'float',
                  'value': 0},
            'Y': {'label': 'Y',
                  'type': 'float',
                  'value': 0}
            }
        }
    fields['topRightCoord'] = {
        'type' :'Object',
        'label':'Top Right Coordinate',
        'name' :'topRightCoord',
        'value':{
            'X': {'label': 'X',
                  'type': 'float',
                  'value': 0},
            'Y': {'label': 'Y',
                  'type': 'float',
                  'value': 0}
            }
        }
    # Combine everything into a module.
    module = Module(id=id,
                  name='Absolute Scaling',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module


def absolute_scaling_action(DIV, empty, sensitivity, ins_name='',
                            bottomLeftCoord={}, topRightCoord={}, **kwargs):
    #sample,empty,DIV,Tsam,instrument
    coord_left = (int(bottomLeftCoord['X']), int(bottomLeftCoord['Y']))
    coord_right = (int(topRightCoord['X']),  int(topRightCoord['Y']))
    DIV, empty, sensitivity = DIV[0], empty[0], sensitivity[0]
    ABS = red.absolute_scaling(DIV, empty, sensitivity, DIV.Tsam, ins_name, coord_left, coord_right)
    return dict(ABS=[ABS])
absolute_scaling = absolute_scaling_module(id='sans.absolute_scaling',
                                   datatype=SANS_DATA, version='1.0',
                                   action=absolute_scaling_action, xtype=xtype,
                                   filterModule=red.absolute_scaling)
