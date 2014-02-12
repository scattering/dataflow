"""
SANS reduction modules
"""
import os
from django.utils import simplejson as json

#from reduction.sans.filters import SansData
#from reduction.sans.filters import plot1D
#from reduction.sans.filters import div
import reduction.sans.filters as red

from .. import wireit
from .. import config
from ..core import Data, Instrument, Template, register_instrument
from ..modules.load import load_module
from ..modules.save import save_module
from .correct_detector_sensitivity import correct_detector_sensitivity_module
from .correct_background import correct_background_module
from .generate_transmission import generate_transmission_module
from .initial_correction import initial_correction_module
from .annular_av import annular_av_module
from .absolute_scaling import absolute_scaling_module
from .correct_dead_time import correct_dead_time_module
#from .convertq import convertq_module
#from .monitor_normalize import monitor_normalize_module
#from .correct_solid_angle import correct_solid_angle_module
#from .convert_qxqy import convert_qxqy_module


#Transmissions
Tsamm = 0
Tempp = 0
#Qx,Qy
qx = {}
qy = {}
correctVer = red.SansData()
#List of Files
fileList = []

# Datatype
SANS_DATA = 'data2d.sans'
data2d = Data(SANS_DATA, red.SansData)
data1d = Data(SANS_DATA, red.plot1D)
datadiv = Data(SANS_DATA, red.div)
#Datatype(id=SANS_DATA,
                  #name='SANS Data',
                  #plot='sansplot')
#dictionary = Datatype(id='dictionary', 
                        #name = 'dictionary',
                        #plot = None)

xtype="AutosizeImageContainer"

# Load module
def load_action(files=[], intent='', **kwargs):
    print "loading", files
    result = [_load_data(f) for f in files]  # not bundles
    print "Result: ", result
    return dict(output=result)
def _load_data(name):
    from apps.tracks.models import File
    print name
    friendly_name = File.objects.get(name=name.split('/')[-1]).friendly_name
    if os.path.splitext(friendly_name)[1] == ".DIV":
        return red.read_div(myfilestr=name)
    else:
        return red.read_sample(myfilestr=name)
load = load_module(id='sans.load', datatype=SANS_DATA, version='1.0',
                   action=load_action)


# Save module
def save_action(input=[], ext='', **kwargs):
    for f in input: _save_one(f, ext) # not bundles
    return {}
def _save_one(input, ext):
    outname = initname = red.map_files('save')
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", initname, 'as', outname
    with open(outname, 'w') as f:
        f.write(str(input.__str__()))
save = save_module(id='sans.save', datatype=SANS_DATA,
                   version='1.0', action=save_action, xtype="SaveContainer")


# Modules
def correct_dead_time_action(sample_in, empty_cell_in, empty_in, blocked_in,
                             deadtimeConstant=3.4e-6, **kwargs):
    deadtimeConstant = float(deadtimeConstant)
    lis = [sample_in[0], empty_cell_in[0], empty_in[0], blocked_in[0]]
    print "List: ", lis
    #Enter DeadTime parameter eventually
    solidangle = [red.correct_solid_angle(f) for f in lis]
    det_eff = [red.correct_detector_efficiency(f) for f in solidangle]
    deadtime = [red.correct_dead_time(f, deadtimeConstant) for f in det_eff]
    result = deadtime
    return dict(sample_out=[result[0]], empty_cell_out=[result[1]],
                empty_out=[result[2]], blocked_out=[result[3]])


deadtime = correct_dead_time_module(id='sans.correct_dead_time',
                                    datatype=SANS_DATA, version='1.0',
                                    action=correct_dead_time_action,
                                    xtype=xtype)


