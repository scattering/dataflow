"""
Extracts a given number of runs (TripleAxis objects) 
from a list of loaded TripleAxis objects.
"""

from ... import config
from ...core import Module

from ..datatypes import TAS_DATA

def extract_module(id=None, datatype=None, action=None,
                version='0.0', fields={},
                description="Extract specific datasets", **kwargs):
    """
    Return a module for extracting select TripleAxis objects from data file(s)
    """

    icon = {
        'URI': config.IMAGES + 'TAS/extract.png', 
        'image': config.IMAGES + 'TAS/extract.png',
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
             description='Data parts',
             required=False,
             multiple=True,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Extracted data',
             ),
    ]
    
    fields = {'data_objects': {
            "type": "data_summary",
            "label": "Select the runs to extract",
            "name": "data_objects",
            "value": [],
        }      
    }    
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Extract',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module

def extract_action(input, data_objects=[], **kwargs):
    """ isolates/extracts the given list of objects """
    print "extracting", data_objects

    return dict(output=data_objects)


extract = extract_module(id='tas.extract', datatype=TAS_DATA,
                         version='1.0', action=extract_action, fields=None)
