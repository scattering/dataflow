# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.utils import simplejson
from apps.tracks.forms import languageSelectForm 

from ...apps.fileview import testftp

from ...dataflow import wireit
from ...dataflow.calc import run_template
from ...dataflow.core import register_instrument
#from ...dataflow.tas.instruments import BT7
#from ...dataflow.offspecular.instruments import ANDR
#from ...dataflow.tas import instruments
from ...dataflow.SANS import newinstruments as SANS_INS

import random

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

def mytest(request):
   return render_to_response('tracer_testingforWireit/xhr_temp.html')

def home(request):
    site_list = ['/hello/', '/test/', '/editor/', '/loadFiles/']
    return render_to_response('tracer_testingforWireit/home.html', locals())
    
##################
#### file loading testing

store = [{
        "id": 0,
        "text": "A leaf Node",
        "leaf": True
    },{
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
	return HttpResponse(simplejson.dumps(testftp.runMe()))
    
def displayFileLoad(request):
	return render_to_response('FileUpload/FileTreeTest.html', locals())
    
###################
#### TRACKS testing

a = [{"name":"test tas", "wires": [{"src": {"terminal": "output", "moduleId": 0}, "tgt": {"terminal": "input", "moduleId": 1}}, {"src": {"terminal": "output", "moduleId": 1}, "tgt": {"terminal": "input", "moduleId": 2}}, {"src": {"terminal": "output", "moduleId": 2}, "tgt": {"terminal": "input", "moduleId": 3}}], "modules": [{"terminals": "", "config": {"position": [5, 20], "xtype": "WireIt.Container"}, "name": "Load", "value": {}}, {"terminals": {"input": [-15, 1, -1, 0], "output": [15, 1, 1, 0]}, "config": {"position": [160, 20], "xtype": "WireIt.ImageContainer"}, "name": "Join", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [280, 40], "xtype": "WireIt.ImageContainer"}, "name": "Scale", "value": {}}, {"terminals": "", "config": {"position": [340, 40], "xtype": "WireIt.Container"}, "name": "Save", "value": {}}], "properties": {"name": "test tas", "description": "example TAS diagram"}}]    
offspec = [{"name":"andr test","wires": [{"src": {"terminal": "output", "moduleId": 0}, "tgt": {"terminal": "input", "moduleId": 2}}, {"src": {"terminal": "output", "moduleId": 2}, "tgt": {"terminal": "input", "moduleId": 3}}, {"src": {"terminal": "output", "moduleId": 3}, "tgt": {"terminal": "input", "moduleId": 4}}, {"src": {"terminal": "output", "moduleId": 4}, "tgt": {"terminal": "input", "moduleId": 5}}, {"src": {"terminal": "output", "moduleId": 5}, "tgt": {"terminal": "input", "moduleId": 6}}, {"src": {"terminal": "output", "moduleId": 6}, "tgt": {"terminal": "input", "moduleId": 1}}], "modules": [{"terminals": "", "config": {"files": ["/home/brendan/sampledata/ANDR/sabc/Isabc2002.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2003.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2004.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2005.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2006.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2007.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2008.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2009.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2010.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2011.cg1", "/home/brendan/sampledata/ANDR/sabc/Isabc2012.cg1"], "position": [50, 50], "intent": "signal", "xtype": "WireIt.Container"}, "name": "Load", "value": {}}, {"terminals": "", "config": {"position": [650, 350], "ext": "dat", "xtype": "WireIt.Container"}, "name": "Save", "value": {}}, {"terminals": {"input": [-15, 1, -1, 0], "output": [15, 1, 1, 0]}, "config": {"position": [150, 100], "xtype": "WireIt.ImageContainer"}, "name": "Join", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [250, 150], "xtype": "WireIt.ImageContainer", "offsets": {"theta": 0.10000000000000001}}, "name": "Offset", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [350, 200], "xtype": "WireIt.ImageContainer"}, "name": "Wiggle", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [450, 250], "xtype": "WireIt.ImageContainer"}, "name": "Pixels to two theta", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [550, 300], "xtype": "WireIt.ImageContainer"}, "name": "Two theta to qxqz", "value": {}}], "properties": {"name": "test ospec", "description": "example ospec diagram"}}]
SANS = [{"name":"sans test","wires": [{"src": {"terminal": "output", "moduleId": 0}, "tgt": {"terminal": "input", "moduleId": 2}}, {"src": {"terminal": "output", "moduleId": 2}, "tgt": {"terminal": "input", "moduleId": 3}}, {"src": {"terminal": "output", "moduleId": 3}, "tgt": {"terminal": "input", "moduleId": 4}}, {"src": {"terminal": "output", "moduleId": 4}, "tgt": {"terminal": "input", "moduleId": 5}}, {"src": {"terminal": "output", "moduleId": 5}, "tgt": {"terminal": "input", "moduleId": 1}}], "modules": [{"terminals": "", "config": {"files": ["/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC010.SA3_SRK_S110", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC008.SA3_SRK_S108", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC002.SA3_SRK_S102", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC006.SA3_SRK_S106", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC005.SA3_SRK_S105", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC007.SA3_SRK_S107", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/PLEX_2NOV2007_NG3.DIV"], "position": [5, 20], "intent": "signal", "xtype": "WireIt.Container"}, "name": "Load", "value": {}}, {"terminals": "", "config": {"position": [500, 500], "ext": "dat", "xtype": "WireIt.Container"}, "name": "Save", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 100], "xtype": "WireIt.ImageContainer"}, "name": "initial_correction", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 200], "xtype": "WireIt.ImageContainer"}, "name": "correct_detector_efficiency", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 300], "xtype": "WireIt.ImageContainer"}, "name": "absolute_scaling", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 400], "xtype": "WireIt.ImageContainer"}, "name": "annular_av", "value": {}}], "properties": {"name": "test sans", "description": "example sans data"}}]

