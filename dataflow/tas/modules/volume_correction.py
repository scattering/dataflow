"""
For TripleAxis, volume correction
"""

from reduction.tas import data_abstraction

from ... import config
from ...core import Module

from ..datatypes import TAS_DATA, xtype

def volume_correction_module(id=None, datatype=None, action=None,
                             version='0.0', fields={},
                             description="apply TripleAxis volume correction", **kwargs):
    """
    Return a module for correcting TripleAxis volume
    """

    icon = {
        'URI': config.IMAGES + 'TAS/volume_resolution_correction.png',
        'image': config.IMAGES + 'TAS/volume_resolution_correction.png',
        'width': 'auto', 
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='TripleAxis object',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='TripleAxis object with corrected volume',
             ),
    ]
    
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Volume Correction',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module


def volume_correction_action(input, **kwargs):
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.resolution_volume_correction()
    return dict(output=input)



volume_correction = volume_correction_module(id='tas.volume_correction', datatype=TAS_DATA,
                                            version='1.0', action=volume_correction_action, xtype=xtype,
                                            filterModule=data_abstraction.TripleAxis.resolution_volume_correction)

