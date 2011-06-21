# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

def xhr_test(request):
        print request
	if request.is_ajax():
        	if request.method == 'GET':
            		message = "This is an XHR GET request"
            	elif request.method == 'POST':
                	message = "This is an XHR POST request"
            		# Here we can access the POST data
           	 	print request.POST
    	else:
        	message = "No XHR"
	return HttpResponse(message)

def mytest(request):
       return render_to_response('tracer_testingforWireit/xhr_temp.html')

def home(request):
	site_list = ['/hello/','/test/', '/editor/']
	return render_to_response('tracer_testingforWireit/home.html', locals())

a = [{"name":"TASWires","wires": [{"src": {"terminal": "output", "moduleId": 0}, "tgt": {"terminal": "input", "moduleId": 1}}, {"src": {"terminal": "output", "moduleId": 1}, "tgt": {"terminal": "input", "moduleId": 2}}, {"src": {"terminal": "output", "moduleId": 2}, "tgt": {"terminal": "input", "moduleId": 3}}], "modules": [{"terminals": "", "config": {"position": [5, 20], "xtype": "WireIt.Container"}, "name": "Load", "value": {}}, {"terminals": {"input": [-15, 1, -1, 0], "output": [15, 1, 1, 0]}, "config": {"position": [160, 20], "xtype": "WireIt.ImageContainer"}, "name": "Join", "value": {}}, {"terminals": {"input": [0, 10, -1, 0], "output": [20, 10, 1, 0]}, "config": {"position": [280, 40], "xtype": "WireIt.ImageContainer"}, "name": "Scale", "value": {}}, {"terminals": "", "config": {"position": [340, 40], "xtype": "WireIt.Container"}, "name": "Save", "value": {}}], "properties": {"name": "test tas", "description": "example TAS diagram"}}]

def listWirings(request):
        print 'I am loading'
	return HttpResponse(simplejson.dumps(a))

def saveWiring(request):
	print 'I am saving'
	return HttpResponse('Save')

def displayEditor(request):
	return render_to_response('tracer_testingforWireit/editor.html')
