"""
Load Chalk River TripleAxis data sets.
"""

from ... import config
from ...core import Module

def load_chalk_module(id=None, datatype=None, action=None,
                version='0.0', fields={}, xtype='WireIt.Container', **kwargs):
    """Module for loading a dataset for Chalk River: .aof and .acf files"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }

    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields = { 'chalk_files': {
            "type": "files",
            "label": "Add your .AOF file and corresponding .ACF file and/or .LOG file.",
            "name": "chalk_files",
            "value": [],
        },
        'h1': {
            "type": "float",
            "label":"orient1 h",
            "name": "h1",
            "value": None,
        },
        'k1': {
            "type": "float",
            "label":"orient1 k",
            "name": "k1",
            "value": None,
        },
        'l1': {
            "type": "float",
            "label":"orient1 l",
            "name": "l1",
            "value": None,
        },
        'h2': {
            "type": "float",
            "label":"orient2 h",
            "name": "h2",
            "value": None,
        },
        'k2': {
            "type": "float",
            "label":"orient2 k",
            "name": "k2",
            "value": None,
        },
        'l2': {
            "type": "float",
            "label":"orient2 l",
            "name": "l2",
            "value": None,
        }
    }
    
   
    # Combine everything into a module.
    module = Module(id=id,
                  name='Chalk River Load',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype,
                  **kwargs
                  )

    return module
