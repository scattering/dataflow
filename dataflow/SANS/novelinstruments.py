"""
SANS reduction modules
"""
import json, simplejson
import os, sys, math
import numpy as np
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir)
from pprint import pprint

if 1:
	from ...dataflow import wireit
	from .. import config
	from ..calc import run_template
	from .. import wireit
	from ..core import Data, Instrument, Template, register_instrument
	from ..modules.load import load_module
	from ..modules.save import save_module
	from ...reduction.sans.filters import *
	from ..SANS.convertq import convertq_module
	from ..SANS.correct_detector_sensitivity import correct_detector_sensitivity_module
	from ..SANS.monitor_normalize import monitor_normalize_module
	from ..SANS.correct_background import correct_background_module
	from ..SANS.generate_transmission import generate_transmission_module
	from ..SANS.initial_correction import initial_correction_module
	from ..SANS.correct_solid_angle import correct_solid_angle_module
	from ..SANS.convert_qxqy import convert_qxqy_module
	from ..SANS.annular_av import annular_av_module
	from ..SANS.absolute_scaling import absolute_scaling_module
	from ..SANS.correct_dead_time import correct_dead_time_module
	#from ...reduction.sans.filters import SansData
	#from ...reduction.sans.filters import plot1D
	#from ...reduction.sans.filters import div
	from ...apps.tracks.models import File


from django.utils import simplejson

#from ... import ROOT_URL

#print 'repo', ROOT_URL.REPO_ROOT
#print 'home', ROOT_URL.HOMEDIR

if 0:
	import dataflow.wireit as wireit

	from dataflow import config

	from dataflow.calc import run_template, get_plottable
	from dataflow.core import Data, Instrument, Template, register_instrument
	from dataflow.modules.load import load_module
	from dataflow.modules.save import save_module
	from reduction.sans.filters import *
	from dataflow.SANS.convertq import convertq_module
	from dataflow.SANS.correct_detector_efficiency import correct_detector_efficiency_module
	from dataflow.SANS.correct_detector_sensitivity import correct_detector_sensitivity_module
	from dataflow.SANS.monitor_normalize import monitor_normalize_module
	from dataflow.SANS.correct_background import correct_background_module
	from dataflow.SANS.generate_transmission import generate_transmission_module
	from dataflow.SANS.initial_correction import initial_correction_module
	from dataflow.SANS.correct_solid_angle import correct_solid_angle_module
	from dataflow.SANS.convert_qxqy import convert_qxqy_module
	from dataflow.SANS.annular_av import annular_av_module
	from dataflow.SANS.absolute_scaling import absolute_scaling_module
	from dataflow.SANS.correct_dead_time import correct_dead_time_module
	#from apps.tracks.models import File
if 0:
	import dataflow.dataflow.wireit as wireit

	from dataflow.dataflow import config

	from dataflow.dataflow.calc import run_template, get_plottable
	from dataflow.dataflow.core import Data, Instrument, Template, register_instrument
	from dataflow.dataflow.modules.load import load_module
	from dataflow.dataflow.modules.save import save_module
	from dataflow.reduction.sans.filters import *
	from dataflow.dataflow.SANS.convertq import convertq_module
	from dataflow.dataflow.SANS.correct_detector_efficiency import correct_detector_efficiency_module
	from dataflow.dataflow.SANS.correct_detector_sensitivity import correct_detector_sensitivity_module
	from dataflow.dataflow.SANS.monitor_normalize import monitor_normalize_module
	from dataflow.dataflow.SANS.correct_background import correct_background_module
	from dataflow.dataflow.SANS.generate_transmission import generate_transmission_module
	from dataflow.dataflow.SANS.initial_correction import initial_correction_module
	from dataflow.dataflow.SANS.correct_solid_angle import correct_solid_angle_module
	from dataflow.dataflow.SANS.convert_qxqy import convert_qxqy_module
	from dataflow.dataflow.SANS.annular_av import annular_av_module
	from dataflow.dataflow.SANS.absolute_scaling import absolute_scaling_module
	from dataflow.dataflow.SANS.correct_dead_time import correct_dead_time_module
	from dataflow.apps.tracks.models import File


