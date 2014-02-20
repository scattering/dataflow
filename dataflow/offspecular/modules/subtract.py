"""
Subtract data sets
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def subtract_module(id=None, datatype=None, action=None,
                version='0.0', fields=[],
                description="Combine multiple datasets", xtype=None):
    """
    Return a module for combining multiple datasets
    """

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'diff.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'diff_image.png',
        'terminals': {
            'minuend': (-12, 4, -1, 0),
            'subtrahend': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    terminals = [
        dict(id='minuend',
             datatype=datatype,
             use='in',
             description='a in a-b',
             required=True,
             multiple=False,
             ),
        dict(id='subtrahend',
             datatype=datatype,
             use='in',
             description='b in a-b',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='a-b',
             ),
    ]
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Subtract',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module

# Subtract module
def subtract_action(minuend=[], subtrahend=None, **kwargs):
    print "subtracting"
    return dict(output=filters.Subtract().apply(minuend, subtrahend))
subtract = subtract_module(id='ospec.subtract', datatype=OSPEC_DATA, version='1.0', action=subtract_action)
