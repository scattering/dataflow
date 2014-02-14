## adds default objects to DB
import os
import hashlib
import cStringIO
import gzip
import hmac
import copy
import tempfile
from django.utils import simplejson as json
import json as orderedjson # keeps order of OrderedDict on dumps!

from numpy import NaN, array
import numpy as np

from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #paging for lists
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login

from dataflow import wireit
from dataflow.core import lookup_module, lookup_datatype
from dataflow.calc import calc_single, get_plottable, get_csv
from dataflow.cache import CACHE_MANAGER
from dataflow.offspecular.instruments import ANDR, ASTERIX
print "ANDR imported: ", ANDR.id
print "ASTERIX imported: ", ASTERIX.id
from dataflow.sans.novelinstruments import SANS_NG3
print "SANS imported: ", SANS_NG3.id
from dataflow.tas.instruments import TAS as TAS_INS
print "TAS imported: ", TAS_INS.id
from dataflow.refl.instruments import PBR as PBR_INS
print "PBR imported: ", PBR_INS.id

# For reading in files and their metadata in the EditExperiment page
from reduction.tas.data_abstraction import ncnr_filereader
from reduction.tas.data_abstraction import chalk_filereader
from reduction.tas.data_abstraction import hfir_filereader
from reduction.tas.data_abstraction import TripleAxis

# Used for segment interactor calculations
from reduction.common import linegen

from . import ftpview
from .models import * #add models by name
from .forms import (languageSelectForm, titleOnlyForm, experimentForm1,
                    experimentForm2, titleOnlyFormExperiment)

DATA_DIR=settings.DATA_DIR
CACHE_MANAGER.use_redis(settings.REDIS_HOST)

def showInteractors(request):
    return render_to_response('interactors.html')

def showPlotWindow(request):
    return render_to_response('plotwindow.html')

def showFTPloader(request):
    return render_to_response('FTPloader.html')

def showSliceWindow(request):
    return render_to_response('slicewindow.html')

def mytest(request):
    return render_to_response('tracer_testingforWireit/xhr_temp.html')

def uploadtest(request):
    return render_to_response('upload.html')

def testTable(request):
    return render(request,'testTable.html')

def xhr_test(request):
    if request.is_ajax():
        if request.method == 'GET':
            message = "This is an XHR GET request"
        elif request.method == 'POST':
            message = "This is an XHR POST request"
        else:
            message = "No XHR"
    else:
        message = "What is this, WSGI?"
    return HttpResponse(message)

def return_data(request):
    dataArray = [['file name', 'database id', 'sha1', 'x', 'y', 'z'],
                 [NaN, NaN, NaN, 10, 10, 10], [NaN, NaN, NaN, -10, -10, -10],
                 ['file3', '1', 'sh1', '1,9', '2,3', '3,4'],
                 ['file2', '1', 'sh2', '4,5', '2,3', '5,5']]
    return HttpResponse(json.dumps(dataArray))

def email_collaborator(request):
    """ Sends an email to a collaborator to give them access to a project via a link"""
    if not (request.POST.has_key('project_id') 
            and request.POST.has_key('collaborator_email')
            and request.POST.has_key('user_id')):
        return
    from django.template.loader import render_to_string
    from django.contrib.sites.models import RequestSite
    from django.contrib.sites.models import Site        
    
    # getting the site
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    project = Project.objects.get(id=request.POST['project_id'])
    user = User.objects.get(id=request.POST['user_id'])
    user_name = user.get_full_name()
    if len(user_name) < 1:
        user_name = user.email #if the user hasn't provided a name, use their email
        
    ctx_dict = {'email_activation_key': request.POST['collaborator_email'] + ';' + project.activation_key, 
                'site': site, 
                'user': user_name,
                'project_activate': 'apps.tracks.views.add_collaborator'}
    subject = render_to_string('registration/collaborate/activation_email_subject.txt', ctx_dict)
    
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    message = render_to_string('registration/collaborate/activation_email.txt', ctx_dict)
    
    #user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.POST['collaborator_email']])
    return HttpResponse('OK')
        

