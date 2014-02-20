"""
SANS reduction modules
"""
import reduction.sans.filters as red

from .. import config
from ..core import Instrument, Template, register_instrument
from .modules.save import save
from .modules.load import load
from .modules.absolute_scaling import absolute_scaling
from .modules.annular_av import annular_av
from .modules.convert_qxqy import convert_qxqy
from .modules.convertq import convertq
from .modules.correct_background import correct_background
#from .modules.correct_background import correct_blocked_beam
from .modules.correct_dead_time import correct_dead_time
from .modules.correct_detector_efficiency import correct_detector_efficiency
from .modules.correct_detector_sensitivity import correct_detector_sensitivity
from .modules.correct_solid_angle import correct_solid_angle
from .modules.generate_transmission import generate_transmission
from .modules.initial_correction import initial_correction
from .modules.monitor_normalize import monitor_normalize

from .datatypes import data2d

reduction = [
    correct_dead_time,
    generate_transmission,
    correct_detector_sensitivity,
    initial_correction,
    annular_av,
    absolute_scaling,

    convertq,
    correct_background,
    monitor_normalize,
    correct_solid_angle,
    convert_qxqy,
    #correct_blocked_beam,
    correct_detector_efficiency,
    ]
#Instrument definitions
SANS = Instrument(id='ncnr.sans',
                 name='sans',
                 menu=[('Input', [load, save]),
                       ('Reduction', reduction),
                      ],
                 requires=[config.JSCRIPT + '/sansplot.js'],
                 datatypes=[data2d],
                 )
                 
instruments = [SANS]
for instrument in instruments:
    register_instrument(instrument)

# Testing
def sans_example():
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

    return template, config

def test():
    from ..calc import verify_examples
    verify_examples(__file__, [('sans.out', sans_example())],'test/dataflow_results')

def demo():
    from ..calc import run_example
    run_example(*sans_example(), verbose=False)

if __name__ == '__main__':
    demo()
