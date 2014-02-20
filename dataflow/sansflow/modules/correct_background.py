"""
Subtracts the Background from Sample (SAM-BGD)
"""
import reduction.sans.filters as red

from ... import config
from ...core import Module

from ..datatypes import SANS_DATA, xtype

def correct_background_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, **kwargs):
    """SAM-BGD"""

    icon = {
        'URI': config.IMAGES + "correct_background.png",
        'terminals': {
            'input': (16, -16, -1, 0),
            'output': (16, 48, 1, 0),
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
             description='background correction',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='correct_background',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def correct_background_action(input=None, **kwargs):
    result = [red.correct_background(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_background = correct_background_module(id='sans.correct_background',
                                               datatype=SANS_DATA, version='1.0',
                                               action=correct_background_action,
                                               xtype=xtype,
                                               filterModule=red.correct_background)

