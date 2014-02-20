"""
Module to convert two theta to QxQz
"""

from reduction.offspecular import filters

from ... import config
from ...core import Module
try:
    from collections import OrderedDict
except:
    from ...ordered_dict import OrderedDict

from ..datatypes import OSPEC_DATA

def two_theta_lambda_qxqz_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, xtype=None, **kwargs):
    """Creates a module for converting two theta and lambda to qx and qz"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "qxqz.png", 
        'image': config.IMAGES + config.ANDR_FOLDER + "twothetalambda_qxqz_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'output_grid': (-12, 40, -1, 0),
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
        dict(id='output_grid',
             datatype=datatype,
             use='in',
             description='output grid',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='data with qxqz',
             ),
    ]
    
    fields = OrderedDict()
    fields["theta"] = {
            "type":"string",
            "label": "Sample angle (theta - leave blank to use motor value from datafile)",
            "name": "theta",
            "value": "",
        }
    fields["qxmin"] = {
            "type":"float",
            "label": "Qx min",
            "name": "qxmin",
            "value":-0.003,
        }
    fields["qxmax"] = {
            "type":"float",
            "label": "Qx max",
            "name": "qxmax",
            "value": 0.003,
        }
    fields["qxbins"] = {
            "type":"float",
            "label": "Qx bins",
            "name": "qxbins",
            "value": 201,
        }
    fields["qzmin"] = {
            "type":"float",
            "label": "Qz min",
            "name": "qzmin",
            "value": 0.0,
        }
    fields["qzmax"] = {
            "type":"float",
            "label": "Qz max",
            "name": "qzmax",
            "value": 0.1,
        }
    fields["qzbins"] = {
            "type":"float",
            "label": "Qz bins",
            "name": "qzbins",
            "value": 201,
        }

    # Combine everything into a module.
    module = Module(id=id,
                  name='Two theta lambda to qxqz',
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


# Two theta Lambda to qxqz module
def two_theta_lambda_qxqz_action(input=[], theta=None, qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201,**kwargs):
    print "converting two theta and lambda to qx and qz"
    result = filters.TwothetaLambdaToQxQz().apply(input, theta, qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
    return dict(output=result)
two_theta_lambda_qxqz = two_theta_lambda_qxqz_module(id='ospec.tth_wl_qxqz', datatype=OSPEC_DATA, version='1.0', action=two_theta_lambda_qxqz_action)