#def add_collaborator(request, email_address, activation_key):
def add_collaborator(request, email_activation_key=None):
    """ When a collaborator clicks the link sent by the email_collaborator function,
        this function will be called. If they have an existing account (based on email)
        they will be directed to the project. If not, a temporary account will be
        created for them (with an unusable password, ie they'll be prompted to set it).
        
        email_activation_key: has the form 'email;activationkey' (separated by semicolon)
    """
    email_address, activation_key = email_activation_key.split(';')        
    projects = Project.objects.filter(activation_key=activation_key)
    #if there is in fact a project with this activation key:
    if len(projects) > 0: 
        # if the user is logged in already, the project is added to their account
        # as opposed to adding it to the email (and maybe creating an account for the email)
        if request.user.is_authenticated():
            collaborators = [request.user]
        else:
            collaborators = User.objects.filter(email=email_address)
            
        if len(collaborators) > 0:
            projects[0].users.add(collaborators[0]) #adds user to project
            return HttpResponseRedirect('/projects/')
        else:
            random_pass=User.objects.make_random_password(10)
            collaborator = User.objects.create(username=email_address,
                                               first_name = '',
                                               last_name = '',
                                               email = email_address
                                               )
            collaborator.set_password(random_pass)
            #collaborator.set_unusable_password()
            collaborator.save()
            projects[0].users.add(collaborator)
            user = authenticate(username=email_address,password=random_pass)
            login(request, user)
            
            #message=r'Your username is this email.address.   Please reset your password the first time you log in.  Have fun!'
            #send_mail(r'Welcome to DrNeutron!', message, settings.DEFAULT_FROM_EMAIL, [email_address])
            #We want redirect to http://www.drneutron.org/password/reset/confirm/yourhashhere/
            
            return HttpResponseRedirect('/projects/')
            #return HttpResponseRedirect(profile/edit)
    else:
        # no project with this activation_key exists (project could have been deleted)
        #TODO: create an error page!!!!
        pass

def calculate_segment_interactor(request):
    #try:
    point1 = (float(request.GET['x1']), float(request.GET['y1']))
    point2 = (float(request.GET['x2']), float(request.GET['y2']))
    xarr = array(json.loads(request.GET['xarr']))
    yarr = array(json.loads(request.GET['yarr']))
    zarr = array(json.loads(request.GET['zarr']))
    
    myline = linegen.line_interp(point1, point2, divisions=5)
    xout, yout, zout = myline.interp(xarr, yarr, zarr)
    line_x = myline.line_x
    line_y = myline.line_y
    
    zout[np.isnan(zout)] = 0.
    return HttpResponse(json.dumps({'line_x': line_x.tolist(),
                                    'line_y': line_y.tolist(),
                                    'zout': zout.tolist()}))
    #except:
    #    pass

