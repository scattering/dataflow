"""
For TripleAxis, rebin
"""

from ... import config
from ...core import Module

def normalize_monitor_module(id=None, datatype=None, action=None,
                             version='0.0', fields={},
                             description="Rebin TripleAxis data for plotting. ", **kwargs):
    """
    Return a module for rebinning TripleAxis data
    """

    icon = {
        'URI': config.IMAGES + 'TAS/monitor_normalization.png',   #make new icon
        'image': config.IMAGES + 'TAS/monitor_normalization.png', #make new icon
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
             description='TripleAxis object, independent and dependent variables (axes), and (optional) number of bins input',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='TripleAxis object with rebinned fields',
             ),
    ]
    
    fields['independent_variable'] = {
        "type": "float",
        "label": "Independent variable",
        "name": "independent_variable",
        "value": "h",
    }
    fields['dependent_variable'] = {
        "type": "float",
        "label": "Dependent variable",
        "name": "dependent_variable",
        "value": "k",
    }
    fields['bincount'] = {
        "type": "float",
        "label": "Number of bins",
        "name": "bincount",
        "value": 0,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Rebin',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module
