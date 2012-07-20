from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.utils import simplejson
import json # keeps order of OrderedDict on dumps!
from apps.tracks.forms import languageSelectForm, titleOnlyForm, experimentForm1, experimentForm2, titleOnlyFormExperiment
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #paging for lists
from django.core.exceptions import ObjectDoesNotExist
import cStringIO, gzip

import hashlib,os
import types
import tempfile

## models
from django.contrib.auth.models import User 
from models import * #add models by name

## adds test objects to DB
from ... import fillDB


#from ...apps.fileview import testftp

from ...dataflow import wireit
from ...dataflow.core import lookup_module, lookup_datatype
from ...dataflow.calc import run_template
from ...dataflow.calc import calc_single, fingerprint_template, get_plottable, get_csv
from ...dataflow.offspecular.instruments import ANDR, ASTERIX
print "ANDR imported: ", ANDR.id
#from ...dataflow.offspecular.instruments import ASTERIX
print "ASTERIX imported: ", ASTERIX.id
from ...dataflow.SANS.novelinstruments import SANS_NG3
print "SANS imported: ", SANS_NG3.id
from ...dataflow.tas.instruments import TAS as TAS_INS
print "TAS imported: ", TAS_INS.id

# For reading in files and their metadata in the EditExperiment page
from ...reduction.tripleaxis.data_abstraction import ncnr_filereader
from ...reduction.tripleaxis.data_abstraction import chalk_filereader
from ...reduction.tripleaxis.data_abstraction import hfir_filereader


from ...dataflow import wireit

import random
from numpy import NaN

from django.conf import settings
FILES_DIR=settings.FILES_DIR

def xhr_test(request):
    if request.is_ajax():
        if request.method == 'GET':
            message = "This is an XHR GET request"
        elif request.method == 'POST':
            message = "This is an XHR POST request"
            # Here we can access the POST data
            print request.POST
        else:
            message = "No XHR"
    else:
        message = "What is this, WSGI?"
    return HttpResponse(message)

def showInteractors(request):
    return render_to_response('interactors.html')

def showPlotWindow(request):
    return render_to_response('plotwindow.html')

def showSliceWindow(request):
    return render_to_response('slicewindow.html')

def mytest(request):
    return render_to_response('tracer_testingforWireit/xhr_temp.html')

def uploadtest(request):
    return render_to_response('upload.html')

def testTable(request):
    return render(request,'testTable.html')

def return_data(request):
    dataArray=[['file name','database id','sha1','x','y','z'],[NaN,NaN,NaN,10,10,10],[NaN,NaN,NaN,-10,-10,-10],['file3','1','sh1','1,9','2,3','3,4'],['file2','1','sh2','4,5','2,3','5,5']]    
    return HttpResponse(simplejson.dumps(dataArray))

def return_metadata(experiment_id):
    """
    !!! ASSUMPTION: all files have the same metadata fields !!!
    
    Creating a dataObject to be passed to moduleSimpleConfigForm.js
    dataObject will have the following mappings (key : value_description):
        headerlist : List of headers. Indices correspond to column indices in metadata.
                     e.g. ['Available Files', 'h_min', 'h_max', ...]. 
        metadata : 2D lists of metadata columns. A file and all of its metadata shares the same
                   row index in this 2D list. By default, filenames are located in the first
                   column (i.e. metadata[0]).
                   e.g. [['file001', 'file002', ...], [0, 0.1, 0.2,...], [1.0, 1.1, 1.2,...], ...]
                   
    This format is used to obtain min of min's and max of max's. NO LONGER USED FOR dataObject.
        
        dataObject : a 2D array of in the form: [[fileheaders...], [min of min's...], 
                                                 [max of max's...],[row1 values], [row2 values],...]
    """
    #if request.GET.has_key(u'experiment_id'):
    #experiment_id = request.GET[u'experiment_id']
    if experiment_id < 0:
        return '{}'
    
    experiment = Experiment.objects.get(id=experiment_id) 
    
    headerlist = ['Available Files']
    metadata = []
    dataObject = []
    
    for f in experiment.Files.all():
        try:
            metadata[0].append(f.friendly_name)
        except:
            metadata.insert(0, [f.friendly_name])
        
        datalist = [f.friendly_name]
        metadatalist = f.metadata.all()
        for i in range(len(metadatalist)):
            #if a min/max  is not a float, it is assigned NaN
            try:
                value = float(metadatalist[i].Value)
            except:
                value = NaN
            key = metadatalist[i].Key
            
            
            try:
                index = headerlist.index(key)
            except:
                index = len(headerlist)
                headerlist.append(key)
                
            try:
                metadata[index].append(value)
            except:
                #first time, instantiate the list
                metadata.insert(index, [value])
                
            # the '_min' should always directly proceed the '_max' based on the way
            # Metadata was created in uploadFiles()
            ending = key[-4:] #will get the '_min' or '_max'
            if ending == '_min':
                datalist.append(repr(value))
            elif ending == '_max':
                datalist[-1] = datalist[-1] + ',' + repr(value)
                
        dataObject.append(datalist)
                
    fileheaders = ['Available Files']
    for i in range(0, len(headerlist)/2):
        #loops through all headers, skipping every other (ie the ones ending in '_max')
        index = i * 2 + 1
        fileheaders.append(headerlist[index][:-4]) #removes the '_min' ending
        
    minvals = [NaN]
    maxvals = [NaN]
    for i in range(0, len(headerlist)/2):
        minval = min(metadata[i * 2 + 1]) #find min of min's for each '_min' column
        maxval = max(metadata[i * 2 + 2]) #find max of max's for each '_max' column
               
        minvals.append(NaN if type(minval)==type('') else minval)
        maxvals.append(NaN if type(maxval)==type('') else maxval)
        
        
    dataObject.insert(0, minvals)
    dataObject.insert(0, maxvals)
    dataObject.insert(0, fileheaders)
    
    #return HttpResponse(simplejson.dumps(dataObject))
    return simplejson.dumps(dataObject)

