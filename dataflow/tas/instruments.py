"""
Triple Axis Spectrometer reduction and analysis modules
"""
import os, sys
import types

from django.utils import simplejson as json

from reduction.tripleaxis import data_abstraction

from .. import config
from ..core import Instrument, Data, Template, register_instrument
    
from .modules.tas_join import join_module
from .modules.tas_subtract import subtract_module
from ..modules.save import save_module
from ..modules.load import load_module
from .modules.tas_extract import extract_module
from .modules.loadchalk import load_chalk_module
from .modules.tas_normalize_monitor import normalize_monitor_module
from .modules.tas_detailed_balance import detailed_balance_module
from .modules.tas_monitor_correction import monitor_correction_module
from .modules.tas_volume_correction import volume_correction_module

TAS_DATA = 'data1d.tas'
xtype = 'AutosizeImageContainer'
data1d = Data(TAS_DATA, data_abstraction.TripleAxis,
              loaders=[{'function':data_abstraction.autoloader, 'id':'loadTAS'},
                       {'function':data_abstraction.chalk_autoloader, 'id':'loadChalkRiver'}])

# Reduction operations may refer to data from other objects, but may not
# modify it.  Instead of modifying, first copy the data and then work on
# the copy.
#
#def data_join(files, align):
    ## Join code: belongs in reduction.tripleaxis
    ##if align != 'x': raise TypeError("Can only align on x for now")
    #align = 'x' # Ignore align field for now since our data only has x,y,dy
    #new = {}
    ##print "files"; pprint(files)
    #for f in files:
        #for x, y, dy, mon in zip(f['x'], f['y'], f['dy'], f['monitor']):
            #if x not in new: new['x'] = (0, 0, 0)
            #Sy, Sdy, Smon = new['x']
            #new[x] = (y + Sy, dy ** 2 + Sdy, mon + Smon)
    #points = []
    #for xi in sorted(new.keys()):
        #Sy, Sdy, Smon = new[xi]
        #points.append((xi, Sy, math.sqrt(Sdy), Smon))
    #x, y, dy, mon = zip(*points)

    #basename = min(f['name'] for f in files)
    #outname = os.path.splitext(basename)[0] + '.join'
    #result = {'name': outname, 'x': x, 'y': y, 'dy': dy, 'monitor': mon}
    #return result



# === Component binding ===
def get_friendly_name(fh):
    from apps.tracks.models import File
    return File.objects.get(name=str(fh)).friendly_name

def _load_data(name):
    #(dirName, fileName) = os.path.split(name)
    #friendlyName = get_friendly_name(fileName)
    return data_abstraction.filereader(name, friendly_name=os.path.basename(name))

def load_action(files=[], intent=None, position=None, xtype=None, **kwargs):
    """ was set up to load ONLY 1 file... might work for bundles now """
    print "loading", files
    result = []
    for i, f in enumerate(files):
        subresult = _load_data(f)
        if type(subresult) == types.ListType:
            result.extend(subresult)
        else:
            result.append(subresult)
    return dict(output=result)
################################################################################
# NOTE: 02/03/2012 bbm
# this is what was in "load_action" before
# it would clearly not work - the directory was hardcoded, 
# and relied on a directory structure
# that will not exist on a typical machine (i.e. /home/brendan...)
#
# the replacement above is an adaptation of the loader code in 
# dataflow.offspecular.instruments
################################################################################

load = load_module(id='tas.load', datatype=TAS_DATA, version='1.0',
                   action=load_action)

