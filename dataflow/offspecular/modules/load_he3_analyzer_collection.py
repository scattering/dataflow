"""
Load an he3 analyzer collection
"""
import os

from reduction.offspecular.he3analyzer import He3AnalyzerCollection

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA_HE3

def load_he3_module(id=None, datatype=None, action=None,
                version='0.0', fields=[], xtype=None):
    """Module for loading an he3 analyzer collection"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "load_he3.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "load_he3_image.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    xtype = "WireIt.Container"
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    fields = {"files": {
        "type":"files",
        "label": "He3 analyzer files",
        "name": "files",
        "value": []
        }
    }
    
    # uses user define types - not acceptable
    #cells_field = {
    #    "type":"list:user",
    #    "label": "Cells",
    #    "name": "cells",
    #    "value": [],
    #}
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Load he3',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module


# Load he3 module
def load_he3_action(files=[], **kwargs):
    print "loading he3", files
    result = [_load_he3_data(f) for f in files]
    return dict(output=result)
def _load_he3_data(name):
    (dirName, fileName) = os.path.split(name)
    return He3AnalyzerCollection(filename=fileName, path=dirName)
load_he3 = load_he3_module(id='ospec.loadhe3', datatype=OSPEC_DATA_HE3,
                           version='1.0', action=load_he3_action)
