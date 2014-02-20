"""
Offspecular reflectometry reduction modules
"""
import os, sys, pickle, types
import json
#try: from collections import OrderedDict
#except ImportError: from dataflow.ordered_dict import OrderedDict

from reduction.offspecular import filters
from reduction.offspecular.FilterableMetaArray import FilterableMetaArray

from .. import config
#from ..wireit import template_to_wireit_diagram, instrument_to_wireit_language
from ..modules.load import load_module
from ..core import Instrument, Template, register_instrument
from ..wireit import template_to_wireit_diagram, instrument_to_wireit_language
from .modules.load import load
from .modules.save import save
#from .modules.load_asterix import load_asterix
from .modules.load_asterix_spectrum import load_asterix_spectrum
from .modules.normalize_to_monitor import normalize_to_monitor
from .modules.asterix_correct_spectrum import asterix_correct_spectrum
from .modules.combine import combine
from .modules.subtract import subtract
from .modules.autogrid import autogrid
from .modules.offset import offset
from .modules.wiggle import wiggle
from .modules.smooth import smooth
from .modules.tof_lambda import tof_lambda
from .modules.shift_data import shift_data
from .modules.pixels_two_theta import pixels_two_theta
from .modules.asterix_pixels_two_theta import asterix_pixels_two_theta
from .modules.theta_two_theta_qxqz import theta_two_theta_qxqz
from .modules.twotheta_q import twotheta_q
from .modules.two_theta_lambda_qxqz import two_theta_lambda_qxqz
from .modules.load_he3_analyzer_collection import load_he3
from .modules.append_polarization_matrix import append_polarization_matrix
from .modules.combine_polarized import combine_polarized
from .modules.polarization_correct import polarization_correct
from .modules.timestamps import timestamp
from .modules.load_timestamps import load_timestamp
from .modules.empty_qxqz_grid import empty_qxqz_grid
from .modules.mask_data import mask_data
from .modules.slice_data import slice_data
from .modules.collapse_data import collapse_data

from .datatypes import data2d, datahe3, datastamp


# ======== Polarization modules ===========

#Instrument definitions
OSPEC = Instrument(id='ncnr.ospec',
                 name='ospec',
                 menu=[('Input', [load, load_he3, load_timestamp, save]),
                       ('Reduction', [autogrid, combine, subtract, offset, wiggle, smooth, pixels_two_theta, theta_two_theta_qxqz, twotheta_q, empty_qxqz_grid, mask_data, slice_data, collapse_data, normalize_to_monitor]),
                       ('Polarization reduction', [timestamp, append_polarization_matrix, combine_polarized, polarization_correct]),
                       ],
                 requires=[config.JSCRIPT + '/ospecplot.js'],
                 datatypes=[data2d, datahe3, datastamp],
                 )

ASTERIX = Instrument(id='lansce.ospec.asterix',
                 name='asterix',
                 menu=[('Input', [load, load_asterix_spectrum, save]),
                       ('Reduction', [autogrid, combine, offset, shift_data, tof_lambda, asterix_pixels_two_theta, two_theta_lambda_qxqz, mask_data, collapse_data, slice_data, normalize_to_monitor, asterix_correct_spectrum]),
                       ('Polarization reduction', [polarization_correct]),
                       ],
                 requires=[],
                 datatypes=[data2d],
                 )
                 
for instrument in [OSPEC, ASTERIX]:
    register_instrument(instrument)


