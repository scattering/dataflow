"""
Takes a dataset with a defined polarization state (not None) and
calculates the row of the NT matrix that corresponds to each datapoint
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA, OSPEC_DATA_HE3


def append_polarization_matrix_module(id=None, datatype=None,
                                      cell_datatype=None, action=None,
                                      version='0.0', fields={},
                                      description="Append polarization matrix",
                                      xtype=None):
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
    
    xtype = 'AutosizeImageContainer'
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
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Append polarization matrix',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )

    return module

def append_polarization_matrix_action(input=[], he3cell=None, **kwargs):
    print "appending polarization matrix"
    he3analyzer = None
    if he3cell != None: # should always be true; he3cell is now required
        he3analyzer = he3cell[0]
    return dict(output=filters.AppendPolarizationMatrix().apply(input, he3cell=he3analyzer))
append_polarization_matrix = append_polarization_matrix_module(id='ospec.append', datatype=OSPEC_DATA,
                                                        cell_datatype=OSPEC_DATA_HE3, version='1.0', action=append_polarization_matrix_action)

