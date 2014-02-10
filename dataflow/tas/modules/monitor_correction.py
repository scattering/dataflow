"""
For TripleAxis, monitor correction
"""

from reduction.tas import data_abstraction

from ... import config
from ...core import Module

from ..datatypes import TAS_DATA, xtype

def monitor_correction_module(id=None, datatype=None, action=None,
                             version='0.0', fields={},
                             description="apply TripleAxis monitor correction", **kwargs):
    """
    Return a module for correcting a TripleAxis monitor
    """

    icon = {
        'URI': config.IMAGES + 'TAS/harmonic_monitor_correction.png',
        'image': config.IMAGES + 'TAS/harmonic_monitor_correction.png',
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
             description='TripleAxis object and instrument name',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='TripleAxis object with corrected monitor',
             ),
    ]
    
    fields['instrument_name'] = {
        "type":"string",
        "label": "Instrument name",
        "name": "instrument_name",
        "value": 'BT7',
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Monitor Correction',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module


def monitor_correction_action(input, instrument_name, **kwargs):
    #Requires instrument name, e.g. 'BT7'.
    #Check monitor_correction_coordinates.txt for available instruments
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.harmonic_monitor_correction(instrument_name)
    return dict(ouput=input)


monitor_correction = monitor_correction_module(id='tas.monitor_correction', datatype=TAS_DATA,
                                               version='1.0', action=monitor_correction_action, xtype=xtype,
                                               filterModule=data_abstraction.TripleAxis.harmonic_monitor_correction)