import redis
server = redis.Redis("localhost")


#def return_loaded_file(request):
    

def getBinaryData(request):
    binary_fp = request.POST['binary_fp']
    #import numpy
    #data = numpy.random.rand(1000,1000).astype(numpy.float32).tostring()
    #binary_fp = data['binary_fp']
    print "getting data:", binary_fp
    print 'server.exists(binary_fp):', server.exists(binary_fp), server.keys()
    data = ''
    if server.exists(binary_fp):
        data = server.lrange(binary_fp, 0, -1)[0]
        print "sending data:", binary_fp
    
    response = HttpResponse(data, mimetype='application/octet-stream')
    #response = HttpResponse(['hello there', data], mimetype='multipart/x-mixed-replace')
    return response


def home(request):
    context = RequestContext(request)
    site_list = ['/editor/', '/login/', '/myProjects/', '/interactors/']
    return render_to_response('tracer_testingforWireit/home.html', locals(), context_instance=context)

##################
#### file loading testing

store = [{
    "id": 0,
    "text": "A leaf Node",
    "leaf": True
    }, {
        "id": 1,
        "text": "A folder Node",
        "children": [{
            "id": 2,
            "text": "A child Node",
            "leaf": True
            #"children":[{}],
        }]
    }]
def getNCNRdirectories(request):
    return HttpResponse(simplejson.dumps(testftp.runMe()))  #testftp.runMe()

def displayFileLoad(request):
    return render_to_response('FileUpload/FileTreeTest.html', locals())




sample_data = {
    'type': '2d',
    'z':  [ [1, 2], [3, 4] ],
    'title': 'This is the title',
    'dims': {
        'xmax': 1.0,
        'xmin': 0.0,
        'ymin': 0.0,
        'ymax': 12.0,
        'xdim': 2,
        'ydim': 2,
        },
    'xlabel': 'This is my x-axis label',
    'ylabel': 'This is my y-axis label',
    'zlabel': 'This is my z-axis label',
}

b = {'save':'successful'}

# apps.tracks.models, convert file hash to file path
        # File.objects.get(id=hash).location ("/tmp/FILES/{filename}")
        # wireit.py, convert wireit_diagram to template
# 

instrument_class_by_language = {}
for instr in [ANDR, SANS_NG3, TAS_INS, ASTERIX]:
    instrument_class_by_language[instr.name] = instr

#instrument_by_language = {'andr2': ANDR, 'andr':ANDR, 'sans':SANS_INS, 'tas':TAS_INS, 'asterix':ASTERIX }
print 'instrument_class_by_language:', instrument_class_by_language

#@csrf_exempt 
def listWirings(request):
    context = RequestContext(request)
    print 'I am loading'
    data = simplejson.loads(request.POST['data'])
    instr = Instrument.objects.get(instrument_class = data['language'])
    wirings = [] # start from scratch
    default_templates = instr.Templates.all()
    for t in default_templates:
        wirings.append(simplejson.loads(t.Representation))

    experiment_templates = Experiment.objects.get(id=data['experiment_id']).templates.all()
    for t in experiment_templates:
        wirings.append(simplejson.loads(t.Representation))

    return HttpResponse(simplejson.dumps(wirings)) 

