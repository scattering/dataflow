"""
For TripleAxis, monitor correction
"""

from ... import config
from ...core import Module

def monitor_correction_module(id=None, datatype=None, action=None,
                             version='0.0', fields=[],
                             description="apply TripleAxis monitor correction"):
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
    
    instrument_name_field = {
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
                  fields=[instrument_name_field] + fields,
                  action=action,
                  )

    return module