def return_metadata(experiment_id):
    """
    !!! ASSUMPTION: all files have the same metadata fields !!!
    
    Creating a dataObject to be passed to moduleSimpleConfigForm.js
    dataObject will have the following mappings (key : value_description):

        headerlist : List of headers.  Indices correspond to column indices
        in  metadata.
        E.g.::

            ['Available Files', 'h_min', 'h_max', ...].

        metadata : 2D lists of metadata columns.  A file and all of its
        metadata  shares the same row index in this  2D list. By default,
        filenames are located in the first column  (i.e. metadata[0]).
        E.g.::

           [ ['file001', 'file002', ...], [0, 0.1, 0.2,...],
             [1.0, 1.1, 1.2,...], ... ]
                   
    This format is used to obtain min of min's and max of max's.
    NO LONGER USED FOR dataObject.
        
        dataObject : a 2D array.
        E.g.::

            [ [fileheaders...],  [min of min's...],
              [max of max's...], [row1 values], [row2 values], ... ]
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
    
    #return HttpResponse(json.dumps(dataObject))
    return json.dumps(dataObject)

#def return_loaded_file(request):
    

def getBinaryData(request):
    binary_fp = request.POST['binary_fp']
    #data = np.random.rand(1000,1000).astype(np.float32).tostring()
    #binary_fp = data['binary_fp']
    #print "getting data:", binary_fp
    #print 'cache().exists(binary_fp):', cache().exists(binary_fp), cache().keys()
    data = ''
    if CACHE_MANAGER.cache.exists(binary_fp):
        data = CACHE_MANAGER.cache.lrange(binary_fp, 0, -1)[0]
        print "sending data:", binary_fp
    
    response = HttpResponse(data, mimetype='application/octet-stream')
    #response = HttpResponse(['hello there', data], mimetype='multipart/x-mixed-replace')
    return response


def home(request):
    context = RequestContext(request)
    site_list = ['/editor/', '/login/', '/projects/', '/interactors/']
    return render_to_response('tracer_testingforWireit/home.html',
                              locals(), context_instance=context)

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

def getFTPdirectories(request):
    if (request.GET.has_key('address') and request.GET.has_key('username')
        and request.GET.has_key('password')):
        address = request.GET['address']
        username = request.GET['username']
        password = request.GET['password']
        if request.GET.has_key('directory'):
            directory = request.GET['directory']
        else:
            directory = '/'
        result = ftpview.runFTP(address, directory, username=username,
                                password=password)
        return HttpResponse(json.dumps(result))

    return HttpResponse('Improper request')


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
for instr in [ANDR, SANS_NG3, TAS_INS, ASTERIX, PBR_INS]:
    instrument_class_by_language[instr.name] = instr

#instrument_by_language = {'andr2': ANDR, 'andr':ANDR, 'sans':SANS_INS, 'tas':TAS_INS, 'asterix':ASTERIX }
print 'instruments:', instrument_class_by_language.keys()

def listWirings(request):
    context = RequestContext(request)
    print 'I am loading'
    data = json.loads(request.POST['data'])
    instr = Instrument.objects.get(instrument_class = data['language'])
    wirings = [] # start from scratch
    default_templates = instr.Templates.all()
    for t in default_templates:
        wirings.append(json.loads(t.Representation))

    experiment_templates = Experiment.objects.get(id=data['experiment_id']).templates.all()
    for t in experiment_templates:
        wirings.append(json.loads(t.Representation))

    return HttpResponse(json.dumps(wirings)) 

#    return HttpResponse(json.dumps(a)) #andr vs bt7 testing

def saveWiring(request):
    #context = RequestContext(request)
    print 'I am saving'
    print request.POST
    postData = json.loads(request.POST['data'])
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
                result = {'save': 'failure', 'errorStr': 'this name exists, please use another'}
                reply = HttpResponse(json.dumps(result))
                reply.status_code = 500
                return reply
            temp = instr.Templates.create(Title=new_wiring['name'],
                                          Representation=json.dumps(new_wiring))
            temp.user.add(request.user)
        else:
            result = {'save': 'failure', 'errorStr': 'you are not staff!'}
            reply = HttpResponse(json.dumps(result))
            reply.status_code = 500
            return reply
    else:
        if len(Template.objects.filter(Title=new_wiring['name'])) > 0:
            result = {'save': 'failure', 'errorStr': 'This name exists, please use another.'}
            reply = HttpResponse(json.dumps(result))
            reply.status_code = 500
            return reply
        temp = Template.objects.create(Title=new_wiring['name'],
                                       Representation=json.dumps(new_wiring))
        temp.user.add(request.user)
    # this puts the Template into the pool of existing Templates.
    #wirings_list.append(new_wiring)
    return HttpResponse(json.dumps({'save':'successful'})) #, context_instance=context

def get_filepath_by_hash(fh):
    return os.path.join(File.objects.get(name=str(fh)).location,str(fh))



#def getFromRedis(hashval):
#    result = cache_manager.cache.lrange(hashval, 0, -1)
#    response = HttpResponse(result[0], mimetype='text/csv')
#    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
#    return response

def old_getCSV(request, data):
    print 'IN RUN REDUCTION: getting CSV'
    data = json.loads(request.POST['data'])
    print 'IN RUN REDUCTION: getting CSV'
    config = {}
    bad_headers = ["files", "position", "xtype", "width",
                   "terminals", "height", "title", "image", "icon"]
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
        #response = HttpResponse(json.dumps({'redis_key': result}))
    #print json.dumps({'redis_key': result[0][:800]})
    outfilename = data.get('outfilename', 'data.csv')
    response = HttpResponse(result, mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % (outfilename,)
    #response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
    return response


            
def setupReduction(data):
    #data = json.loads(request.POST['data'])
    #import pprint
    print 'IN RUN REDUCTION'
    #pprint.pprint( data )
    config = {}
    bad_headers = ["files", "position", "xtype", "width", "terminals",
                   "height", "title", "image", "icon", "fields"]
    active_group =str(int(data['group'])) # all keys are strings!
    for i in range(len(data['modules'])):
        m = data['modules'][i]
        conf = {}
        config_in = m.get('config', {})
        groups = config_in.get('groups', {})
        current_reduct = groups.get(active_group, {})
        for key, value in current_reduct.items():
            if key == 'files' and current_reduct.get('autochain-loader', {}).get('value', False) == True:
                new_moduleId = len(data['modules'])
                for f in value['value']:
                    new_config = copy.deepcopy(current_reduct)
                    #new_config.pop('files')
                    new_config['files']['value'] = [f]
                    new_config['autochain-loader']['value'] = False
                    new_mod = {'name': m['name'],
                               'config': {'position': [],
                                          'groups': { active_group : new_config}}}
                    data['modules'].append(new_mod)
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
    data = json.loads(request.POST['data'])
    template, config, nodenum, terminal_id = setupReduction(data)
    print "template:", template
    print "config:", config
    print "terminal_id:", terminal_id
    
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
    """
    takes a request to run a reduction, then stashes the result in 
    the filesystem as a tarfile with SHA1 as filename.
    """
    import tarfile
    import StringIO

    data = json.loads(request.POST['data'])
    toReduce = data['toReduce']
    template, config, nodenum, terminal_id = setupReduction(toReduce)
    result = calc_single(template, config, nodenum, terminal_id)
    result_strs = []
    sha1 = hashlib.new('sha1')
    for dataset in result:
        data_str = dataset.dumps()
        sha1.update(data_str)
        result_strs.append(data_str)
        
    filename = sha1.hexdigest()
    file_path = os.path.join(DATA_DIR, filename)
    
    tar = tarfile.open(file_path,"w:gz")
    
    for i, data_str in enumerate(result_strs):
        string = StringIO.StringIO()
        string.write(data_str)
        string.seek(0)
        info = tarfile.TarInfo(name="data_%d" % (i,))
        info.size=len(string.buf)
        tar.addfile(tarinfo=info, fileobj=string)

    tar.close()
    
    node = template.modules[nodenum]
    module_id = node['module'] # template.modules[node]
    module = lookup_module(module_id)
    terminal = module.get_terminal_by_id(terminal_id)
    datatype = terminal['datatype']
    
    print 'data:\n', data
    
    if data.has_key('experiment_id'):
        experiment_id = data['experiment_id']
        experiment = Experiment.objects.get(id=experiment_id)
    else:
        experiment = None
    
    new_wiring = data.get('new_wiring', '')
    dataname = data.get('dataname', 'saved_data')
    
    new_files = File.objects.filter(name=filename)
    if len(new_files) > 0:
        new_file = new_files[0]
    else:
        new_file = File.objects.create(friendly_name=dataname, name=filename,
                                       template_representation=new_wiring,
                                       datatype=datatype, location=DATA_DIR)
    
    for dobj in result:
        add_metadata_to_file(new_file, dobj)
    
    if experiment is not None:
        #print "experiment id: ", request.POST[u'experiment_id']
        experiment.Files.add(new_file)
    return HttpResponse('OK');
    
def getCSV(request):
    data = json.loads(request.POST['data'])
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
    data = json.loads(request.POST['data'])
    if data.has_key('filehashes'):
        filehashes = data['filehashes']
        existences = {}
        for filehash in filehashes:
            existing_file = File.objects.filter(name=filehash)
            if len(existing_file) > 0: file_exists = True
            else: file_exists = False
            existences[filehash] = file_exists
        print existences
    return HttpResponse(json.dumps(existences))


def uploadFTPFiles(request):
    """
    Given an FTP ``address``, ``experiment_id``, ``instrument_class``, ``loader_id``,
    and paths to the files to get (``filepaths``), the files will be retrieved from
    the ``address`` via FTP and uploaded.
    """
    if (request.POST.has_key('address')
        and request.POST.has_key('username')
        and request.POST.has_key('password')
        and request.POST.has_key( 'experiment_id')
        and request.POST.has_key('instrument_class')
        and request.POST.has_key( 'loader_id')
        and request.POST.has_key('filepaths')):
        filepaths = json.loads(request.POST['filepaths']) #given as a string of a list
        username = request.POST['username']
        password = request.POST['password']
        
        file_descriptors = ftpview.getFiles(request.POST['address'], filepaths,
                                            username=username, password=password)
        experiment_id = request.POST['experiment_id']
        instrument_class = request.POST['instrument_class']
        loader_id = request.POST['loader_id']
        uploadFilesAux(file_descriptors, experiment_id, instrument_class, loader_id) #upload the files
    
    return HttpResponse('OK')
        

def uploadFiles(request):
    """
    Uploads files to Dataflow. To upload files, ``request`` must have:
        request.POST.FILES.FILES
        request.POST.instrument_class
        request.POST.experiment_id
        request.POST.loader_id
    """
    if request.FILES.has_key('FILES'):
        #instrument_class = request.POST[u'instrument_class']
        #instrument_by_language = {'andr2': ANDR, 'andr':ANDR, 'sans':SANS_INS, 'tas':TAS_INS, 'asterix':ASTERIX }
        #instrument = instrument_class_by_language.get(instrument_class, None)
        file_data = request.FILES.getlist('FILES')
        file_descriptors = []
        for f in file_data:
            file_contents = f.read()
            file_sha1 = hashlib.sha1(file_contents)

            #write_here = os.path.join(FILES_DIR,file_sha1.hexdigest())
            #open(write_here, 'w').write(file_data)
            tmp_file, tmp_path = tempfile.mkstemp()
            open(tmp_path, 'wb').write(file_contents)
            file_descriptors.append({'filename': tmp_path, 'friendly_name': f.name})
        
    if file_descriptors: #only has file_descriptors if it has 'FILES' or 'FTP_FILES'
        instrument_class = request.POST[u'instrument_class']    
        loader_id = request.POST[u'loader_id']
        experiment_id = request.POST[u'experiment_id']
        uploadFilesAux(file_descriptors, experiment_id, instrument_class, loader_id)

    return HttpResponse('OK') 

def uploadFilesAux(file_descriptors, experiment_id, instrument_class, loader_id):
    """
    Uploads the files (as specified by ``file_descriptors``) to Dataflow. Additional
    parameters required as well. uploadFiles was extracted into this auxiliary method to
    allow uploading manually (such as used by uploadFTPFiles), not just via WSGIRequest.
    
    Returns: nothing
    """    
    import tarfile
    import StringIO

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except:
        experiment = None #in the event the id does not match an experiment
    loader_function = None
    datatype_id = None
    for dt in instrument_class_by_language[instrument_class].datatypes:
        for l in dt.loaders:
            if l['id'] == loader_id:
                loader_function = l['function']
                datatype_id = dt.id
                break
    dataObjects = loader_function(file_descriptors)
    try:
        for fd in file_descriptors:
            os.remove(fd['filename'])
    except OSError as exc:
        print 'views.uploadFilesAux',exc
        #os.remove issues

    for dobj in dataObjects:
        # you'll want your data objects to take friendly_name as an argument (required above)
        # and pass it to an attribute called "friendly_name"
        # This allows for files that have many subsets of data in them to generate 
        # their own "friendly_name" for each dataset, in the manner of your choosing.
        if dobj is not None:
            #If the file uploaded was not uploadable with the selected loader, dobj=None
            #TODO: need to send an error to the user and notify them that the file was no good
            friendly_name = dobj.friendly_name if hasattr(dobj, 'friendly_name') else "data"
            serialized = dobj.dumps()
            s_sha1 = hashlib.sha1(serialized)
            filename = s_sha1.hexdigest()
            new_files = File.objects.filter(name=filename)
            
            string = StringIO.StringIO()
            string.write(serialized)
            string.seek(0)
    
            file_path = os.path.join(DATA_DIR, filename)
            tar = tarfile.open(file_path,"w:gz")
            info = tarfile.TarInfo(name=friendly_name)
            info.size=len(string.buf)
            tar.addfile(tarinfo=info, fileobj=string)
            tar.close()
            #dataname = data.get('dataname', 'saved_data')
            
            #write_here = os.path.join(FILES_DIR, s_sha1.hexdigest())
            #gzip.open(write_here, 'wb').write(serialized) 
            
            if len(new_files) > 0:
                new_file = new_files[0]
            else:
                new_file = File.objects.create(name=s_sha1.hexdigest(),
                                               friendly_name=friendly_name,
                                               location=DATA_DIR,
                                               datatype=datatype_id)
                add_metadata_to_file(new_file, dobj)
                
            if experiment is not None:
                #print "experiment id: ", request.POST[u'experiment_id']
                experiment.Files.add(new_file)                   

@transaction.commit_on_success
def add_metadata_to_file(new_file, instrument):
    """
    Adds the metadata extrema from the provided instrument to the provided file.
    Metadata is stored as key-value pairs as specified in models.py.
    NOTE: ONLY CALL FOR NEW FILES --> will be inefficient if the metadata object already exists
    """
    extrema = instrument.get_extrema()
    for key in extrema.keys():
        # Assumes that all keys (ie field headers) are strings/chars       
        new_metadata = Metadata.objects.create(Myfile=new_file,
                                               Key=key + '_min',
                                               Value=extrema[key][0])
        new_file.metadata.add(new_metadata)
        new_metadata = Metadata.objects.create(Myfile=new_file,
                                               Key=key + '_max',
                                               Value=extrema[key][1])
        new_file.metadata.add(new_metadata)
        
        
        _ = """
        # finds the unique location of this key in the database if it was previously loaded.
        # sorts on the file's unique hash then key value. Does this for both min and max.
        existing_metadata = Metadata.objects.filter(Myfile=new_file.name).filter(Key=keymin)
        
        if existing_metadata: 
            # if there is a metadata object in the database already, update its value
            existing_metadata[0].Value = extrema[key][0]
        else:
            new_metadata_min = Metadata.objects.create(Myfile=new_file,
                Key=keymin, Value=extrema[key][0])
            new_file.metadata.add(new_metadata_min)
        keymax = key + '_max'
        existing_metadata = files.filter(Key=keymax)
        if existing_metadata: 
            # if there is a metadata object in the database already, update its value
            existing_metadata[0].Value = extrema[key][1]                    
        else:
            new_metadata_max = Metadata.objects.create(Myfile=new_file,
                Key=keymax, Value=extrema[key][1])
            new_file.metadata.add(new_metadata_max)
        """
    
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
                # in the event that there is no extension (ie only a hash
                # was provided), fileExt remains None
                pass
            
    if fileExt in ['.bt2', '.bt4', '.bt7', '.bt9', '.ng5']:
        instrument = ncnr_filereader(filestr, friendly_name=friendly_name)
    elif fileExt in ['.dat']:
        instrument = hfir_filereader(filestr)
    
    return instrument

###### BT7 TESTING
#    register_instrument(BT7)
#    instruments.init_data()
#    template = wireit.wireit_diagram_to_template(json.loads(str(request.POST['data'])), BT7)
    #   a = run_template(template, [{'files': ['f1.bt7', 'f2.bt7']}, {'align': ['A3']}, {'scale': 2.5}, {'ext': 'dat'}])
    #   print a    
    #   data = [[random.random(), random.random()] for i in range(10)]
    #   c = {'reduction':'successful', 'data': data}
    #   return HttpResponse(json.dumps(a))

###### ANDR TESTING
#    register_instrument(ANDR)
#    print "DONE REGISTERING"
#    template = wireit.wireit_diagram_to_template(json.loads(str(request.POST['data'])), ANDR)
#    template = wireit.wireit_diagram_to_template(offspec[0], ANDR)
#    print template
#    print "RUNNING"
#    a = run_template(template, [d['config'] for d in template.modules])
#    print "DONE RUNNING"
#    print a
#    return HttpResponse(json.dumps(a))


######## 
## Views for displaying a language selection form and for calling the file association table with the selected language.
## scheme is the same as for the editor



########
## Views for displaying a language selection form and for calling the editor template with the selected language.
## The intermediate template 'editorRedirect.html' is used so that we can redirect to /editor/ while preserving 
## the language selection.

def return_files_metadata(request):
    """
    Returns FILES and METADATA
    """
    if request.GET.has_key('experiment_id'):
        experiment_id = int(request.GET['experiment_id'])
        experiment = Experiment.objects.get(id=experiment_id)
        
        file_list = experiment.Files.all()
        file_keys = [[fl.name, fl.friendly_name] for fl in file_list]
        file_metadata = return_metadata(experiment_id)
        result = {'file_keys': file_keys, 'file_metadata': file_metadata}
        return HttpResponse(json.dumps(result))    
        #return json.dumps(file_keys),return_metadata(experiment_id) 

def displayEditor(request):
    context = RequestContext(request)
    file_context = {}
    print "displayEditor", request.POST.has_key('language')
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
        file_context['file_keys'] = json.dumps(file_keys)
        file_context['file_metadata'] = return_metadata(experiment_id)
        language_name = request.POST['language']
        file_context['language_name'] = language_name
        file_context['experiment_id'] = experiment_id
        # not using json here because for some reason the old version of json on danse
        # does not respect key order for OrderedDict.
    
        #try:
        lang = wireit.instrument_to_wireit_language(instrument_class_by_language[language_name])
        file_context['language_actual'] = orderedjson.dumps(lang)

        _ = '''
        except:
            #TODO 6/11/2012 - this redirects --> need to convert into popup if possible!
            reply = HttpResponse('Remember to save changes first!')
            reply.status_code = 500
            return reply
        '''
        return render_to_response('tracer_testingforWireit/editor.html',
                                  file_context, context_instance=context)
    else:
        return HttpResponseRedirect('/editor/langSelect/')

# this is now deprecated - because languages are sent directly in displayEditor
def languageSelect(request):
    context = RequestContext(request)
    if request.POST.has_key('instruments'):
        return render_to_response('tracer_testingforWireit/editorRedirect.html',
                                  {'lang':request.POST['instruments']},
                                  context_instance=context)
    form = languageSelectForm()
    return render_to_response('tracer_testingforWireit/languageSelect.html',
                              {'form':form}, context_instance=context)


###########
## Views for users, redirects to projects page from login. Then continues logically from there.
@login_required
def projects(request):
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
        # importing secret key here only to minimize its visibility...
        from apps.keygen import get_key
        msg = str(newproj.Title) + ';' + str(newproj.id) #creating activation_key based on project Title and id
        newproj.activation_key = hmac.new(get_key(), msg, hashlib.sha1).hexdigest()
        newproj.save()
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
    return render_to_response('userProjects/displayProjects.html',
                              {'projects':projects, 'form':form},
                              context_instance=context)

@login_required
def editProject(request, project_id):
    if request.POST.has_key('experiment_id'):
        experiment_id = request.POST['experiment_id']
        Experiment.objects.get(id=experiment_id).delete() 
    elif request.POST.has_key('new_experiment'):
        new_exp = Experiment.objects.create(ProposalNum=request.POST['new_experiment'],
                                            project=Project.objects.get(id=project_id))
        new_exp.users.add(request.user)
        _ = '''
        # No longer using instrument name when creating an experiment! Only instrument_class matters.
        # This segment was replaced by the instrument class 'if' segment below.
        if request.POST.has_key('instrument_name'):
            if request.POST['instrument_name']:
                instrument = Instrument.objects.get(id=request.POST['instrument_name'])
                instrument_class = instrument.instrument_class
                new_exp.instrument = instrument
                new_exp.save()
        '''
        if request.POST.has_key('instrument_class') and request.POST['instrument_class']:
            new_exp.instrument = Instrument.objects.get(instrument_class=request.POST['instrument_class'])
            new_exp.save()
        if request.POST.has_key('facility'):
            if request.POST['facility']:
                facility = Facility.objects.get(id=request.POST['facility'])
                new_exp.facility = facility
                new_exp.save()
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
    return render_to_response('userProjects/editProject.html',
                              {'project':project, 'form':form, 'experiments':experiments},
                              context_instance=context)

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
            write_here = tempfile.gettempdir() + file_sha1.hexdigest()
            open(write_here, 'w').write(file_contents)
            
            new_files = File.objects.filter(name=file_sha1.hexdigest())
            if len(new_files) > 0:
                new_file = new_files[0]
            else:
                new_file = File.objects.create(name=file_sha1.hexdigest(),
                                               friendly_name=f.name,
                                               location=DATA_DIR)
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
    form1 = experimentForm1(initial={'facility':facility, 'instrument_class':instrument_class})
    #form1 = experimentForm1(initial={'facility':facility, 'instrument_class':instrument_class, 'instrument_name':instrument, })
    loaders = []
    for dt in instrument_class_by_language[instrument_class].datatypes:
        loaders.extend([l['id'] for l in dt.loaders])
    form2 = experimentForm2(USER=request.user, experiment=experiment, loaders = loaders )
    #print form2.fields['new_templates'].length
    return render_to_response('userProjects/editExperiment.html',
                              { 'form1':form1, 'form2': form2, 'experiment':experiment, },
                              context_instance=context)

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
