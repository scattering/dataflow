"""
Triple Axis Spectrometer reduction and analysis modules
"""
import math, os, sys, types

if 1:
    from ...reduction.tripleaxis import data_abstraction
    from ..calc import run_template
    from .. import wireit
    from ... import ROOT_URL
    from django.utils import simplejson
    import numpy
    
    from .. import config
    from ..core import Instrument, Data, Template, register_instrument
    
    #from dataflow.dataflow.modules.load import load_module
    from .modules.tas_join import join_module
    from ..modules.save import save_module
    from .modules.tas_load import load_module
    from .modules.tas_normalize_monitor import normalize_monitor_module
    from .modules.tas_detailed_balance import detailed_balance_module
    from .modules.tas_monitor_correction import monitor_correction_module
    from .modules.tas_volume_correction import volume_correction_module
    from ...apps.tracks.models import File


if 0:
    #direct imports for use individually (ie running this file)
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from dataflow.reduction.tripleaxis import data_abstraction
    from dataflow.dataflow.calc import run_template
    from dataflow.dataflow import wireit
    from dataflow import ROOT_URL
    from django.utils import simplejson
    
    import numpy
    from dataflow.dataflow import config
    from dataflow.dataflow.core import Instrument, Data, Template, register_instrument

    from dataflow.dataflow.tas.modules.tas_join import join_module
    from dataflow.dataflow.modules.save import save_module
    from dataflow.dataflow.tas.modules.tas_load import load_module
    from dataflow.dataflow.tas.modules.tas_normalize_monitor import normalize_monitor_module
    from dataflow.dataflow.tas.modules.tas_detailed_balance import detailed_balance_module
    from dataflow.dataflow.tas.modules.tas_monitor_correction import monitor_correction_module
    from dataflow.dataflow.tas.modules.tas_volume_correction import volume_correction_module
    from dataflow.apps.tracks.models import File
    #from dataflow.apps.tracks.models import File

TAS_DATA = 'data1d.tas'
data1d = Data(TAS_DATA, data_abstraction.TripleAxis)
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

def load_action(files=None, intent=None, position=None, xtype=None, **kwargs):
    """Currently set up to load ONLY 1 file"""
    #print "loading", files

    print 'FRIENDLY FILE', File.objects.get(name=files[0].split('/')[-1]).friendly_name
    print "/home/brendan/dataflow/reduction/tripleaxis/spins_data/" + File.objects.get(name=files[0].split('/')[-1]).friendly_name
    result = [data_abstraction.filereader(f, friendly_name="/home/brendan/dataflow/reduction/tripleaxis/spins_data/" + File.objects.get(name=f.split('/')[-1]).friendly_name) for f in files]
    print "done loading"
    return dict(output=result)
    #pass
load = load_module(id='tas.load', datatype=TAS_DATA,
                   version='1.0', action=load_action,)

def save_action(input, ext=None, xtype=None, position=None, **kwargs):
    # Note that save does not accept inputs from multiple components, so
    # we only need to deal with the bundle, not the list of bundles.
    # This is specified by terminal['multiple'] = False in modules/save.py
    for f in input: _save_one(f, ext)
    return {}

def _save_one(input, ext):
    #TODO - make a real save... this is a dummy
    outname = input['name']
    if ext is not None:
        outname = ".".join([os.path.splitext(outname)[0], ext])
    print "saving", input['name'], 'as', outname
    save_data(input, name=outname)
save_ext = {
    "type":"[string]",
    "label": "Save extension",
    "name": "ext",
    "value": "",
}
save = save_module(id='tas.save', datatype=TAS_DATA,
                   version='1.0', action=save_action,
                   fields=[save_ext])
    
def join_action(input, xaxis='', yaxis='', **kwargs):
    # This is confusing because load returns a bundle and join, which can
    # link to multiple loads, has a list of bundles.  So flatten this list.
    # The confusion between bundles and items will bother us continuously,
    # and it is probably best if every filter just operates on and returns
    # bundles, which I do in this example.
    joinedtas = None
    print "JOINING"
    for tas in input:
        if joinedtas == None:
            joinedtas = tas
        else:
            joinedtas = data_abstraction.join(joinedtas, tas)
    joinedtas.xaxis = xaxis
    joinedtas.yaxis = yaxis
    return dict(output=[joinedtas])
