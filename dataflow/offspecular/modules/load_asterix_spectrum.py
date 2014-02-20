"""
Load spectrum data sets from Asterix.
"""
import os

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def load_asterix_spectrum_module(id=None, datatype=None, action=None,
                version='0.0', fields=[], xtype=None):
    """Module for loading an Asterix spectrum dataset"""

    icon = {
        'URI': config.IMAGES + "load.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    xtype = 'WireIt.Container'
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields = {"files": {
        "type":"files",
        "label": "Spectrum Files",
        "name": "files",
        "value": [],
        }
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='LoadAsterixSpectrum',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module

def load_asterix_spectrum_action(files=[], **kwargs):
    filename = files[0]
    (dirName, fileName) = os.path.split(filename)
    return dict(output=[filters.LoadAsterixSpectrum(filename, path=dirName)])
load_asterix_spectrum = load_asterix_spectrum_module(id='ospec.asterix.load_spectrum', datatype=OSPEC_DATA,
                                                     version='1.0', action=load_asterix_spectrum_action)

