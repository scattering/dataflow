"""
SANS reduction modules
"""
import os, sys, math
import numpy as np
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir)
from pprint import pprint

from .. import config
from ..calc import run_template
from ..core import Datatype, Instrument, Template, register_instrument
from ..modules.load import load_module
from ..modules.save import save_module
from ...reduction.sans.filters import *
from ..SANS.convertq import convertq_module
from ..SANS.correct_detector_efficiency import correct_detector_efficiency_module
from ..SANS.monitor_normalize import monitor_normalize_module
from ..SANS.correct_background import correct_background_module
from ..SANS.generate_transmission import generate_transmission_module
from ..SANS.initial_correction import initial_correction_module
from ..SANS.correct_solid_angle import correct_solid_angle_module
from ..SANS.convert_qxqy import convert_qxqy_module
from ..SANS.annular_av import annular_av_module
from ..SANS.absolute_scaling import absolute_scaling_module

#from ... import ROOT_URL

#print 'repo', ROOT_URL.REPO_ROOT
#print 'home', ROOT_URL.HOMEDIR

#from dataflow import config
#from dataflow.calc import run_template
#from dataflow.core import Datatype, Instrument, Template, register_instrument
#from dataflow.modules.load import load_module
#from reduction.sans.filters import *
#from dataflow.SANS.convertq import convertq_module
#from dataflow.SANS.correct_detector_efficiency import correct_detector_efficiency_module
#from dataflow.SANS.monitor_normalize import monitor_normalize_module
#from dataflow.SANS.correct_background import correct_background_module
#from dataflow.SANS.generate_transmission import generate_transmission_module
#from dataflow.SANS.initial_correction import initial_correction_module
#from dataflow.SANS.correct_solid_angle import correct_solid_angle_module
#from dataflow.SANS.convert_qxqy import convert_qxqy_module
#from dataflow.SANS.annular_av import annular_av_module
#from dataflow.SANS.absolute_scaling import absolute_scaling_module
import json, simplejson
#Transmissions
Tsam = 0
Temp = 0
#Qx,Qy
qx = {}
qy = {}
correctVer = SansData()
#List of Files
global fileList
 
# Datatype
SANS_DATA = 'data1d.sans'
data2d = Datatype(id=SANS_DATA,
                  name='SANS Data',
                  plot='sansplot')

 
# Load module
def load_action(files=None, intent=None):
    print "loading", files
    result = [_load_data(f) for f in files] # not bundles
    global fileList
    fileList = result
    plottable_2D = {
    'z': fileList[0].data.x.tolist(),
    'title': 'SAM',
    'dims': {
      'xmax': 128.0,
      'xmin': 0.0,
      'ymin': 0.0,
      'ymax': 128.0,
      'xdim': 128,
      'ydim': 128,
    },
    'xlabel': 'X',
    'ylabel': 'Y',
    'zlabel': 'Intensity',
};
    #plottable_2D = json.dumps(plottable_2D)
    #return dict(output=plottable_2D)
def _load_data(name):
    print name
    if os.path.splitext(name)[1] == ".DIV":
        return read_div(myfilestr=name)
    else:
        return read_sample(myfilestr=name)
    
load = load_module(id='sans.load', datatype=SANS_DATA,version='1.0', action=load_action)


# Save module
def save_action(input=None, ext=None):
    for f in input: _save_one(f, ext) # not bundles
    return {}
def _save_one(input, ext):
    outname = initname = map_files('save')
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
    result = [monitor_normalize(f) for f in input]
    print "result: ", result
    return result

def generate_transmission_action(input=None):
    
    print "input: ",input
    
    global Tsam,Temp
    coord_left=(60,60)
    coord_right=(70,70)
    Tsam=generate_transmission(input[3],input[2],coord_left,coord_right)
    Temp=generate_transmission(input[4],input[2],coord_left,coord_right)
    print 'Sample transmission= {0} (IGOR Value = 0.724): '.format(Tsam)
    print 'Empty Cell transmission= {0} (IGOR Value = 0.929): '.format(Temp)
    
    
   
def initial_correction_action(input=None):
    global fileList
    lis = []
    for i in fileList:
            lis.append(i)
       
    print "Lis: ",lis
    lis = monitor_normalize_action(lis[0:6])
    generate_transmission_action(lis)
    
    
    #SAM,BGD,EMP,Trans
    global Tsam,Temp
    BGD = fileList[len(fileList)-2]
    COR = initial_correction(fileList[0],BGD,fileList[1],Tsam/Temp)
    print COR.data.x
    global correctVer
    correctVer = COR
    print "result: ", correctVer

    plottable_2D = {
    'z': COR.data.x.tolist(),
    'title': 'COR',
    'dims': {
      'xmax': 128.0,
      'xmin': 0.0,
      'ymin': 0.0,
      'ymax': 128.0,
      'xdim': 128,
      'ydim': 128,
    },
    'xlabel': 'X',
    'ylabel': 'Y',
    'zlabel': 'Intensity',
};
    #plottable_2D = json.dumps(plottable_2D)
    #return dict(output=plottable_2D)