#    return HttpResponse(simplejson.dumps(a)) #andr vs bt7 testing

#@csrf_exempt 
def saveWiring(request):
    #context = RequestContext(request)
    print 'I am saving'
    print request.POST
    postData = simplejson.loads(request.POST['data'])
    new_wiring = postData['new_wiring']
    # this stores the wires in a simple list, in memory on the django server.
    # replace this with a call to storing the wiring in a real database.
    #print 'TEMPLATE NAME: ', new_wiring['name']
    #print 'TEMPLATE REPR: ', new_wiring
    print 'USER: ',request.user
    print new_wiring
    user = User.objects.get(username=request.user)
    if postData['saveToInstrument'] == True:
        if user.is_staff:
            instr = Instrument.objects.get(instrument_class = new_wiring['language'])
            if len(instr.Templates.filter(Title=new_wiring['name'])) > 0:
                reply = HttpResponse(simplejson.dumps({'save': 'failure', 'errorStr': 'this name exists, please use another'}))
                reply.status_code = 500
                return reply
            temp = instr.Templates.create(Title=new_wiring['name'], Representation=simplejson.dumps(new_wiring))
            temp.user.add(request.user)
        else:
            reply = HttpResponse(simplejson.dumps({'save': 'failure', 'errorStr': 'you are not staff!'}))
            reply.status_code = 500
            return reply
    else:
        if len(Template.objects.filter(Title=new_wiring['name'])) > 0:
            reply = HttpResponse(simplejson.dumps({'save': 'failure', 'errorStr': 'this name exists, please use another'}))
            reply.status_code = 500
            return reply
        temp = Template.objects.create(Title=new_wiring['name'], Representation=simplejson.dumps(new_wiring))
        temp.user.add(request.user)
    # this puts the Template into the pool of existing Templates.
    #wirings_list.append(new_wiring)
    return HttpResponse(simplejson.dumps({'save':'successful'})) #, context_instance=context

def get_filepath_by_hash(fh):
    return os.path.join(File.objects.get(name=str(fh)).location,str(fh))



#@csrf_exempt
#def getFromRedis(hashval):
#    result = server.lrange(hashval, 0, -1)
#    response = HttpResponse(result[0], mimetype='text/csv')
#    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
#    return response