'''
def _load_chalk_data(aof_filename, orient1, orient2, acf_filename=None):
    #(dirName, fileName) = os.path.split(name)
    #friendlyName = get_friendly_name(fileName)
    
    return data_abstraction.chalk_filereader(aof_filename, orient1, orient2, acf_filename=acf_filename)

def load_chalk_action(chalk_files=[], h1=None, k1=None, l1=None, h2=None, k2=None, l2=None, **kwargs):

    print "loading chalk river"
    result = []
    orient1 = []
    orient2 = []
    aof_filename = None
    aof_file = None
    acf_filename = None
    acf_file = None
    log_filename = None
    log_file = None
    
    try:
        h1 = kwargs['fields']['h1']['value']
        k1 = kwargs['fields']['k1']['value']
        l1 = kwargs['fields']['l1']['value']
        h2 = kwargs['fields']['h2']['value']
        k2 = kwargs['fields']['k2']['value']
        l2 = kwargs['fields']['l2']['value']
        orient1 = [h1, k1, l1]
        orient2 = [h2, k2, l2]
    except:
        #TODO Throw error! orient1 and orient2 MUST be given!
        pass
    # The .AOF file may be linked with a .ACF file and a .LOG file.
    # ASSUMPTION: the filename of these files are the same!!!
    # The first .AOF, .ACF, or .LOG found will determine this shared filename.
    for i, f in enumerate(chalk_files):
        if aof_filename and acf_filename and log_filename:
            #if the datafiles were already found, break loop
            break
        
        fileName, fileExt = os.path.splitext(f) # capitalization matters for the filename!
        fileExt = fileExt.lower()
        if not aof_filename and fileExt == '.aof':
            
            if (not acf_filename and not log_filename) or \
               (acf_filename and acf_filename == fileName) or \
               (log_filename and log_filename == fileName):
                aof_filename = fileName 
                aof_file = f
                
        elif not acf_filename and fileExt == '.acf':
            
            if (not aof_filename and not log_filename) or \
               (aof_filename and aof_filename == fileName) or \
               (log_filename and log_filename == fileName):            
                acf_filename = fileName
                acf_file = f
                
        elif not log_filename and fileExt == '.log':
            
            if (not aof_filename and not acf_filename) or \
               (aof_filename and aof_filename == fileName) or \
               (acf_filename and acf_filename == fileName):                
                log_filename = fileName
                log_file = f
            
    
    #improve reader so it will include .log files!
    #result should be a list of TripleAxis objects
    result = _load_chalk_data(aof_file, orient1, orient2, acf_filename=acf_file)

    return dict(output=result)

loadchalk = load_chalk_module(id='tas.loadchalk', datatype=TAS_DATA,
                   version='1.0', action=load_chalk_action,)


def extract_action(input, data_objects=[], **kwargs):
    """ isolates/extracts the given list of objects """
    print "extracting", data_objects
    
    return dict(output=data_objects)


extract = extract_module(id='tas.extract', datatype=TAS_DATA,
                   version='1.0', action=extract_action, fields=None)
'''


def save_action(input, ext=None, xtype=None, position=None, **kwargs):
    # Note that save does not accept inputs from multiple components, so
    # we only need to deal with the bundle, not the list of bundles.
    # This is specified by terminal['multiple'] = False in modules/save.py
    for f in input: _save_one(f, ext)
    return {}

def _save_one(input, ext):
    #TODO - make a real save... this is a dummy
    outname = input.meta_data.filename
    # TODO: if ext is None, then infile will be overwritten
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", input.meta_data.filename, 'as', outname
    #save_data(input, name=outname)
    
fields = {'ext': {
    "type":"string",
    "label": "Save extension",
    "name": "ext",
    "value": ""
    }
}
save = save_module(id='tas.save', datatype=TAS_DATA,
                   version='1.0', action=save_action,
                   fields=fields)
save.xtype = 'SaveContainer'
    
def join_action(input, xaxis='', yaxis='', num_bins=0, xstep=None, ystep=None, **kwargs):
    # This is confusing because load returns a bundle and join, which can
    # link to multiple loads, has a list of bundles.  So flatten this list.
    # The confusion between bundles and items will bother us continuously,
    # and it is probably best if every filter just operates on and returns
    # bundles, which I do in this example.

    print "JOINING"
    try:
        xaxis = kwargs['fields']['xaxis']['value']
        yaxis = kwargs['fields']['yaxis']['value']
        num_bins = kwargs['fields']['num_bins']['value']
        xstep = kwargs['fields']['xstep']['value']
        ystep = kwargs['fields']['ystep']['value']
    except:
        pass
    #for now, we will work on joining arbitrary inputs instead of two at a time...
    #This will hopefully work on bundles, instead of doing things pairwise...
    joinedtas = data_abstraction.join(input)

    joinedtas.xaxis = xaxis
    joinedtas.yaxis = yaxis
    joinedtas.num_bins = num_bins
    joinedtas.xstep = xstep
    joinedtas.ystep = ystep
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

def subtract_action(signal, background, scan_variable=None, **kwargs):
    print "SUBTRACTING"
    try:
        scan_var = kwargs['fields']['scan_variable']['value']
    except:
        pass
    subtractedtas = data_abstraction.subtract(signal, background, independent_variable=scan_variable)

    # Could always set up x/y axes here based on the independent variable
    
    return dict(output=[subtractedtas])


subtract = subtract_module(id='tas.subtract', datatype=TAS_DATA, version='1.0', 
                   action=subtract_action, xtype=xtype, filterModule=data_abstraction.subtract)


#All TripleAxis reductions below require that:
#  'input' be a TripleAxis object (see data_abstraction.py)

