"""
Module to correct Asterix raw data by spectrum
"""

from ... import config
from ...core import Module

def asterix_correct_spectrum_module(id=None, datatype=None, action=None,
                 version='0.0', fields=[]):
    """Multiplies the monitor counts in the raw data by the spectrum values
    data must be aligned along TOF axis, so this correction should be done
    first."""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "qxqz.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "qxqz_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'output_grid': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='data',
             required=True,
             multiple=False,
             ),
        dict(id='spectrum',
             datatype=datatype,
             use='in',
             description='spectrum',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='monitor multiplied by spectrum',
             ),
    ]

    # Combine everything into a module.
    module = Module(id=id,
                  name='Correct Spectrum',
                  version=version,
                  description=action.__doc__,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  )

    return module