# ======= example diagrams ========
def nonpolarized_sample():
    from os.path import join, dirname

    ROOT = join(dirname(dirname(dirname(__file__))),'sampledata','ANDR','sabc')
    files = [join(ROOT,'Isabc2%03d.cg1'%i) for i in range(1, 13)]
    modules = [
        dict(module="ospec.load", position=(50, 50),
             config={'files': files, 'intent': 'signal'}),
        dict(module="ospec.save", position=(650, 350), config={'ext': 'dat'}),
        dict(module="ospec.combine", position=(452, 390), config={}),
        dict(module="ospec.offset", position=(321, 171), config={'offsets':{'theta':0, 'xpixel':10}}),
        dict(module="ospec.wiggle", position=(204, 92), config={}),
        dict(module="ospec.twotheta", position=(450, 250), config={}),
        dict(module="ospec.th_tth_qxqz", position=(560, 392), config={}),
        dict(module="ospec.grid", position=(350, 390), config={}),
        dict(module="ospec.emptyqxqz", position=(350, 470), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[5, 'input']),
        dict(source=[5, 'output'], target=[2, 'input_data']),
        dict(source=[5, 'output'], target=[7, 'input']),
        dict(source=[7, 'output'], target=[2, 'input_grid']),
        dict(source=[2, 'output'], target=[6, 'input']),
        dict(source=[8, 'output'], target=[6, 'output_grid']),
        dict(source=[6, 'output'], target=[1, 'input']),
    ]
    config = dict((n, d['config']) for (n, d) in enumerate(modules))
    template = Template(name='test ospec',
                        description='nonpolarized ospec example',
                        modules=modules,
                        wires=wires,
                        instrument=ANDR.id,
                        )
    return template, config

def polarized_sample():
    from os.path import join, split, dirname
    ROOT = join(dirname(dirname(dirname(__file__))),'sampledata','ANDR','cshape_121609')
    path, ext = os.path.join(ROOT,'Iremun00'), ['.ca1', '.cb1']
    files = [path + str(i + 1) + extension for i in range(0, 9) for extension in ext if i != 2]
    pols = json.load(open(join(ROOT, 'file_catalog.json'), 'r'))
    pol_states = dict((split(file)[-1], pols[split(file)[-1]]['polarization']) for file in files)
    modules = [
        dict(module="ospec.load", position=(50, 25),
             config={'files': files, 'intent': 'signal', 'PolStates':pol_states}),
        dict(module="ospec.timestamp", position=(100, 125), config={}),
        dict(module="ospec.loadhe3", position=(50, 375), config={'files':[join(ROOT,'He3Cells.json')]}),
        dict(module="ospec.save", position=(700, 175), config={'ext': 'dat'}),
        dict(module="ospec.comb_polar", position=(450, 180), config={}),
        dict(module="ospec.append", position=(300, 225), config={}),
        dict(module="ospec.corr_polar", position=(570, 125), config={}),
        dict(module="ospec.grid", position=(350, 375), config={}),
        dict(module="ospec.loadstamp", position=(50, 250), config={'files':[join(ROOT, 'end_times.json')]}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[1, 'input']),
        dict(source=[8, 'output'], target=[1, 'stamps']),
        dict(source=[1, 'output'], target=[5, 'input']),
        dict(source=[2, 'output'], target=[5, 'he3cell']),
        dict(source=[5, 'output'], target=[4, 'input']),
        dict(source=[5, 'output'], target=[7, 'input']),
        dict(source=[7, 'output'], target=[4, 'grid']),
        dict(source=[4, 'output'], target=[6, 'input']),
        dict(source=[6, 'output'], target=[3, 'input']),
    ]
    config = dict((n, d['config']) for (n, d) in enumerate(modules))
    template = Template(name='test ospec',
                        description='polarized ospec example',
                        modules=modules,
                        wires=wires,
                        instrument=ANDR.id,
                        )
    return template,config


def test():
    from ..calc import verify_examples
    tests = [
        # TODO: enable offspecular tests
        #('pol.out', polarized_sample()),
        #('nonpol.out', nonpolarized_sample()),
    ]
    verify_examples(__file__, tests, 'test/dataflow_results')

def demo():
    #import logging; logging.basicConfig(level=logging.DEBUG)
    from ..calc import run_example
    #from .. import wireit
    #print 'language', json.dumps(wireit.instrument_to_wireit_language(TAS), indent=2)
    run_example(*polarized_sample(), verbose=False)

if __name__ == "__main__":
    demo()