def old_getCSV(data):
    print 'IN RUN REDUCTION: getting CSV'
    data = simplejson.loads(request.POST['data'])
    print 'IN RUN REDUCTION: getting CSV'
    config = {}
    bad_headers = ["files", "position", "xtype", "width", "terminals", "height", "title", "image", "icon"]
    active_group =str(int(data['group'])) # all keys are strings!
    for i, m in enumerate(data['modules']):
        conf = {}
        config_in = m.get('config', {})
        groups = config_in.get('groups', {})
        current_reduct = groups.get(active_group, {})
        for key, value in current_reduct.items():
            print key, value
            if key == 'files':
                file_hashes = [data['file_dict'][f] for f in value['value']]
                file_paths = [get_filepath_by_hash(fh) for fh in file_hashes]
                conf.update({'files': file_paths})
            elif key not in bad_headers:
                conf.update({key: value['value']}) # mod for detailed confs coming from javascript
        config.update({i:conf})
    context = RequestContext(request)
    terminal_id = data['clickedOn']['source']['terminal']
    nodenum = int(data['clickedOn']['source']['moduleId'])
    print "calculating: terminal=%s, nodenum=%d" % (terminal_id, nodenum)
    language = data['language']
    instrument = instrument_class_by_language.get(language, None)
    #instrument_by_language = {'andr2': ANDR, 'andr':ANDR, 'sans':SANS_INS, 'tas':TAS_INS, 'asterix':ASTERIX}
    #instrument = instrument_by_language.get(language, None)
    result = ['{}']
    if instrument is not None:
        template = wireit.wireit_diagram_to_template(data, instrument)
        # configuration for template is embedded
        print "getting result"
        result = get_csv(template, config, nodenum, terminal_id)[0]
        #response = HttpResponse(simplejson.dumps({'redis_key': result}))
    #print simplejson.dumps({'redis_key': result[0][:800]})
    outfilename = data.get('outfilename', 'data.csv')
    response = HttpResponse(result, mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % (outfilename,)
    #response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
    return response


            
#@csrf_exempt 
def setupReduction(data):
    #data = simplejson.loads(request.POST['data'])
    #import pprint
    print 'IN RUN REDUCTION'
    #pprint.pprint( data )
    config = {}
    bad_headers = ["files", "position", "xtype", "width", "terminals", "height", "title", "image", "icon", "fields"]
    active_group =str(int(data['group'])) # all keys are strings!
    for i in range(len(data['modules'])):
        m = data['modules'][i]
        conf = {}
        config_in = m.get('config', {})
        groups = config_in.get('groups', {})
        current_reduct = groups.get(active_group, {})
        for key, value in current_reduct.items():
            if key == 'files' and current_reduct.get('autochain-loader', {}).get('value', False) == True:
                import copy
                new_moduleId = len(data['modules'])
                for f in value['value']:
                    new_config = copy.deepcopy(current_reduct)
                    #new_config.pop('files')
                    new_config['files']['value'] = [f]
                    new_config['autochain-loader']['value'] = False
                    data['modules'].append({'name': m['name'], 'config': {'position': [], 'groups': { active_group : new_config}}})
                    new_wire = {'src': {'moduleId': new_moduleId, 'terminal': 'output'},
                                'tgt': {'moduleId': i, 'terminal': 'input'}}
                    data['wires'].append(new_wire)
                    new_moduleId += 1
                current_reduct['files']['value'] = []
                #print 'autochaining! new config:'
                #pprint.pprint( data )
                
    for i in range(len(data['modules'])):
        m = data['modules'][i]
        conf = {}
        config_in = m.get('config', {})
        groups = config_in.get('groups', {})
        current_reduct = groups.get(active_group, {})
        for key, value in current_reduct.items():
            if key in ['files', 'chalk_files']: # if new file formats are added, at to list
                file_hashes = [data['file_dict'][f] for f in value['value']]
                file_paths = [get_filepath_by_hash(fh) for fh in file_hashes]
                conf.update({'files': file_paths})
            elif key not in bad_headers:
                conf.update({key: value['value']}) # mod for detailed confs coming from javascript
        config.update({i:conf})
    #context = RequestContext(request)
    terminal_id = data['clickedOn']['source']['terminal']
    nodenum = int(data['clickedOn']['source']['moduleId'])
    print "calculating: terminal=%s, nodenum=%d" % (terminal_id, nodenum)
    language = data['language']
    #instrument_by_language = {'andr2': ANDR, 'andr':ANDR, 'sans':SANS_INS, 'tas':TAS_INS, 'asterix':ASTERIX }
    instrument = instrument_class_by_language.get(language, None)
    #result = ['{}']
    if instrument is None:
        return
    template = wireit.wireit_diagram_to_template(data, instrument) 
    return template, config, nodenum, terminal_id
    
#        # configuration for template is embedded
#        print "getting result"
#        if data['result_type'] == 'csv':
#            result = get_csv(template, config, nodenum, terminal_id)[0]
#            outfilename = data.get('outfilename', 'data.csv')
#            response = HttpResponse(result, mimetype='text/csv')
#            response['Content-Disposition'] = 'attachment; filename=%s' % (outfilename,)
#            #response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
#            return response
#        else: # data['result_type'] == 'plottable':
#            result = get_plottable(template, config, nodenum, terminal_id)
#            JSON_result = '[' + ','.join(result) + ']'            
#            # result is a list of plottable items (JSON strings) - need to concatenate them
#            print "result acquired"
#            zbuf = cStringIO.StringIO()
#            zfile = gzip.GzipFile(mode='wb', compresslevel=3, fileobj=zbuf)
#            zfile.write(JSON_result.encode('utf-8'))
#            zfile.close()
#            print "buffer written"
#            compressed_content = zbuf.getvalue()
#            response = HttpResponse(compressed_content)
#            response['Content-Encoding'] = 'gzip'
#            response['Content-Length'] = str(len(compressed_content))
#            print "response sent", str(len(compressed_content))
#            return response
#            #return HttpResponse(JSON_result) #, context_instance=context
      
def runReduction(request):
    data = simplejson.loads(request.POST['data'])
    template, config, nodenum, terminal_id = setupReduction(data)
    
    result = get_plottable(template, config, nodenum, terminal_id)
    
    JSON_result = '[' + ','.join(result) + ']'
    # result is a list of plottable items (JSON strings) - need to concatenate them
    print "result acquired"
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=3, fileobj=zbuf)
    zfile.write(JSON_result.encode('utf-8'))
    zfile.close()
    print "buffer written"
    compressed_content = zbuf.getvalue()
    response = HttpResponse(compressed_content)
    response['Content-Encoding'] = 'gzip'
    response['Content-Length'] = str(len(compressed_content))
    print "response sent", str(len(compressed_content))
    return response

