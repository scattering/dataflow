"""
SANS reduction modules
"""
import os, sys, math
import numpy as np
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir)
from pprint import pprint

from dataflow import config
from dataflow.calc import run_template
from dataflow.core import Datatype, Instrument, Template, register_instrument
from dataflow.modules.load import load_module
from dataflow.modules.save import save_module
from reduction.sans.filters import *
from dataflow.SANS.convertq import convertq_module
from dataflow.SANS.correct_detector_efficiency import correct_detector_efficiency_module
from dataflow.SANS.monitor_normalize import monitor_normalize_module
from dataflow.SANS.correct_background import correct_background_module
# Datatype
SANS_DATA = 'data1d.sans'
data2d = Datatype(id=SANS_DATA,
                  name='SANS Data',
                  plot='sansplot')

 
# Load module
def load_action(files=None, intent=None):
    print "loading", files
    result = [_load_data(f) for f in files] # not bundles
    return dict(output=result)
def _load_data(name):
    print name
    if os.path.splitext(name)[1] == ".DIV":
        return read_div(myfilestr=name)
    else:
        return read_sample(myfilestr=name)
    
load = load_module(id='sans.load', datatype=SANS_DATA,
                   version='1.0', action=load_action)


# Save module
def save_action(input=None, ext=None):
    for f in input: _save_one(f, ext) # not bundles
    return {}
def _save_one(input, ext):
    outname = initname = "/home/elakian/.txt"
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    with open(outname, 'w') as f:
        f.write(str(input.__str__()))
save = save_module(id='sans.save', datatype=SANS_DATA,
                   version='1.0', action=save_action)


# Modules
def monitor_normalize_action(input=None):
    
    #flat = []
    ##np.set_printoptions(edgeitems = 128)
    #for bundle in input:
        #flat.extend(bundle)
    result = [monitor_normalize(f) for f in input]
    return dict(output=result)
mon_norm = monitor_normalize_module(id='sans.monitor_normalize', datatype=SANS_DATA, version='1.0', action=monitor_normalize_action)

def convertq_action(input=None):
    flat = []
    for bundle in input:
        flat.extend(bundle)
    result = [convert_q(f) for f in flat]
    return dict(output=result)
convertq = convertq_module(id='sans.convertq', datatype=SANS_DATA, version='1.0', action=convertq_action)

def correct_detector_efficiency_action(input=None):
    result = [correct_detector_efficiency(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_det_eff = correct_detector_efficiency_module(id='sans.correct_detector_efficiency', datatype=SANS_DATA, version='1.0', action=correct_detector_efficiency_action)

def correct_background_action(input=None):
    result = [correct_background(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_back = correct_background_module(id='sans.correct_background', datatype=SANS_DATA, version='1.0', action=correct_background_action)

#Instrument definitions
SANS_INS = Instrument(id='ncnr.sans.ins',
                 name='NCNR SANS INS',
                 archive=config.NCNR_DATA + '/sansins',
                 menu=[('Input', [load, save]),
                       ('Reduction', [convertq,correct_det_eff,mon_norm,correct_back])
                                              ],
                 requires=[config.JSCRIPT + '/sansplot.js'],
                 datatypes=[data2d],
                 )
instruments = [SANS_INS]

# Testing
if __name__ == '__main__':
    for instrument in instruments:
        register_instrument(instrument)
    modules = [
        dict(module="sans.load", position=(5, 20),
             config={'files': ["/home/elakian/dataflow/reduction/sans/ncnr_sample_data/PLEX_2NOV2007_NG3.DIV","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC002.SA3_SRK_S102","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC005.SA3_SRK_S105","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC006.SA3_SRK_S106","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC010.SA3_SRK_S110"], 'intent': 'signal'}),
        dict(module="sans.save", position=(280, 40), config={'ext': 'dat'}),
        dict(module="sans.monitor_normalize", position=(360 , 60), config={}),
        dict(module="sans.correct_detector_efficiency", position=(360 , 60), config={}),
        dict(module="sans.correct_background", position=(360 , 60), config={}),
        ]
    wires = [
        dict(source=[0, 'output'], target=[2, 'input']),
        dict(source=[2, 'output'], target=[1, 'input']),
        
        ]
    config = [d['config'] for d in modules]
    template = Template(name='test sans',
                        description='example sans diagram',
                        modules=modules,
                        wires=wires,
                        instrument=SANS_INS.id,
                        )
    result = run_template(template, config)
    pprint(result)
    