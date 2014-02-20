"""
Does initial correction
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def initial_correction_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """(SAM-BGD)-[tsam/temp](EMP-BGD)"""

    icon = {
        'URI': config.IMAGES + "SANS/initial_image.png",
	'image': config.IMAGES + "SANS/initial_correction_image.png",
        'terminals': {
            #inputs
            'sample': (-16, 8, -1, 0),
            'empty_cell': (-16, 28, -1, 0),
            'blocked': (-16, 48, -1, 0),
            #'trans': (0, 140, -1, 0),
            
            'COR': (48, 10, 1, 0),
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
                  name='Initial Correction',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module


def initial_correction_action(sample, empty_cell, blocked, **kwargs):
    print type(sample)
    SAM,EMP,BGD = sample[0], empty_cell[0], blocked[0]
    CORR = red.initial_correction(SAM, BGD, EMP, SAM.Tsam / SAM.Temp)
    CORR.Tsam = SAM.Tsam
    result = CORR
    return dict(COR=[result])
initial_correction = initial_correction_module(id='sans.initial_correction',
                                         datatype=SANS_DATA, version='1.0',
                                         action=initial_correction_action,
                                         xtype=xtype,
                                         filterModule=red.initial_correction)


