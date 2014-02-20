"""
Load data sets from Asterix.
"""
import os
import types

from reduction.offspecular import filters

from ... import config
from ...core import Module
from ...modules.load import load_module

from ..datatypes import OSPEC_DATA, get_friendly_name

def load_asterix_module(id=None, datatype=None, action=None,
                version='0.0', fields=[], xtype=None, **kwargs):
    """Module for loading an Asterix dataset"""

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
        "label": "Files",
        "name": "files",
        "value": []
        }
    }
    
#    center_pixel_field = {
#        "label": "Center Pixel", 
#        "name": "center_pixel", 
#        "type": "float", 
#        "value": 145.0,        
#    }
#    wl_over_tof_field = {
#        "label": "Wavelength over Time-of-Flight", 
#        "name": "wl_over_tof", 
#        "type": "scientific", 
#        "value": 1.9050372144288577e-5,
#    }    
#    pw_over_d_field = {
#        "label": "Pixel width/distance (to sample)", 
#        "name": "pixel_width_over_dist", 
#        "type": "float", 
#        "value":  0.00034113856493630764,
#    }

      
    # Combine everything into a module.
    module = Module(id=id,
                  name='LoadAsterix',
                  version=version,
                  description=action.__doc__,
                  #icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  xtype=xtype,
                  **kwargs
                  )

    return module

def load_asterix_action(input=[], files=[], **kwargs):
    result = []
    for f in files:
        subresult = _load_asterix_data(f)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    for subresult in input:
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
        #result = [_load_data(f, auto_PolState, PolStates.get(get_friendly_name(os.path.split(f)[-1]), '')) for f in files] # not bundles
    return dict(output=result)

def _load_asterix_data(name):
    (dirName, fileName) = os.path.split(name)
    friendly_name = get_friendly_name(fileName)
    print "friendly_name:", friendly_name
    if friendly_name.endswith('hdf'):
        format = "HDF4"
    else: #h5
        format = "HDF5"
    return filters.LoadAsterixRawHDF(fileName, path=dirName, friendly_name=friendly_name, format=format )
    #return SuperLoadAsterixHDF(fileName, path=dirName, center_pixel=center_pixel, wl_over_tof=wl_over_tof, pixel_width_over_dist=pixel_width_over_dist, format=format )

#load_asterix = load_asterix_module(id='ospec.asterix.load', datatype=OSPEC_DATA,
#                   version='1.0', action=load_asterix_action, filterModule=LoadAsterixRawHDF)
autochain_loader_field = {
    "type":"boolean",
    "label": "Cache individual files",
    "name": "autochain-loader",
    "value": False,
    }

load_asterix = load_module(id='ospec.asterix.load', datatype=OSPEC_DATA,
                           version='1.0', action=load_asterix_action, fields={'autochain-loader':autochain_loader_field}, filterModule=filters.LoadAsterixRawHDF)

