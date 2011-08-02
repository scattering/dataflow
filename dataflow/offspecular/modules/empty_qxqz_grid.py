"""
Create an empty qxqz grid
"""

from ... import config
from ...core import Module

def empty_qxqz_grid_module(id=None, datatype=None, action=None,
                version='0.0', fields=[]):
    """Module for creating QxQz grids"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "empty_qxqz.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "empty_qxqz_image.png",
        'terminals': {
            'output': (20, 10, 1, 0),
        }
    }
    
    terminals = [
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data',
             ),
    ]

    # qxmin, qxmax, qxbins, qzmin, qzmax, qzbins
    # (-0.003, 0.003, 201, 0, 0.1, 201)
    qxmin_field = {
        "type":"float",
        "label": "Qx min",
        "name": "qxmin",
        "value":-0.003,
    }
    qxmax_field = {
        "type":"float",
        "label": "Qx max",
        "name": "qxmax",
        "value": 0.003,
    }
    qxbins_field = {
        "type":"int",
        "label": "Qx bins",
        "name": "qxbins",
        "value": 201,
    }
    qzmin_field = {
        "type":"float",
        "label": "Qz min",
        "name": "qzmin",
        "value": 0.0,
    }
    qzmax_field = {
        "type":"float",
        "label": "Qz max",
        "name": "qzmax",
        "value": 0.1,
    }
    qzbins_field = {
        "type":"int",
        "label": "Qz bins",
        "name": "qzbins",
        "value": 201,
    }
    
    # Combine everything into a module.
    module = Module(id=id,
                  name='Empty QxQz grid',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=[qxmin_field, qxmax_field, qxbins_field, qzmin_field, qzmax_field, qzbins_field] + fields,
                  action=action,
                  )
    module.LABEL_WIDTH = 150
    return module
