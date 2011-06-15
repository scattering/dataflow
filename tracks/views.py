# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

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
	site_list = ['/hello/','/test/']
	return render_to_response('tracer_testingforWireit/home.html', locals())