def generate_transmission_action(sample_in, empty_cell_in, empty_in, Tsam_in,
                                 Temp_in, monitorNormalize=1e8,
                                 bottomLeftCoord={}, topRightCoord={},
                                 **kwargs):
    coord_left = (int(bottomLeftCoord['X']), int(bottomLeftCoord['Y']))
    coord_right = (int(topRightCoord['X']), int(topRightCoord['Y']))
    monitorNormalize = float(monitorNormalize)
    lis = [sample_in[0], empty_cell_in[0], empty_in[0], Tsam_in[0], Temp_in[0]] 
    print "Lis: ", lis
    norm = [red.monitor_normalize(f,monitorNormalize) for f in lis]
    
    Tsam = red.generate_transmission(norm[3], norm[2], coord_left, coord_right)
    Temp = red.generate_transmission(norm[4], norm[2], coord_left, coord_right)
    #tran = Transmission(Tsam, Temp)

    
    print 'Sample transmission= {0} (IGOR Value = 0.724): '.format(Tsam)
    print 'Empty Cell transmission= {0} (IGOR Value = 0.929): '.format(Temp)
    result = norm
    sam = result[0]
    sam.Tsam = Tsam
    sam.Temp = Temp
    return dict(sample_out=[sam], empty_cell_out=[result[1]])#,=[result[3]])
generate_trans = generate_transmission_module(id='sans.generate_transmission',
                                              datatype=SANS_DATA, version='1.0',
                                              action=generate_transmission_action,
                                              xtype=xtype,
                                              filterModule=red.generate_transmission)

def initial_correction_action(sample, empty_cell, blocked, **kwargs):
    print type(sample)
    lis = [sample[0], empty_cell[0], blocked[0]]
    SAM = lis[0]
    EMP = lis[1]
    BGD = lis[2]
    CORR = red.initial_correction(SAM, BGD, EMP, SAM.Tsam / SAM.Temp)
    CORR.Tsam = SAM.Tsam
    result = CORR
    return dict(COR=[result])
initial_corr = initial_correction_module(id='sans.initial_correction',
                                         datatype=SANS_DATA, version='1.0',
                                         action=initial_correction_action,
                                         xtype=xtype,
                                         filterModule=red.initial_correction)


def correct_detector_sensitivity_action(COR, DIV_in, **kwargs):
    lis = [COR[0], DIV_in[0]]
    print "####################DIV#############"
    print lis[1]
    CORRECT = lis[0]
    sensitivity = lis[-1]
    DIVV = red.correct_detector_sensitivity(CORRECT, sensitivity)
    DIVV.Tsam = COR[0].Tsam
    result = DIVV
    return dict(DIV_out=[result])
correct_det_sens = correct_detector_sensitivity_module(
    id='sans.correct_detector_sensitivity', datatype=SANS_DATA, version='1.0',
    action=correct_detector_sensitivity_action, xtype=xtype,
    filterModule=red.correct_detector_sensitivity)


def convert_qxqy_action():
    global correctVer, qx, qy
    correctVer, qx, qy = red.convert_qxqy(correctVer)
    print "Convertqxqy"


def absolute_scaling_action(DIV, empty, sensitivity, ins_name='',
                            bottomLeftCoord={}, topRightCoord={}, **kwargs):
    #sample,empty,DIV,Tsam,instrument
    coord_left = (int(bottomLeftCoord['X']), int(bottomLeftCoord['Y']))
    coord_right = (int(topRightCoord['X']),  int(topRightCoord['Y']))
    lis = [DIV[0], empty[0], sensitivity[0]]
    
    sensitivity = lis[-1]
    EMP = lis[1]
    DIV = lis[0]
    ABS = red.absolute_scaling(DIV, EMP, sensitivity, DIV.Tsam, ins_name,coord_left,coord_right)
    return dict(ABS=[ABS])
absolute = absolute_scaling_module(id='sans.absolute_scaling',
                                   datatype=SANS_DATA, version='1.0',
                                   action=absolute_scaling_action, xtype=xtype,
                                   filterModule=red.absolute_scaling)

def annular_av_action(ABS, **kwargs):
    correct = red.convert_q(ABS[0])
    AVG = red.annular_av(correct)
    result = [AVG]
    print "Done Red"
    return dict(OneD=result)
