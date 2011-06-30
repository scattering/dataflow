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
from dataflow.SANS.generate_transmission import generate_transmission_module
from dataflow.SANS.initial_correction import initial_correction_module
from dataflow.SANS.correct_solid_angle import correct_solid_angle_module
from dataflow.SANS.convert_qxqy import convert_qxqy_module
from dataflow.SANS.annular_av import annular_av_module

#Transmissions
Tsam = 0
Temp = 0
qx = {}
qy = {}
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
    outname = initname = "/home/elakian/sansdatafile.txt"
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    with open(outname, 'w') as f:
        f.write(str(input.__str__()))
save = save_module(id='sans.save', datatype=SANS_DATA,
                   version='1.0', action=save_action)


# Modules
def monitor_normalize_action(input=None):
    
    #np.set_printoptions(edgeitems = 128)
    #print "input",input
    ##flat = []
        
    #file = open("/home/elakian/sansdata2.dat","w")
    
    #x = monitor_normalize(input[0][0])
    #file.write(repr(x.data.x))
    
    #file.close()
    
    #for bundle in input:
        #flat.extend(bundle)
    x = 0
    #print "size: ", len(input[0])
    #result = []
    #for f in input:
        #result= [monitor_normalize(input[0][x])]
        #x+=1
    result = [monitor_normalize(f) for f in input[0]]
    print "result: ", result
    return dict(output=result)
mon_norm = monitor_normalize_module(id='sans.monitor_normalize', datatype=SANS_DATA, version='1.0', action=monitor_normalize_action)

def generate_transmission_action(input=None):
    
    print "input: ",input
    
    global Tsam,Temp
    coord_left=(60,60)
    coord_right=(70,70)
    Tsam=generate_transmission(input[0][3],input[0][2],coord_left,coord_right)
    Temp=generate_transmission(input[0][4],input[0][2],coord_left,coord_right)
    print 'Sample transmission= {0} (IGOR Value = 0.724): '.format(Tsam)
    print 'Empty Cell transmission= {0} (IGOR Value = 0.929): '.format(Temp)
    return dict(output=input[0])
    #result = [generate_transmission(f) for f in flat]
    #return dict(output=result)
gen_trans = generate_transmission_module(id='sans.generate_transmission', datatype=SANS_DATA, version='1.0', action=generate_transmission_action)
def initial_correction_action(input=None):
    #SAM,BGD,EMP,Trans
    global Tsam,Temp
    BGD = read_sample("/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC007.SA3_SRK_S107")
    COR = initial_correction(input[0][0],BGD,input[0][1],Tsam/Temp)
    print COR.data.x
    result = [COR]
    return dict(output=result)
initial_corr = initial_correction_module(id='sans.initial_correction', datatype=SANS_DATA, version='1.0', action=initial_correction_action)

def convertq_action(input=None):
    result = [convert_q(input[0][0])]
    return dict(output=result)
convq = convertq_module(id='sans.convertq', datatype=SANS_DATA, version='1.0', action=convertq_action)
def correct_solid_angle_action(input=None):
    
    print "input#########: ",input
    result = [correct_solid_angle(input[0][0])]
    return dict(output=result)
solid_angle = correct_solid_angle_module(id='sans.correct_solid_angle', datatype=SANS_DATA, version='1.0', action=correct_solid_angle_action)
def correct_detector_efficiency_action(input=None):
    sensitivity = read_div("/home/elakian/dataflow/reduction/sans/ncnr_sample_data/PLEX_2NOV2007_NG3.DIV")
    DIV = correct_detector_efficiency(input[0][0],sensitivity)
    result = [DIV]
    return dict(output=result)
correct_det_eff = correct_detector_efficiency_module(id='sans.correct_detector_efficiency', datatype=SANS_DATA, version='1.0', action=correct_detector_efficiency_action)
def convert_qxqy_action(input=None):
    global qx,qy
    CON,qx,qy = convert_qxqy(input[0][0])
    result = [CON]
    return dict(output=result)