#Transmissions
Tsamm = 0
Tempp = 0
#Qx,Qy
qx = {}
qy = {}
correctVer = SansData()
#List of Files
fileList = []

# Datatype
SANS_DATA = 'data2d.sans'
data2d = Data(SANS_DATA, SansData)
data1d = Data(SANS_DATA, plot1D)
datadiv = Data(SANS_DATA, div)
#Datatype(id=SANS_DATA,
                  #name='SANS Data',
                  #plot='sansplot')
#dictionary = Datatype(id='dictionary', 
                        #name = 'dictionary',
                        #plot = None)
 
# Load module
def load_action(files=[], intent='', **kwargs):
    print "loading", files
    result = [_load_data(f) for f in files]  # not bundles
    print "Result: ", result
    return dict(output=result)
def _load_data(name):
    print name
    friendly_name = File.objects.get(name=name.split('/')[-1]).friendly_name
    if os.path.splitext(friendly_name)[1] == ".DIV":
        return read_div(myfilestr=name)
    else:
        return read_sample(myfilestr=name)
    
load = load_module(id='sans.load', datatype=SANS_DATA, version='1.0', action=load_action)


# Save module
def save_action(input=[], ext='', **kwargs):
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
def correct_dead_time_action(sample_in, empty_cell_in, empty_in, blocked_in, deadtimeConstant=3.4e-6 , **kwargs):
    lis = [sample_in[0], empty_cell_in[0], empty_in[0], blocked_in[0]] 
    print "List: ", lis
    #Enter DeadTime parameter eventually
    solidangle = [correct_solid_angle(f) for f in lis]
    det_eff = [correct_detector_efficiency(f) for f in solidangle]
    deadtime = [correct_dead_time(f, deadtimeConstant) for f in det_eff]
    result = deadtime
    return dict(sample_out=[result[0]], empty_cell_out=[result[1]], empty_out=[result[2]], blocked_out=[result[3]])
deadtime = correct_dead_time_module(id='sans.correct_dead_time', datatype=SANS_DATA, version='1.0', action=correct_dead_time_action)

def generate_transmission_action(sample_in, empty_cell_in, empty_in, Tsam_in, Temp_in, monitorNormalize=1e8, bottomLeftCoord={}, topRightCoord={}, **kwargs):
    coord_left = (bottomLeftCoord['X'], bottomLeftCoord['Y'])
    coord_right = (topRightCoord['X'], topRightCoord['Y'])
    lis = [sample_in[0], empty_cell_in[0], empty_in[0], Tsam_in[0], Temp_in[0]] 
    print "Lis: ", lis
    #Enter Normalization Parameter eventually
    norm = [monitor_normalize(f,monitorNormalize) for f in lis]
    
    Tsam = generate_transmission(norm[3], norm[2], coord_left, coord_right)
    Temp = generate_transmission(norm[4], norm[2], coord_left, coord_right)
    #tran = Transmission(Tsam, Temp)

    
    print 'Sample transmission= {0} (IGOR Value = 0.724): '.format(Tsam)
    print 'Empty Cell transmission= {0} (IGOR Value = 0.929): '.format(Temp)
    result = norm
    sam = result[0]
    sam.Tsam = Tsam
    sam.Temp = Temp
    print "Tsam:", sam.Tsam
    return dict(sample_out=[sam], empty_cell_out=[result[1]])#,=[result[3]])
generate_trans = generate_transmission_module(id='sans.generate_transmission', datatype=SANS_DATA, version='1.0', action=generate_transmission_action)        
def initial_correction_action(sample, empty_cell, blocked, **kwargs):
    print type(sample)
    lis = [sample[0], empty_cell[0], blocked[0]]
    SAM = lis[0]
    EMP = lis[1]
    BGD = lis[2]
    print "Tsam:", SAM.Tsam
    CORR = initial_correction(SAM, BGD, EMP, SAM.Tsam / SAM.Temp)
    CORR.Tsam = SAM.Tsam
    result = CORR
    return dict(COR=[result])
initial_corr = initial_correction_module(id='sans.initial_correction', datatype=SANS_DATA, version='1.0', action=initial_correction_action)