initial_corr = initial_correction_module(id='sans.initial_correction', datatype=SANS_DATA, version='1.0', action=initial_correction_action)

def convertq_action():
    global correctVer
    result = convert_q(correctVer)
    return result

def correct_solid_angle_action():
    global correctVer
    result = correct_solid_angle(correctVer)
    return result

def correct_detector_efficiency_action(input=None):
    global fileList,correctVer
    print "input: ",input
    sensitivity = fileList[len(fileList)-1]
    DIV = correct_detector_efficiency(fileList[0],sensitivity)
    correctVer = DIV
    plottable_2D = {
    'z': correctVer.data.x.tolist(),
    'title': 'DIV',
    'dims': {
      'xmax': 128.0,
      'xmin': 0.0,
      'ymin': 0.0,
      'ymax': 128.0,
      'xdim': 128,
      'ydim': 128,
    },
    'xlabel': 'X',
    'ylabel': 'Y',
    'zlabel': 'Intensity',
};
    #plottable_2D = json.dumps(plottable_2D)
    
    result = plottable_2D
   # return dict(output=result)
correct_det_eff = correct_detector_efficiency_module(id='sans.correct_detector_efficiency', datatype=SANS_DATA, version='1.0', action=correct_detector_efficiency_action)
def convert_qxqy_action():
    global correctVer,qx,qy
    correctVer,qx,qy = convert_qxqy(correctVer)
    print "Convertqxqy"
def annular_av_action(input=None):
    global correctVer,fileList
    AVG = annular_av(correctVer)
    result = AVG
    print "AVG: ",result
    return dict(output=result)
annul_av = annular_av_module(id='sans.annular_av', datatype=SANS_DATA, version='1.0', action=annular_av_action)
def absolute_scaling_action(input=None):
    #sample,empty,DIV,Tsam,instrument
    global correctVer,fileList,Tsam,qx,qy
    correctVer = convertq_action()
    correctVer = correct_solid_angle_action()
    convert_qxqy_action()
    sensitivity = fileList[len(fileList)-1]
    EMP = fileList[2]
    ABS = absolute_scaling(correctVer,EMP,sensitivity,Tsam,'NG3')
    result = [ABS]
    print "abs: ",result
    plottable_2D = {
    'z': ABS.data.x.tolist(),
    'title': 'COR',
    'dims': {
      'xmax': 128.0,
      'xmin': 0.0,
      'ymin': 0.0,
      'ymax': 128.0,
      'xdim': 128,
      'ydim': 128,
    },
    'xlabel': 'X',
    'ylabel': 'Y',
    'zlabel': 'Intensity',
};
    #plottable_2D = json.dumps(plottable_2D)
   # return dict(output=plottable_2D);
absolute = absolute_scaling_module(id='sans.absolute_scaling', datatype=SANS_DATA, version='1.0', action=absolute_scaling_action)

def correct_background_action(input=None):
    result = [correct_background(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_back = correct_background_module(id='sans.correct_background', datatype=SANS_DATA, version='1.0', action=correct_background_action)

#Instrument definitions
SANS_INS = Instrument(id='ncnr.sans.ins',
                 name='NCNR SANS INS',
                 archive=config.NCNR_DATA + '/sansins',
                 menu=[('Input', [load, save]),
                       ('Reduction', [correct_det_eff,correct_back,initial_corr,annul_av,absolute])
                                              ],
                 requires=[config.JSCRIPT + '/sansplot.js'],
                 datatypes=[data2d],
                 )
instruments = [SANS_INS]

# Testing
#if __name__ == '__main__':
def TESTING():
    global fileList
    fileList = [map_files('sample_4m'),map_files('empty_cell_4m'),map_files('empty_4m'),map_files('trans_sample_4m'),map_files('trans_empty_cell_4m'),map_files('blocked_4m'),map_files('div')]
    #fileList = ["/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC010.SA3_SRK_S110","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC008.SA3_SRK_S108","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC002.SA3_SRK_S102","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC006.SA3_SRK_S106","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC005.SA3_SRK_S105"]
    for instrument in instruments:
        register_instrument(instrument)
    modules = [
        dict(module="sans.load", position=(5, 20),
             config={'files': fileList, 'intent': 'signal'}),
        dict(module="sans.save", position=(280, 40), config={'ext': 'dat'}),
        dict(module="sans.initial_correction", position=(360 , 60), config={}),
        dict(module="sans.correct_detector_efficiency", position=(360 , 60), config={}),
        dict(module="sans.absolute_scaling", position=(360 , 60), config={}),
        dict(module="sans.annular_av", position=(360 , 60), config={}),
        
        #dict(module="sans.correct_background", position=(360 , 60), config={}),
        
        ]
    wires = [
        dict(source=[0, 'output'], target=[2, 'input']),
        dict(source=[2, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
        dict(source=[5, 'output'], target=[1, 'input']),

        ]
    config = [d['config'] for d in modules]
    template = Template(name='test sans',
                        description='example sans data',
                        modules=modules,
                        wires=wires,
                        instrument=SANS_INS.id,
                        )
    return run_template(template, config)
        
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