xaxis_field = {
        "type":"string",
        "label": "X axis for 2D plotting",
        "name": "xaxis",
        "value": '',
}
yaxis_field = {
        "type":"string",
        "label": "Y axis for 2D plotting",
        "name": "yaxis",
        "value": '',
}
join = join_module(id='tas.join', datatype=TAS_DATA,
                   version='1.0', action=join_action,fields = [xaxis_field,yaxis_field])

#All TripleAxis reductions below require that:
#  'input' be a TripleAxis object (see data_abstraction.py)

def detailed_balance_action(input, **kwargs):
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.detailed_balance()
    return dict(output=input)

def normalize_monitor_action(input, target_monitor, **kwargs):
    #Requires the target monitor value
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.normalize_monitor(target_monitor)
    #result=input[0].get_plottable()
    return dict(output=input)

def monitor_correction_action(input, instrument_name, **kwargs):
    #Requires instrument name, e.g. 'BT7'.  
    #Check monitor_correction_coordinates.txt for available instruments
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.harmonic_monitor_correction()
    return dict(ouput=input)

def volume_correction_action(input, **kwargs):
    for tasinstrument in input:
        tasinstrument.xaxis = ''
        tasinstrument.yaxis = ''
        tasinstrument.resolution_volume_correction()
    return dict(output=input)

normalizemonitor = normalize_monitor_module(id='tas.normalize_monitor', datatype=TAS_DATA,
                                            version='1.0', action=normalize_monitor_action)

detailedbalance = detailed_balance_module(id='tas.detailed_balance', datatype=TAS_DATA,
                                          version='1.0', action=detailed_balance_action)

monitorcorrection = monitor_correction_module(id='tas.monitor_correction', datatype=TAS_DATA,
                                              version='1.0', action=monitor_correction_action)

volumecorrection = volume_correction_module(id='tas.volume_correction', datatype=TAS_DATA,
                                            version='1.0', action=volume_correction_action)


# ==== Instrument definitions ====
BT7 = Instrument(id='ncnr.tas.bt7',
                 name='NCNR BT7',
                 archive=config.NCNR_DATA + '/bt7',
                 menu=[('Input', [load, save]),
                       ('Reduction', [join, normalizemonitor, detailedbalance,
                                      monitorcorrection, volumecorrection])
                       ],
                 #requires=[config.JSCRIPT + '/tasplot.js'],
                 datatypes=[data1d],
                 )


# Return a list of triple axis instruments
if 1:
    instruments = [BT7]
    for instrument in instruments:
        register_instrument(instrument)


if 0:
    modules = [
        dict(module="tas.load", position=(10, 150), config={'files':[ROOT_URL.HOMEDIR[:-12] + 'reduction/tripleaxis/EscanQQ7HorNSF91831.bt7']}),
        dict(module="tas.normalize_monitor", position=(270, 20), config={'target_monitor': 165000}),
        dict(module="tas.detailed_balance", position=(270, 120), config={}),
        dict(module="tas.monitor_correction", position=(270, 220), config={'instrument_name':'BT7'}),
        dict(module="tas.volume_correction", position=(270, 320), config={}),
        dict(module="tas.save", position=(500, 150), config={}),
    ]
    wires = [
        dict(source=[0, 'output'], target=[1, 'input']),
        dict(source=[1, 'output'], target=[5, 'input']),
        
        dict(source=[0, 'output'], target=[2, 'input']),
        dict(source=[2, 'output'], target=[5, 'input']),
        
        dict(source=[0, 'output'], target=[3, 'input']),
        dict(source=[3, 'output'], target=[5, 'input']),
        
        dict(source=[0, 'output'], target=[4, 'input']),
        dict(source=[4, 'output'], target=[5, 'input']),
    ]
    config = {}
    
    template = Template(name='test reduction presentation',
                        description='example reduction diagram',
                        modules=modules,
                        wires=wires,
                        instrument=BT7.id,
                        )

if 1:
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
                        instrument=BT7.id,
                        )


# the actual call to perform the reduction

def TAS_RUN():
    result = run_template(template, config)
    '''
    print 'in TAS'
    for key, value in result.iteritems():
	for i in range(len(value['output'])):
		if not type(value['output'][i])==type({}):
        		value['output'][i] = value['output'][i].get_plottable()
    print result
    '''
    return result


if __name__ == "__main__":
    #hi=TAS_RUN()
    print 'template: ', simplejson.dumps(wireit.template_to_wireit_diagram(template))
    #print ROOT_URL.REPO_ROOT, ROOT_URL.HOMEDIR
    print 'language', simplejson.dumps(wireit.instrument_to_wireit_language(BT7))
    print "done"