def correct_detector_sensitivity_action(COR, DIV_in, **kwargs):
    lis = [COR[0], DIV_in[0]]
    print "####################DIV#############"
    print lis[1]
    CORRECT = lis[0]
    sensitivity = lis[-1]
    DIVV = correct_detector_sensitivity(CORRECT, sensitivity)
    DIVV.Tsam = COR[0].Tsam
    result = DIVV
    return dict(DIV_out=[result])
correct_det_sens = correct_detector_sensitivity_module(id='sans.correct_detector_sensitivity', datatype=SANS_DATA, version='1.0', action=correct_detector_sensitivity_action)
def convert_qxqy_action():
    global correctVer, qx, qy
    correctVer, qx, qy = convert_qxqy(correctVer)
    print "Convertqxqy"

def absolute_scaling_action(DIV, empty, sensitivity, ins_name='', **kwargs):
    #sample,empty,DIV,Tsam,instrument
    lis = [DIV[0], empty[0], sensitivity[0]]
    global qx,qy
    sensitivity = lis[-1]
    EMP = lis[1]
    DIV = lis[0]
    ABS = absolute_scaling(DIV, EMP, sensitivity, DIV.Tsam, ins_name)
    
    correct = convert_q(ABS)
    correct, qx, qy = convert_qxqy(correct)
    result = [correct]
   
    return dict(ABS=result)
absolute = absolute_scaling_module(id='sans.absolute_scaling', datatype=SANS_DATA, version='1.0', action=absolute_scaling_action)
def annular_av_action(ABS, **kwargs):
    AVG = annular_av(ABS[0])
    result = [AVG]
    print "Done Red"
    return dict(OneD=result)