annul_av = annular_av_module(id='sans.annular_av', datatype=SANS_DATA,
                             version='1.0', action=annular_av_action,
                             xtype=xtype, filterModule=red.annular_av)

def correct_background_action(input=None, **kwargs):
    result = [red.correct_background(bundle[-1], bundle[0]) for bundle in input]
    return dict(output=result)
correct_back = correct_background_module(id='sans.correct_background',
                                         datatype=SANS_DATA, version='1.0',
                                         action=correct_background_action,
                                         xtype=xtype,
                                         filterModule=red.correct_background)

#Instrument definitions
SANS_NG3 = Instrument(id='ncnr.sans.ins',
                 name='sans',
                 archive=config.NCNR_DATA + '/sansins',
                 menu=[('Input', [load, save]),
                       ('Reduction', [deadtime, generate_trans, correct_det_sens, initial_corr, annul_av, absolute]),
                      ],
                 requires=[config.JSCRIPT + '/sansplot.js'],
                 datatypes=[data2d],
                 )
                 
instruments = [SANS_NG3]
for instrument in instruments:
    register_instrument(instrument)

# Testing
def demo():
    from ..calc import run_template, memory_cache
    #global fileList
    fileList = [red.map_files('sample_4m'), red.map_files('empty_cell_4m'),
                red.map_files('empty_4m'), red.map_files('trans_sample_4m'),
                red.map_files('trans_empty_cell_4m'), red.map_files('blocked_4m'),
                red.map_files('div')]

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
        dict(module="sans.correct_dead_time", position=(344, 8),
             config={'deadtimeConstant': 3.4e-6}),
        
        #Tsam 5
        dict(module="sans.load", position=(5, 200),
             config={'files': [fileList[3]], 'intent': 'signal'}),
        #Temp 6
        dict(module="sans.load", position=(5, 230),
             config={'files': [fileList[4]], 'intent': 'signal'}),
        #7
        dict(module="sans.generate_transmission", position=(584, 4),
             config={'monitorNormalize': 1e8,
                     'bottomLeftCoord': {'X': 55, 'Y': 53},
                     'topRightCoord': {'X': 74, 'Y': 72}}),
        #8
        dict(module="sans.save", position=(660, 660), config={'ext': 'dat'}),
        #9
        dict(module="sans.initial_correction", position=(779 , 45), config={}),
        
        #DIV 10
        dict(module="sans.load", position=(5, 300),
             config={'files': [fileList[-1]], 'intent': 'signal'}),
        
        #11
        dict(module="sans.correct_detector_sensitivity", position=(750 , 161), config={}),
        ##EMP 12
        #dict(module="sans.load", position=(100, 300),
             #config={'files': [fileList[2]], 'intent': 'signal'}),
        #12
        dict(module="sans.absolute_scaling", position=(750, 265),
             config={'ins_name': 'NG3', 'bottomLeftCoord': {'X': 55, 'Y': 53},
                     'topRightCoord': {'X': 74, 'Y': 72}}),
        #13
        dict(module="sans.annular_av", position=(750 , 383), config={}),
        
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
                        instrument=SANS_NG3.id,
                        )
    #f = open("/home/elakian/tem.txt","w")
    #f.write("Template: ")
    #f.write( json.dumps(wireit.template_to_wireit_diagram(template)))
    #f.write("\n")
    #f.write("Lang: ")
    #f.write(json.dumps(wireit.instrument_to_wireit_language(SANS_NG3)))
    #f.close()
    print 'TEMPLATE', json.dumps(wireit.template_to_wireit_diagram(template))
    #print 'RAW_INSTRUMENT: ', wireit.instrument_to_wireit_language(SANS_INS)
    print 'LANGUAGE', json.dumps(wireit.instrument_to_wireit_language(SANS_NG3))

    cache = memory_cache()
    run_template(template, config, cache)
    #get_plottable(template,config,14,'OneD', cache)
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

if __name__ == '__main__':
    demo()
