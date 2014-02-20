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

def theta_two_theta_qxqz_module(id=None, datatype=None, action=None,
                 version='0.0', fields={}, xtype=None, **kwargs):
    """Creates a module for converting theta and two theta to qx and qz"""

    icon = {
        'URI': config.IMAGES + config.ANDR_FOLDER + "qxqz.png",
        'image': config.IMAGES + config.ANDR_FOLDER + "qxqz_image.png",
        'terminals': {
            'input': (-12, 4, -1, 0),
            'output_grid': (-12, 40, -1, 0),
            'output': (48, 16, 1, 0),
        }
    }
    
    xtype='AutosizeImageContainer'
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
    
    fields = OrderedDict(fields)
    fields["wavelength"] = {
            "type":"float",
            "label": "wavelength",
            "name": "wavelength",
            "value": 5.0,
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
                  name='Theta two theta to qxqz',
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


# Theta Two theta to qxqz module
def theta_two_theta_qxqz_action(input=[], output_grid=None, wavelength=5.0, qxmin= -0.003, qxmax=0.003, qxbins=201, qzmin=0.0, qzmax=0.1, qzbins=201,**kwargs):
    print "converting theta and two theta to qx and qz"
    grid = None
    if output_grid != None:
        grid = output_grid[0]
    result = filters.ThetaTwothetaToQxQz().apply(input, grid, wavelength, qxmin, qxmax, qxbins, qzmin, qzmax, qzbins)
    return dict(output=result)
theta_two_theta_qxqz = theta_two_theta_qxqz_module(id='ospec.th_tth_qxqz', datatype=OSPEC_DATA, version='1.0', action=theta_two_theta_qxqz_action)
