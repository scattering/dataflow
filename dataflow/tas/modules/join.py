"""
Join data sets
"""

from reduction.tas import data_abstraction

from ... import config
from ...core import Module

from ..datatypes import TAS_DATA

def join_module(id=None, datatype=None, action=None,
                version='0.0', fields={},
                description="Combine multiple datasets", **kwargs):
    """
    Return a module for combining multiple datasets
    """

    icon = {
        'URI': config.IMAGES + 'TAS/join.png',
        'image': config.IMAGES + 'TAS/join.png',
        'width': 64, #'auto', 
        'terminals': {
            'input': (-12, 16, -1, 0),
            'output': (48, 16, 2, 0),
        }
    }
    
    
    terminals = [
        dict(id='input',
             datatype=datatype,
             use='in',
             description='Data parts',
             required=False,
             multiple=False,
             ),
        dict(id='output',
             datatype=datatype,
             use='out',
             description='Combined data',
             ),
    ]
    _ = '''
    fields = {
        'xaxis': {
            "type": "string",
            "label": "X axis for 2D plotting",
            "name": "xaxis",
            "value": '',
        }, 
        'yaxis': {
            "type": "string",
            "label": "Y axis for 2D plotting",
            "name": "yaxis",
            "value": '',
        },
        'num_bins': {
            "type": "float",
            "label": "Number of bins (optional)",
            "name": "num_bins",
            "value": 0.0,
        },
        'xstep': {
            "type": "float",
            "label": "X bin spacing/step (optional)",
            "name": "xstep",
            "value": None,
        },
        'ystep': {
            "type": "float",
            "label": "Y bin spacing/step (optional)",
            "name": "ystep",
            "value": None,
        }
    }
    '''
    # Combine everything into a module.
    module = Module(id=id,
                  name='Join',
                  version=version,
                  description=description,
                  icon=icon,
                  terminals=terminals,
                  fields=fields,
                  action=action,
                  **kwargs
                  )

    return module



def join_action(input, xaxis='', yaxis='', num_bins=0, xstep=None, ystep=None,
                fields={}, **kwargs):
    # This is confusing because load returns a bundle and join, which can
    # link to multiple loads, has a list of bundles.  So flatten this list.
    # The confusion between bundles and items will bother us continuously,
    # and it is probably best if every filter just operates on and returns
    # bundles, which I do in this example.

    #print "JOINING",input

    #for now, we will work on joining arbitrary inputs instead of two at a time...
    #This will hopefully work on bundles, instead of doing things pairwise...
    joinedtas = data_abstraction.join(input)

    # convert extract fields['name']['value'] to fields['name']
    fields = dict((k,v['value']) for k,v in fields.items())
    # assign joinedtas attributes from fields if present, otherwise from
    # direct function parameters
    joinedtas.xaxis = fields.get('xaxis',xaxis)
    joinedtas.yaxis = fields.get('yaxis',yaxis)
    joinedtas.num_bins = fields.get('num_bins',num_bins)
    joinedtas.xstep = fields.get('xstep',xstep)
    joinedtas.ystep = fields.get('ystep',ystep)
    return dict(output=[joinedtas])


fields = {
    #TODO get the choices from the data object, NOT hardcoded in. 7/25/2012
    'xaxis': {
        "type": "List",
        "label": "X axis for 2D plotting",
        "name": "xaxis",
        "value": '',
        "choices": ["h", "k", "l", "q", "e", "ef", "focus_pg", "elevation", "translation", "focus_cu", "filter_translation", "filter_tilt", "filter_rotation", "ei_cancel", "sample_guide_field_rotatation", "flipper_state", "vsample", "eta", "hsample", "zeta", "ei_flip", "ef_guide", "sample_lower_translation", "analyzer_rotation", "sample_lower_tilt", "sample_elevator", "sample_upper_tilt", "sample_two_theta", "analyzer_theta", "sample_upper_translation", "monochromator_theta", "monochromator_two_theta", "dfm_rotation", "analyzer_two_theta", "sample_theta", "back_slit_width", "back_slit_height", "analyzerblade0", "analyzerblade1", "analyzerblade2", "analyzerblade3", "analyzerblade4", "analyzerblade5", "analyzerblade6", "analyzerblade7", "temperature_control_reading", "temperature_heater_power", "temperature", "temperature_setpoint", "soller_collimator", "radial_collimator", "post_analyzer_collimator", "pre_analyzer_collimator", "post_monochromator_collimator", "pre_monochromator_collimator", "aperture_horizontal", "aperture_vertical",
"orient2", "ei", "orient3", "orient1", "monitor", "timestamp", "duration", "monitor2"],
    },
    'yaxis': {
        "type": "List",
        "label": "Y axis for 2D plotting",
        "name": "yaxis",
        "value": '',
        "choices": ["e", "ef", "h", "k", "l", "q", "focus_pg", "elevation", "translation", "focus_cu", "filter_translation", "filter_tilt", "filter_rotation", "ei_cancel", "sample_guide_field_rotatation", "flipper_state", "vsample", "eta", "hsample", "zeta", "ei_flip", "ef_guide", "sample_lower_translation", "analyzer_rotation", "sample_lower_tilt", "sample_elevator", "sample_upper_tilt", "sample_two_theta", "analyzer_theta", "sample_upper_translation", "monochromator_theta", "monochromator_two_theta", "dfm_rotation", "analyzer_two_theta", "sample_theta", "back_slit_width", "back_slit_height", "analyzerblade0", "analyzerblade1", "analyzerblade2", "analyzerblade3", "analyzerblade4", "analyzerblade5", "analyzerblade6", "analyzerblade7", "temperature_control_reading", "temperature_heater_power", "temperature", "temperature_setpoint", "soller_collimator", "radial_collimator", "post_analyzer_collimator", "pre_analyzer_collimator", "post_monochromator_collimator", "pre_monochromator_collimator", "aperture_horizontal", "aperture_vertical",
"orient2", "ei", "orient3", "orient1", "monitor", "timestamp", "duration", "monitor2"],
    },
    'num_bins': {
        "type": "float",
        "label": "Number of bins (optional)",
        "name": "num_bins",
        "value": 0.0,
    },
    'xstep': {
        "type": "float",
        "label": "X bin spacing/step (optional)",
        "name": "xstep",
        "value": None,
    },
    'ystep': {
        "type": "float",
        "label": "Y bin spacing/step (optional)",
        "name": "ystep",
        "value": None,
    }
}



join = join_module(id='tas.join', datatype=TAS_DATA, fields=fields,
                   version='1.0', action=join_action, filterModule=data_abstraction.join)
join.xtype = 'JoinContainer'
