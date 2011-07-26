"""
Takes a dataset with a defined polarization state (not None) and
calculates the row of the NT matrix that corresponds to each datapoint
"""

from ... import config
from ...core import Module

def append_polarization_matrix_module(id=None, datatype=None, cell_datatype=None, action=None,
                version='0.0', fields=[],
                description="Append polarization matrix"):
    """
    Return a module for appending polarization matrices
    """

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + 'app_polar_matrix.png',
        'image': config.IMAGES + config.ANDR_FOLDER + 'app_polar_matrix_image.png',
        'terminals': {
            'input': (-12, 4, -1, 0),
            'he3cell': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='Data parts',
             required=True,
             multiple=False,
             ),
        dict(id='he3cell',
             datatype=datatype,
             use='in',
             description='He3 cell',
             required=True,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Data with polarization matrix',
             ),
    ]
    
    he3cell_field = {
        "type":"He3AnalyzerCollection",
        "label": "He3 cell",
        "name": "he3cell",
        "value": None,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Append polarization matrix',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=[he3cell_field] + fields,
                  action=action,
                  )

    return module