annul_av = annular_av_module(id='sans.annular_av', datatype=SANS_DATA, version='1.0', action=annular_av_action)
def correct_background_action(input=None, **kwargs):
    result = [correct_background(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_back = correct_background_module(id='sans.correct_background', datatype=SANS_DATA, version='1.0', action=correct_background_action)

#Instrument definitions
SANS_INS = Instrument(id='ncnr.sans.ins',
                 name='NCNR SANS INS',
                 archive=config.NCNR_DATA + '/sansins',
                 menu=[('Input', [load, save]),
                       ('Reduction', [deadtime, generate_trans, correct_det_sens, initial_corr, annul_av, absolute]),
                                              ],
                 requires=[config.JSCRIPT + '/sansplot.js'],
                 datatypes=[data2d],
                 )
instruments = [SANS_INS]
for instrument in instruments:
    register_instrument(instrument)

# Testing
if __name__ == '__main__':
#def TESTING():
    #global fileList
    fileList = [map_files('sample_4m'), map_files('empty_cell_4m'), map_files('empty_4m'), map_files('trans_sample_4m'), map_files('trans_empty_cell_4m'), map_files('blocked_4m'), map_files('div')]
    #fileList = ["/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC010.SA3_SRK_S110","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC008.SA3_SRK_S108","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC002.SA3_SRK_S102","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC006.SA3_SRK_S106","/home/elakian/dataflow/reduction/sans/ncnr_sample_data/SILIC005.SA3_SRK_S105"]
    for instrument in instruments:
        register_instrument(instrument)
	
    modules = [
        #Sample 0
           #files hard coded for now
        dict(module="sans.load", position=(5, 20),
             config={'files': [fileList[0]], 'intent': 'signal'}),
        #Empty Cell 1
        dict(module="sans.load", position=(5, 50),
             config={'files': [fileList[1]], 'intent': 'signal'}),
        #Empty 2
        dict(module="sans.load", position=(5, 80),
             config={'files': [fileList[2]], 'intent': 'signal'}),
        #Blocked 3
        dict(module="sans.load", position=(5, 110),
             config={'files': [fileList[5]], 'intent': 'signal'}),
        #4 
        dict(module="sans.correct_dead_time", position=(250 , 10), config={'deadtimeConstant':3.4e-6}),
        
        #Tsam 5
        dict(module="sans.load", position=(5, 200),
             config={'files': [fileList[3]], 'intent': 'signal'}),
        #Temp 6
        dict(module="sans.load", position=(5, 230),
             config={'files': [fileList[4]], 'intent': 'signal'}),
        #7
        dict(module="sans.generate_transmission", position=(400 , 10), config={'monitorNormalize':1e8, 'bottomLeftCoord':{'X':55, 'Y':53}, 'topRightCoord':{'X':74, 'Y':72}}),
        #8
        dict(module="sans.save", position=(660, 660), config={'ext': 'dat'}),
        #9
        dict(module="sans.initial_correction", position=(480 , 100), config={}),
        
        #DIV 10
        dict(module="sans.load", position=(5, 300),
             config={'files': [fileList[-1]], 'intent': 'signal'}),
        
        #11
        dict(module="sans.correct_detector_sensitivity", position=(540 , 200), config={}),
        ##EMP 12
        #dict(module="sans.load", position=(100, 300),
             #config={'files': [fileList[2]], 'intent': 'signal'}),
        #12
        dict(module="sans.absolute_scaling", position=(580 , 300), config={'ins_name':'NG3'}),
        #13
        dict(module="sans.annular_av", position=(610 , 400), config={}),
        
        #dict(module="sans.correct_background", position=(360 , 60), config={}),
        
        ]
    wires = [
        #Deadtime (includes solid angle and detector eff)
        dict(source=[0, 'output'], target=[4, 'sample_in']),
        dict(source=[1, 'output'], target=[4, 'empty_cell_in']),
        dict(source=[2, 'output'], target=[4, 'empty_in']),
        dict(source=[3, 'output'], target=[4, 'blocked_in']),
        #Generate Trans (include monitor normalization)
        dict(source=[4, 'sample_out'], target=[7, 'sample_in']),
        dict(source=[4, 'empty_cell_out'], target=[7, 'empty_cell_in']),
        dict(source=[4, 'empty_out'], target=[7, 'empty_in']),
        dict(source=[5, 'output'], target=[7, 'Tsam_in']),
        dict(source=[6, 'output'], target=[7, 'Temp_in']),
        #Initial Correction
        dict(source=[7, 'sample_out'], target=[9, 'sample']),
        dict(source=[7, 'empty_cell_out'], target=[9, 'empty_cell']),
        dict(source=[4, 'blocked_out'], target=[9, 'blocked']),
       # dict(source=[7, 'trans'], target=[9, 'trans']),
        
        #DIV Correction
        dict(source=[9, 'COR'], target=[11, 'COR']),
        dict(source=[10, 'output'], target=[11, 'DIV_in']),
        #dict(source =[11,'DIV'],target = [8,'input']),
        ###ABS Scaling
        dict(source=[11, 'DIV_out'], target=[12, 'DIV']),
        dict(source=[2, 'output'], target=[12, 'empty']),
        dict(source=[10, 'output'], target=[12, 'sensitivity']),
        #Annular Average
        dict(source=[12, 'ABS'], target=[13, 'ABS']),
        dict(source=[13, 'OneD'], target=[8, 'input']),
        
        
        #dict(source =[9,'COR'],target = [8,'input']),
        #dict(source=[2, 'output'], target=[3, 'input']),
        #dict(source=[3, 'output'], target=[4, 'input']),
        #dict(source=[4, 'output'], target=[5, 'input']),
        #dict(source=[5, 'output'], target=[1, 'input']),

        
        #dict(source =[11,'DIV'],target = [8,'input']),
        ]
    config = dict((n, d['config']) for (n, d) in enumerate(modules))
    template = Template(name='test sans',
                        description='example sans data',
                        modules=modules,
                        wires=wires,
                        instrument=SANS_INS.id,
                        )
    #f = open("/home/elakian/tem.txt","w")
    #f.write("Template: ")
    #f.write( simplejson.dumps(wireit.template_to_wireit_diagram(template)))
    #f.write("\n")
    #f.write("Lang: ")
    #f.write(simplejson.dumps(wireit.instrument_to_wireit_language(SANS_INS))) 
    #f.close()
    print 'TEMPLATE', simplejson.dumps(wireit.template_to_wireit_diagram(template))
    #print 'RAW_INSTRUMENT: ', wireit.instrument_to_wireit_language(SANS_INS)
    print 'LANGUAGE', simplejson.dumps(wireit.instrument_to_wireit_language(SANS_INS))                

    run_template(template, config)
    #get_plottable(template,config,14,'OneD')
    #result = get_plottable(template, config, 14, 'OneD')
    
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