qxqy = convert_qxqy_module(id='sans.convert_qxqy', datatype=SANS_DATA, version='1.0', action=convert_qxqy_action)
def annular_av_action(input=None):
   # input = input[0]
    #AVG = annular_av(input[0])
    #result = [AVG]
    return ;#dict(output=result)
annul_av = annular_av_module(id='sans.annular_av', datatype=SANS_DATA, version='1.0', action=annular_av_action)

def correct_background_action(input=None):
    result = [correct_background(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_back = correct_background_module(id='sans.correct_background', datatype=SANS_DATA, version='1.0', action=correct_background_action)

#Instrument definitions
SANS_INS = Instrument(id='ncnr.sans.ins',
                 name='NCNR SANS INS',
                 archive=config.NCNR_DATA + '/sansins',
                 menu=[('Input', [load, save]),
                       ('Reduction', [convq,correct_det_eff,mon_norm,correct_back,gen_trans,initial_corr,solid_angle,qxqy,annul_av])
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
             config={'files': ["/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC010.SA3_SRK_S110","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC008.SA3_SRK_S108","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC002.SA3_SRK_S102","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC006.SA3_SRK_S106","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC005.SA3_SRK_S105"], 'intent': 'signal'}),
        dict(module="sans.save", position=(280, 40), config={'ext': 'dat'}),
        dict(module="sans.monitor_normalize", position=(360 , 60), config={}),
        dict(module="sans.generate_transmission", position=(360 , 60), config={}),
        dict(module="sans.initial_correction", position=(360 , 60), config={}),
        dict(module="sans.correct_detector_efficiency", position=(360 , 60), config={}),
        dict(module="sans.convertq", position=(360 , 60), config={}),
        dict(module="sans.correct_solid_angle", position=(360 , 60), config={}),
        dict(module="sans.convert_qxqy", position=(360 , 60), config={}),
        dict(module="sans.annular_av", position=(360 , 60), config={}),
        dict(module="sans.correct_background", position=(360 , 60), config={}),
        
        ]
    wires = [
        dict(source=[0, 'output'], target=[2, 'input']),
        dict(source=[2, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
        dict(source=[5, 'output'], target=[6, 'input']),
        dict(source=[6, 'output'], target=[7, 'input']),
        dict(source=[7, 'output'], target=[8, 'input']),
        dict(source=[8, 'output'], target=[9, 'input']),
        dict(source=[9, 'output'], target=[1, 'input']),
        ]
    config = [d['config'] for d in modules]
    template = Template(name='test sans',
                        description='example sans data',
                        modules=modules,
                        wires=wires,
                        instrument=SANS_INS.id,
                        )
    result = run_template(template, config)
    pprint(result)
        
    #datadir=os.path.join(os.path.dirname(__file__),'ncnr_sample_data')
    #filedict={'empty_1m':os.path.join(datadir,'SILIC001.SA3_SRK_S101'),
              #'empty_4m':os.path.join(datadir,'SILIC002.SA3_SRK_S102'),
              #'empty_cell_1m':os.path.join(datadir,'SILIC003.SA3_SRK_S103'),
              #'blocked_1m':os.path.join(datadir,'SILIC004.SA3_SRK_S104'),
              #'trans_empty_cell_4m':os.path.join(datadir,'SILIC005.SA3_SRK_S105'),
              #'trans_sample_4m':os.path.join(datadir,'SILIC006.SA3_SRK_S106'),
              #'blocked_4m':os.path.join(datadir,'SILIC007.SA3_SRK_S107'),
              #'empty_cell_4m':os.path.join(datadir,'SILIC008.SA3_SRK_S108'),
              #'sample_1m':os.path.join(datadir,'SILIC009.SA3_SRK_S109'),
              #'sample_4m':os.path.join(datadir,'SILIC010.SA3_SRK_S110'),
              #'mask':os.path.join(datadir,'DEFAULT.MASK'),
              #'div':os.path.join(datadir,'PLEX_2NOV2007_NG3.DIV'),
              #}
