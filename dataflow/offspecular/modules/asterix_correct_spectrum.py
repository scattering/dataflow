"""
Module to correct Asterix raw data by spectrum
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def asterix_correct_spectrum_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, xtype=None, **kwargs):
    """Multiplies the monitor counts in the raw data by the spectrum values
    data must be aligned along TOF axis, so this correction should be done
    first."""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "correct_spectrum_icon.png", 
        'image': config.IMAGES + config.ANDR_FOLDER + "correct_spectrum_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'spectrum': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
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
                  xtype=xtype,
                  **kwargs
                  )

    return module

# Correct spectrum module
def asterix_correct_spectrum_action(input=[], spectrum=[], **kwargs):
    print "correcting spectrum"
    # There should only be one entry into spectrum... more than that doesn't make sense
    # grabbing the first item from the spectrum list:
    return dict(output=filters.AsterixCorrectSpectrum().apply(input, spectrum=spectrum[0]))
asterix_correct_spectrum = asterix_correct_spectrum_module(id='ospec.asterix.corr_spectrum', datatype=OSPEC_DATA,
                                                           version='1.0', action=asterix_correct_spectrum_action)

