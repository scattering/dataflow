"""
Converts to Q
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def convertq_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """Converts to Q"""

    icon = {
        'URI': config.IMAGES + "convertq.png",
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
             description='converted data',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Convertq',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def convertq_action(input=None):
    result = [red.convert_q(input[0][0])]
    return dict(output=result)
convertq = convertq_module(id='sans.convertq', datatype=SANS_DATA, version='1.0', action=convertq_action, xtype=xtype)
