"""
Create an empty qxqz grid
"""
from reduction.offspecular import filters

from ... import config
from ...core import Module

from ..datatypes import OSPEC_DATA

def empty_qxqz_grid_module(id=None, datatype=None, action=None,
                version='0.0', fields=[], xtype=None):
    """Module for creating QxQz grids"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "empty_qxqz.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "empty_qxqz_image.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    xtype = 'AutosizeImageContainer'
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    # qxmin, qxmax, qxbins, qzmin, qzmax, qzbins
    # (-0.003, 0.003, 201, 0, 0.1, 201)
    fields = {
        "qxmin":  {
            "type":"float",
            "label": "Qx min",
            "name": "qxmin",
            "value":-0.003,
        },
        "qxmax":  {
            "type":"float",
            "label": "Qx max",
            "name": "qxmax",
            "value": 0.003,
        },
        "qxbins":  {
            "type":"int",
            "label": "Qx bins",
            "name": "qxbins",
            "value": 201,
        },
        "qzmin":  {
            "type":"float",
            "label": "Qz min",
            "name": "qzmin",
            "value": 0.0,
        },
        "qzmax":  {
            "type":"float",
            "label": "Qz max",
            "name": "qzmax",
            "value": 0.1,
        },
        "qzbins":  {
            "type":"int",
            "label": "Qz bins",
            "name": "qzbins",
            "value": 201,
        }
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Empty QxQz grid',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype
                  )
    module.LABEL_WIDTH = 150
    return module

def empty_qxqz_grid_action(qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201, **kwargs):
    print "creating an empty QxQz grid"
    return dict(output=[filters.EmptyQxQzGridPolarized(qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)])
empty_qxqz_grid = empty_qxqz_grid_module(id='ospec.emptyqxqz', datatype=OSPEC_DATA, version='1.0', action=empty_qxqz_grid_action)