def detailed_balance_action(input, **kwargs):
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.detailed_balance()
    return dict(output=input)

def normalize_monitor_action(input, target_monitor=None, **kwargs):
    #Requires the target monitor value
    data_abstraction.normalize_monitor(input, target_monitor)
    return dict(output=input)


def monitor_correction_action(input, instrument_name, **kwargs):
    #Requires instrument name, e.g. 'BT7'.  
    #Check monitor_correction_coordinates.txt for available instruments
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.harmonic_monitor_correction(instrument_name)
    return dict(ouput=input)

def volume_correction_action(input, **kwargs):
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.resolution_volume_correction()
    return dict(output=input)



normalizemonitor = normalize_monitor_module(id='tas.normalize_monitor', datatype=TAS_DATA,
                                            version='1.0', action=normalize_monitor_action, xtype=xtype, 
                                            filterModule=data_abstraction.TripleAxis.normalize_monitor)

detailedbalance = detailed_balance_module(id='tas.detailed_balance', datatype=TAS_DATA,
                                          version='1.0', action=detailed_balance_action, xtype=xtype, 
                                            filterModule=data_abstraction.TripleAxis.detailed_balance)

monitorcorrection = monitor_correction_module(id='tas.monitor_correction', datatype=TAS_DATA,
                                              version='1.0', action=monitor_correction_action, xtype=xtype, 
                                            filterModule=data_abstraction.TripleAxis.harmonic_monitor_correction)

volumecorrection = volume_correction_module(id='tas.volume_correction', datatype=TAS_DATA,
                                            version='1.0', action=volume_correction_action, xtype=xtype, 
                                            filterModule=data_abstraction.TripleAxis.resolution_volume_correction)


# ==== Instrument definitions ====
TAS = Instrument(id='ncnr.tas',
                 name='tas',
                 archive=config.NCNR_DATA + '/tas',
                 menu=[('Input', [load, save]),
                       ('Reduction', [join, subtract, normalizemonitor, detailedbalance,
                                      monitorcorrection, volumecorrection])
                       ],
                 #requires=[config.JSCRIPT + '/tasplot.js'],
                 datatypes=[data1d],
                 )

# Register the list of triple axis instruments
for instrument in [TAS]:
        register_instrument(instrument)


# ==== Example reductions ====
def bt7_example():
    import reduction.tripleaxis
    DATA_ROOT = os.path.dirname(reduction.tripleaxis.__file__)
    modules = [
        dict(module="tas.load", position=(10, 150), config={'files':[os.path.join(DATA_ROOT,'EscanQQ7HorNSF91831.bt7')]}),
        dict(module="tas.normalize_monitor", position=(270, 20), config={'target_monitor': 165000}),
        dict(module="tas.detailed_balance", position=(270, 120), config={}),
        dict(module="tas.monitor_correction", position=(270, 220), config={'instrument_name':'BT7'}),
        dict(module="tas.volume_correction", position=(270, 320), config={}),
        dict(module="tas.save", position=(500, 150), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[1, 'input']),
        #dict(source=[1, 'output'], target=[5, 'input']),
        
        dict(source=[0, 'output'], target=[2, 'input']),
        #dict(source=[2, 'output'], target=[5, 'input']),
        
        dict(source=[0, 'output'], target=[3, 'input']),
        #dict(source=[3, 'output'], target=[5, 'input']),
        
        dict(source=[0, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
    ]
    config = {}
    
    template = Template(name='test reduction presentation',
                        description='example reduction diagram',
                        modules=modules,
                        wires=wires,
                        instrument=TAS.id,
                        )
    return template, config

def spins_example():
    #for loading spins files 59-71 for plotting
    modules = [
        dict(module="tas.load", position=(10, 40), config={}),
        dict(module="tas.join", position=(250, 40), config={}),
        dict(module="tas.save", position=(400, 40), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[1, 'input']),
        dict(source=[1, 'output'], target=[2, 'input']),
    ]
    config = {}
    
    template = Template(name='test reduction presentation',
                        description='example reduction diagram',
                        modules=modules,
                        wires=wires,
                        instrument=TAS.id,
                        )
    return template, config

def test():
    from ..calc import verify_examples
    tests = [
        ('bt7.out', bt7_example()),
        ('spins.out', spins_example()),
    ]
    verify_examples(__file__, tests)

def demo():
    from .. import wireit
    from ..calc import run_example
    print 'language', json.dumps(wireit.instrument_to_wireit_language(TAS), indent=2)
    run_example(*bt7_example())
    #run_example(*spins_example())

if __name__ == "__main__":
    demo()