def saveData(request):
    # takes a request to run a reduction, then stashes the result in 
    # the filesystem as a tarfile with SHA1 as filename.
    location = FILES_DIR
    data = simplejson.loads(request.POST['data'])
    toReduce = data['toReduce']
    template, config, nodenum, terminal_id = setupReduction(toReduce)
    result = calc_single(template, config, nodenum, terminal_id)
    result_str = result.dumps()
    filename = hashlib.sha1(result_str)
    
    node = template.modules[nodenum]
    module_id = node['module'] # template.modules[node]
    module = lookup_module(module_id)
    terminal = module.get_terminal_by_id(terminal_id)
    datatype = terminal['datatype']
    
    if toReduce.has_key('experiment_id'):
        experiment_id = toReduce['experiment_id']
        experiment = Experiment.objects.get(id=experiment_id)
    else:
        experiment = None
    
    new_wiring = data.get('new_wiring', '')
        
    import tarfile
    import StringIO

    file_path = os.path.join(FILES_DIR, filename)
    tar = tarfile.open(file_path,"w:gz")
    
    for i, dataset in enumerate(result):
        string = StringIO.StringIO()
        string.write(dataset.dumps())
        string.seek(0)
        info = tarfile.TarInfo(name="data_%d" % (i,))
        info.size=len(string.buf)
        tar.addfile(tarinfo=info, fileobj=string)

    tar.close()
    dataname = data.get('dataname', 'saved_data')
    
    new_file = File.objects.create(friendly_name=dataname, name=filename, template_representation=new_wiring, datatype=datatype, location=location)
    if experiment is not None:
        #print "experiment id: ", request.POST[u'experiment_id']
        experiment.Files.add(new_result)
    return HttpResponse('OK');
    