SANS_2 = [{"name":"SANS 2","wires": [{"src": {"terminal": "output", "moduleId": 0}, "tgt": {"terminal": "input", "moduleId": 2}}, {"src": {"terminal": "output", "moduleId": 2}, "tgt": {"terminal": "input", "moduleId": 3}}, {"src": {"terminal": "output", "moduleId": 3}, "tgt": {"terminal": "input", "moduleId": 4}}, {"src": {"terminal": "output", "moduleId": 4}, "tgt": {"terminal": "input", "moduleId": 5}}, {"src": {"terminal": "output", "moduleId": 5}, "tgt": {"terminal": "input", "moduleId": 1}}], "modules": [{"terminals": "", "config": {"files": ["/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC010.SA3_SRK_S110", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC008.SA3_SRK_S108", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC002.SA3_SRK_S102", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC006.SA3_SRK_S106", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC005.SA3_SRK_S105", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/SILIC007.SA3_SRK_S107", "/var/www/DATAFLOW/dataflow/reduction/sans/ncnr_sample_data/PLEX_2NOV2007_NG3.DIV"], "position": [5, 20], "intent": "signal", "xtype": "WireIt.Container"}, "name": "Load", "value": {}}, {"terminals": "", "config": {"position": [500, 500], "ext": "dat", "xtype": "WireIt.Container"}, "name": "Save", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 100], "xtype": "WireIt.ImageContainer"}, "name": "initial_correction", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 200], "xtype": "WireIt.ImageContainer"}, "name": "Correct Detector Sensitivity", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 300], "xtype": "WireIt.ImageContainer"}, "name": "absolute_scaling", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [360, 400], "xtype": "WireIt.ImageContainer"}, "name": "annular_av", "value": {}}], "properties": {"name": "test sans", "description": "example sans data"}}]

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
};

b = {'save':'successful'}


def listWirings(request):
    print 'I am loading'
    return HttpResponse(simplejson.dumps(offspec+a+SANS+SANS_2))

#    return HttpResponse(simplejson.dumps(a)) #andr vs bt7 testing

def saveWiring(request):
    print 'I am saving'
    return HttpResponse(simplejson.dumps(b))

def runReduction(request):
    print 'I am reducing'
####### SANS TESTING
    result = SANS_INS.TESTING()
    #print result
    #for i in range(6):
   #	name = 'checkingSANSresults' + str(i) + '.txt'
   # 	openFile =open(name,'w')
   # 	openFile.write(simplejson.dumps(result[i]))
   # 	openFile.close()
    #result = SANS_INS.TESTING()
    #print simplejson.dumps(result)
    return HttpResponse(simplejson.dumps(result))
    
    #print FILES
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

def displayEditor(request):
    print request.POST.has_key('language')
    if request.POST.has_key('language'):
        return render_to_response('tracer_testingforWireit/editor.html', {'lang':request.POST['language']})
    else:
        return HttpResponseRedirect('/editor/langSelect/')

def languageSelect(request):
    if request.POST.has_key('instruments'):
        return render_to_response('tracer_testingforWireit/editorRedirect.html',
                            {'lang':request.POST['instruments']})
    form = languageSelectForm()
    return render_to_response('tracer_testingforWireit/languageSelect.html', {'form':form})
    
