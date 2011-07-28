"""
For TripleAxis, monitor correction
"""

from .. import config
from ..core import Module

def monitor_correction_module(id=None, datatype=None, action=None,
                             version='0.0', fields=[],
                             description="apply TripleAxis monitor correction"):
    """
    Return a module for correcting a TripleAxis monitor
    """

    icon = {
        'URI': config.IMAGES + 'sum.png', #GET ICON IMAGE --> replace 'sum.png'
        'terminals': {
            'input': (-15, 1, -1, 0),
            'output': (15, 1, 1, 0),
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
    
    instrumentname_field = {
        "type":"String",
        "label": "Instrument name",
        "name": "instrument_name",
        "value": 1.0,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Monitor Correction',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=[instrumentname_field] + fields,
                  action=action,
                  )

    return module