def getCSV(request):
    data = simplejson.loads(request.POST['data'])
    template, config, nodenum, terminal_id = setupReduction(data)
    
    result = ""
    result_list = get_csv(template, config, nodenum, terminal_id)
    for i, r in enumerate(result_list):
        result += "#" * 80 + "\n"
        result += "# data set %d" % (i,) + "\n"
        result += "#" * 80 + "\n"
        result += r
    
    outfilename = data.get('outfilename', 'data.csv')
    response = HttpResponse(result, mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % (outfilename,)
    return response 

def filesExist(request):
    data = simplejson.loads(request.POST['data'])
    if data.has_key('filehashes'):
        filehashes = data['filehashes']
        existences = {}
        for filehash in filehashes:
            existing_file = File.objects.filter(name=filehash)
            if len(existing_file) > 0: file_exists = True
            else: file_exists = False
            existences[filehash] = file_exists
        print existences
    return HttpResponse(simplejson.dumps(existences))

def uploadFiles(request):
    # TODO: In the process of storing instrument objects instead of raw files
    # TODO: THIS WHOLE METHOD WILL NEED TO BE REDONE    
    location = FILES_DIR
    if request.POST.has_key(u'experiment_id'):
        experiment_id = request.POST[u'experiment_id']
        experiment = Experiment.objects.get(id=experiment_id)
    else:
        experiment = None

    if request.FILES.has_key('FILES'):
        file_data = request.FILES.getlist('FILES')
        aofchalkfiles = []
        acfchalkfiles = []
        for f in file_data:
            #due to the strange nature of chalk river files, those are handled separately
            #appends all chalkriver files
            fileExt = os.path.splitext(f.name)[1].lower()
            if fileExt == '.aof':
                aofchalkfiles.append(f)
                continue
            if fileExt == '.acf':
                acfchalkfiles.append(f)
                continue
                
            file_data = f.read()
            file_sha1 = hashlib.sha1(file_data)

            write_here = os.path.join(location,file_sha1.hexdigest())
            open(write_here, 'w').write(file_data)

            new_files = File.objects.filter(name=file_sha1.hexdigest())
            
            if len(new_files) > 0:
                new_file = new_files[0]
            else:
                new_file = File.objects.create(name=file_sha1.hexdigest(), friendly_name=f.name, location=location, template_representation="", datatype="")
                
            # extract's the instrument's metadata to put into the File model
            data_object = call_appropriate_filereader(write_here, friendly_name=f.name, fileExt=fileExt)
            add_metadata_to_file(new_file, file_sha1, data_object)
            
            if experiment is not None:
                experiment.Files.add(new_file)
        '''
        for aoffile in aofchalkfiles:
            
            #NOTE: to link a .acf and .aof file, their names have to be EXACTLY the same (case sensitive)
            #NOTE: .acf files loaded without a corresponding .aof file are not read nor used.
            acf_filename = None
            aofname = os.path.splitext(aoffile.name)[0]
            for acffile in acfchalkfiles:
                acfname = os.path.splitext(acffile.name)[0]
                if acfname === aofname:
                    acfchalkfiles.remove(acffile)
                    acf_filename = acffile
                    break      
                   
            file_data = aoffile.read()
            file_sha1 = hashlib.sha1(file_data)
    
            write_here = os.path.join(location,file_sha1.hexdigest())
            open(write_here, 'w').write(file_data)
            
            instruments = chalk_filereader(write_here, acf_filename=acf_filename)
            
            # TODO: INCOMPLETE CHALK RIVER LOADING

        '''

    return HttpResponse('OK')

"""    
def uploadFiles(request):
    location = FILES_DIR
    if request.POST.has_key(u'experiment_id'):
        experiment_id = request.POST[u'experiment_id']
        experiment = Experiment.objects.get(id=experiment_id)
    else:
        experiment = None

    if request.FILES.has_key('FILES'):
        language = request.POST['language']
        #instrument_by_language = {'andr2': ANDR, 'andr':ANDR, 'sans':SANS_INS, 'tas':TAS_INS, 'asterix':ASTERIX }
        instrument = instrument_class_by_language.get(language, None)
        file_data = request.FILES.getlist('FILES')
        for f in file_data:
            file_contents = f.read()
            file_sha1 = hashlib.sha1(file_contents)

            #write_here = os.path.join(location,file_sha1.hexdigest())
            #open(write_here, 'w').write(file_data)
            tmp_file, tmp_path = tempfile.mkstemp()
            open(tmp_path, 'wb').write(file_contents)

            new_files = File.objects.filter(name=file_sha1.hexdigest())
            if len(new_files) > 0:
                new_file = new_files[0]
            else:
                new_file = File.objects.create(name=file_sha1.hexdigest(), friendly_name=f.name, location=location)

            if experiment is not None:
                #print "experiment id: ", request.POST[u'experiment_id']
                experiment.Files.add(new_file)

    return HttpResponse('OK') 
"""

def add_metadata_to_file(new_file, file_sha1, instrument):
    """
    Adds the metadata extrema from the provided instrument to the provided file.
    Metadata is stored 
    """
    extrema = instrument.extrema
    for key in extrema.keys():
        # Assumes that all keys (ie field headers) are strings/chars
        keymin = key + '_min'
        
        # finds the unique location of this key in the database if it was previously loaded.
        # sorts on the file's unique hash then key value. Does this for both min and max.
        existing_metadata = Metadata.objects.filter(Myfile=file_sha1.hexdigest()).filter(Key=keymin)
        if existing_metadata: 
            # if there is a metadata object in the database already, update its value
            existing_metadata[0].Value = extrema[key][0]
        else:
            new_metadata_min = Metadata.objects.create(Myfile=new_file, Key=keymin, Value=extrema[key][0])
            new_file.metadata.add(new_metadata_min)
        
        keymax = key + '_max'
        existing_metadata = Metadata.objects.filter(Myfile=file_sha1.hexdigest()).filter(Key=keymax)
        if existing_metadata: 
            # if there is a metadata object in the database already, update its value
            existing_metadata[0].Value = extrema[key][1]                    
        else:
            new_metadata_max = Metadata.objects.create(Myfile=new_file, Key=keymax, Value=extrema[key][1])
            new_file.metadata.add(new_metadata_max)

    
def call_appropriate_filereader(filestr, friendly_name=None, fileExt=None):
    """
    Determines the appropriate reader to call based on the file extension and returns
    the 'loaded' instrument object.
    
    filestr --> full path to file so that "open(filestr, 'r')" will work.
    friendly_name --> original file name before it was hashed to its sha1 identifier.
    fileExt --> file extension, generally obtained from the friendly_name. 
                Not available via sha1 hash
    """
    instrument = None
    if fileExt == None:
        if friendly_name:
            fileExt = os.path.splitext(friendly_name)[1].lower()
        else:
            try:
                fileExt = os.path.splitext(filestr)[1].lower()
            except:
                #in the event that there is no extension (ie only a hash was provided), fileExt remains None
                pass
            
    if fileExt in ['.bt2', '.bt4', '.bt7', '.bt9', '.ng5']:
        instrument = ncnr_filereader(filestr, friendly_name=friendly_name)
    elif fileExt in ['.dat']:
        instrument = hfir_filereader(filestr)
    
    return instrument

###### BT7 TESTING
#    register_instrument(BT7)
#    instruments.init_data()
#    template = wireit.wireit_diagram_to_template(simplejson.loads(str(request.POST['data'])), BT7)
    #   a = run_template(template, [{'files': ['f1.bt7', 'f2.bt7']}, {'align': ['A3']}, {'scale': 2.5}, {'ext': 'dat'}])
    #   print a    
    #   data = [[random.random(), random.random()] for i in range(10)]
    #   c = {'reduction':'successful', 'data': data}
    #   return HttpResponse(simplejson.dumps(a))

###### ANDR TESTING
#    register_instrument(ANDR)
#    print "DONE REGISTERING"
#    template = wireit.wireit_diagram_to_template(simplejson.loads(str(request.POST['data'])), ANDR)
#    template = wireit.wireit_diagram_to_template(offspec[0], ANDR)
#    print template
#    print "RUNNING"
#    a = run_template(template, [d['config'] for d in template.modules])
#    print "DONE RUNNING"
#    print a
#    return HttpResponse(simplejson.dumps(a))


######## 
## Views for displaying a language selection form and for calling the file association table with the selected language.
## scheme is the same as for the editor



########
## Views for displaying a language selection form and for calling the editor template with the selected language.
## The intermediate template 'editorRedirect.html' is used so that we can redirect to /editor/ while preserving 
## the language selection.

## HAVING TROUBLE SENDING LIST OF STRINGS AS CONTEXT TO THE EDITOR
#@csrf_exempt 
def displayEditor(request):
    context = RequestContext(request)
    file_context = {}
    print request.POST.has_key('language')
    if request.POST.has_key('language'):
        if request.POST.has_key('experiment_id'):
            experiment = Experiment.objects.get(id=request.POST['experiment_id'])
            file_list = experiment.Files.all()
            experiment_id = request.POST['experiment_id']
        else:
            experiment = []
            file_list = []
            experiment_id = -1
        file_keys = [[fl.name, fl.friendly_name] for fl in file_list]
        file_context['file_keys'] = simplejson.dumps(file_keys)
        file_context['file_metadata'] = return_metadata(experiment_id)
        language_name = request.POST['language']
        file_context['language_name'] = language_name
        file_context['experiment_id'] = experiment_id
        # not using simplejson here because for some reason the old version of simplejson on danse
        # does not respect key order for OrderedDict.
        
        #try:
        file_context['language_actual'] = json.dumps(wireit.instrument_to_wireit_language(instrument_class_by_language[language_name]))
        '''        
        except:
            #TODO 6/11/2012 - this redirects --> need to convert into popup if possible!
            reply = HttpResponse('Remember to save changes first!')
            reply.status_code = 500
            return reply
        '''
        return render_to_response('tracer_testingforWireit/editor.html', file_context, context_instance=context)
    else:
        return HttpResponseRedirect('/editor/langSelect/')

#@csrf_exempt 
# this is now deprecated - because languages are sent directly in displayEditor
def languageSelect(request):
    context = RequestContext(request)
    if request.POST.has_key('instruments'):
        return render_to_response('tracer_testingforWireit/editorRedirect.html',
                                  {'lang':request.POST['instruments']}, context_instance=context)
    form = languageSelectForm()
    return render_to_response('tracer_testingforWireit/languageSelect.html', {'form':form}, context_instance=context)


###########
## Views for users, redirects to MyProjects page from login. Then continues logically from there.
@login_required
def myProjects(request):
    context = RequestContext(request)
    #Using an elif setup to save a bit of time since only one button (to delete or add project)
    # can be clicked for one request.
    if request.POST.has_key('project_id'):
        project_id = request.POST['project_id']
        Project.objects.get(id=project_id).delete()
        #NOTE: new ids are assigned as (id of last id in list)+1 e.g. deleting project_id 7 out 
        #of 10, will make the next project_id 11 instead of reusing 7. Then if ids 8-11 were
        #deleted, then he next one made would be 7 again.
    elif request.POST.has_key('new_project'):
        newproj = Project.objects.create(Title=request.POST['new_project'])
        newproj.users.add(request.user)
    project_list = Project.objects.filter(users=request.user)
    paginator = Paginator(project_list, 10) #10 projects per pages
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    form = titleOnlyForm()
    return render_to_response('userProjects/displayProjects.html', {'projects':projects, 'form':form}, context_instance=context)

@login_required
def editProject(request, project_id):
    if request.POST.has_key('experiment_id'):
        experiment_id = request.POST['experiment_id']
        Experiment.objects.get(id=experiment_id).delete() 
    elif request.POST.has_key('new_experiment'):
        new_exp = Experiment.objects.create(ProposalNum=request.POST['new_experiment'], project=Project.objects.get(id=project_id))
        new_exp.users.add(request.user)
    context = RequestContext(request)
    project = Project.objects.get(id=project_id)
    experiment_list = project.experiment_set.all() #experiment_list = project.experiments.all()
    
    paginator = Paginator(experiment_list, 10)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        experiments = paginator.page(page)
    except PageNotAnInteger:
        experiments = paginator.page(1)
    except EmptyPage:
        experiments = paginator.page(paginator.num_pages)
    form = titleOnlyFormExperiment()
    return render_to_response('userProjects/editProject.html', {'project':project, 'form':form, 'experiments':experiments}, context_instance=context) 

@login_required 
def editExperiment(request, experiment_id):
    print request.POST
    experiment = Experiment.objects.get(id=experiment_id)
    if request.FILES.has_key('new_files'):
        file_data = request.FILES.getlist('new_files')
        for f in file_data:
            file_contents = f.read()
            file_sha1 = hashlib.sha1(file_contents)
            #file_sha1 = hashlib.sha1()
            #for line in f.read():
            #    file_sha1.update(line)
            write_here = TEMP_DIR + file_sha1.hexdigest()
            open(write_here, 'w').write(file_contents)
            
            new_files = File.objects.filter(name=file_sha1.hexdigest())
            if len(new_files) > 0:
                new_file = new_files[0]
            else:
                new_file = File.objects.create(name=file_sha1.hexdigest(), friendly_name=f.name, location=FILES_DIR)
            experiment.Files.add(new_file)
    if request.POST.has_key('instrument_name'):
        if request.POST['instrument_name']:
            instrument = Instrument.objects.get(id=request.POST['instrument_name'])
            instrument_class = instrument.instrument_class
            experiment.instrument = instrument
            experiment.save()
    if request.POST.has_key('facility'):
        if request.POST['facility']:
            facility = Facility.objects.get(id=request.POST['facility'])
            experiment.facility = facility
            experiment.save()
    if request.POST.has_key('new_templates'):
        if request.POST['new_templates']:
            for i in list(request.POST.getlist('new_templates')):
                template = Template.objects.get(id=i)
                experiment.templates.add(template)
        #print file_sha1.hexdigest()
        #print hashlib.sha1(request.FILES['files'].read()).hexdigest()
    if request.POST.has_key('cur_files'):
        if request.POST['cur_files']:
            delete_files = request.POST.getlist('cur_files')
            for f in delete_files:
                print "f: ", f
                print experiment.Files.filter(name=f)
                experiment.Files.filter(name=f).delete()
    if request.POST.has_key('cur_templates'):
        if request.POST['cur_templates']:
            delete_templates = request.POST.getlist('cur_templates')
            for t in delete_templates:
                print "t: ", t
                experiment.templates.filter(id=t).delete()
    context = RequestContext(request)
    facility = experiment.facility
    instrument = experiment.instrument
    if instrument:
        instrument_class = experiment.instrument.instrument_class
    else:
        instrument_class = None
    form1 = experimentForm1(initial={'facility':facility, 'instrument_class':instrument_class, 'instrument_name':instrument, })
    form2 = experimentForm2(USER=request.user, experiment=experiment)
    #print form2.fields['new_templates'].length
    return render_to_response('userProjects/editExperiment.html', { 'form1':form1, 'form2': form2, 'experiment':experiment, }, context_instance=context)

@login_required
def uploadFilesForm(request):
    context = RequestContext(request)
    if request.GET.has_key('experiment_id'):
        experiment_id = request.GET['experiment_id']
        print "experiment_id", experiment_id
    #experiment = Experiment.objects.get(id=0)
    print request.POST
    print request.FILES
    return render_to_response('FileUpload/editorUpload.html', {}, context_instance=context)
