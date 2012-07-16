#Author: Joe Redmon
#views.py
#7/22/10 - Alex Yee added in new downloadangles method.

import os
from django.db.models.signals import post_save, post_delete
from multiprocessing import Queue
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
import simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from WRed.file_parsing.file_operator import *
from WRed.file_parsing.file_read import *
from WRed.fitting import *
from WRed.file_parsing.file_to_json import *
from WRed.display.models import *
from WRed.runcalc import *
from django import forms
import zipfile

import datetime

'''def concat_data(*args):
    print 'concating...'
    out = Data('db/' + DataFile.objects.get(id = args[0]).md5 + '.file')
    for f in args[1:]:
        out = out + Data('db/' + DataFile.objects.get(id = f).md5 + '.file')
    return out
'''

#Tells clients subscribed to channels that an update has occurred
def updated_callback(sender, **kwargs):
    proxy = xmlrpclib.ServerProxy("http://localhost:8045")
    print("transmitting...")
    try:
      proxy.transmit('/updates/files/all', 'Update!!')
      proxy.transmit('/updates/files/' + str(kwargs['instance'].id), 'Update to that file!!')
    except:
      print "transmission failed, error: ",sys.exc_info()[0]
    print "...end of transmission"

#Important! These are the signals connectors so that every time a DataFile is saved
#or deleted, the updated_callback method is called to send out the signal that something
#has changed
post_save.connect(updated_callback, sender = DataFile)
post_delete.connect(updated_callback, sender = DataFile)

class ViewFileForm(forms.Form):
    md5 = forms.CharField(max_length = 32)
class UploadFileForm(forms.Form):
    file = forms.FileField()
class UploadLiveFileForm(forms.Form):
    file = forms.FileField()
    proposalid = forms.CharField(max_length = 100)
    filename = forms.CharField(max_length = 100)
class DeleteFileForm(forms.Form):
    ids = forms.CharField(max_length = 10000)
class DownloadFileForm(forms.Form):
    id = forms.IntegerField()
class DownloadBatchForm(forms.Form):
    ids = forms.CharField(max_length = 10000)
class WaitForUpdateForm(forms.Form):
    pass
class EvaluateEquationForm(forms.Form):
    equation = forms.CharField(max_length = 1000)
class EvaluateSaveEquationForm(forms.Form):
    equation = forms.CharField(max_length = 1000)
    file_name = forms.CharField(max_length = 200)
class SavePipelineForm(forms.Form):
    name = forms.CharField(max_length = 50)
    pipeline = forms.CharField(max_length = 10000)
#Handles GET requests for individual files, returns a json object of the data file
@login_required
def json_file_display(request, idNum):
    print 'USERNAME: ',request.user.username
    print 'Authenticated: ', request.user.is_authenticated()
    rFile = DataFile.objects.get(id = idNum)
    if request.user.is_authenticated() and (request.user.username == str(rFile.proposal_id) or request.user.is_superuser):
        print 'Good To Go!'
        data = get_object_or_404(DataFile, id = idNum)
        md5 = data.md5
        all_objects = displayfile('db/' + md5 + '.file')
        data = simplejson.dumps(all_objects)
        return HttpResponse(data)
    else:
        print 'Not authenticated!'
    return HttpResponse('Go Login!')

#Handles GET requests for all file information, returns a json object of the files
@login_required
def json_all_files(request):
    files = DataFile.objects.filter(proposal_id = request.user.username)
    if request.user.is_superuser: files = DataFile.objects.all()
    variables = [['File Name','md5', 'id']]
    maxv = []
    minv = []
    for f in files:
        metadata = f.metadata_set.all()
        a = ['N/A'] * len(variables[0])
        for m in metadata:
            if m.field in variables[0]:
                pass
            else:
                variables[0].append(m.field)
                a.append('N/A')
            a[variables[0].index(m.field)] = str(m.low) + ',' + str(m.high)
            maxv.extend(['N/A']*(len(variables[0]) - len(maxv)))
            minv.extend(['N/A']*(len(variables[0]) - len(minv)))
            if maxv[variables[0].index(m.field)] == 'N/A': maxv[variables[0].index(m.field)] = m.high
            if minv[variables[0].index(m.field)] == 'N/A': minv[variables[0].index(m.field)] = m.low
            maxv[variables[0].index(m.field)] = max(m.high, maxv[variables[0].index(m.field)])
            minv[variables[0].index(m.field)] = min(m.low, minv[variables[0].index(m.field)])
            a[0] = f.name
            a[1] = f.md5
            a[2] = f.id
        variables.append(a)
    if(len(maxv) >0):
        maxv[0] = 'Max Values'
        minv[0] = 'Min Values'
    else:
        maxv.append('Max Values')
        minv.append('Min Values')
    variables.insert(1,maxv)
    variables.insert(2,minv)
    for row in variables[1:]:
        row.extend(['N/A']*(len(variables[0]) - len(row)))
    return HttpResponse(simplejson.dumps(variables))

@login_required
def json_pipelines(request):
    pipelines = Pipeline.objects.filter(proposal_id = request.user.username)
    json = []
    for p in pipelines:
        json.append({'name': p.name, 'pipeline' :p.pipeline})
    return HttpResponse(simplejson.dumps(json))
    
@login_required
def save_pipeline(request):
    json = {
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        print "Live Data Post Request"
        form = SavePipelineForm(request.POST, request.FILES)
        if form.is_valid():
            p = Pipeline(proposal_id = request.user.username, name = request.POST['name'], pipeline = request.POST['pipeline'])
            p.save()
            json['success'] = True
    return HttpResponse(simplejson.dumps(json))
    
#Handles POST requests to upload an input file for angleCalculator.js   
def upload_file_angleCalc(request):
    json = {
        'errors': {},
        'data': {},
        'success': False,
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #print form.is_valid()
        if form.is_valid():
            print request.FILES['file'].name
            filename = request.FILES['file'].name
            fid = request.FILES['file'].open()
            #content = request.FILES['file'].read()            
            #fid = open('/tmp/upload', 'w')
            #fid.write(content)
            #fid.close()
            
            #uploadarray = uploadInputFile ('/tmp/upload')
            uploadarray = uploadInputFile (request.FILES['file'])
            json['success'] = True
            json['data'] = {'array': uploadarray}
        else:
            return HttpResponse('not valid. Form:', form)
    else:
        return HttpResponse('method != POST')
        
    #returns a dictionary with 'data' = dictionary with 'array' = array of dictionaries created from uploadInputFile method.
    return HttpResponse(simplejson.dumps(json))
    
#Handles GET requests to download a save file for angleCalculator.js
def download_file_angleCalc(request):
    if request.method == 'GET':
        
        data = file('/tmp/angleCalculatorData.txt')
        response = HttpResponse(data, mimetype='application/force-download')
        response['Content-Disposition'] = 'attachment; filename= angleCalculatorData.txt'
        return response
    else:
        return HttpResponse('method != GET')
    
    
#Handles POST requests to upload static files (cannot be update or changed later)
@login_required
def upload_file(request):
    json = {
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print '**********VALID********, User Name:', request.user.username

            handle_uploaded_file(request.FILES['file'], request.user.username)
            json['success'] = True
            json['text'] = {'file':request.FILES['file'].name}
        else:
            print '**********INVALID********'
    else:

        return HttpResponse('Get Outta Here!')
    return HttpResponse(simplejson.dumps(json))
    
#Handles POST requests to upload live files (files that may be updated or changed later)
def upload_file_live(request):
    print "Live Data Request"
    json = {
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        print "Live Data Post Request"
        form = UploadLiveFileForm(request.POST, request.FILES)
        if form.is_valid():
            print '**********Live Data:VALID********'
            handle_uploaded_live_file(request.FILES['file'], request.POST['filename'], request.POST['proposalid'])
            json['success'] = True
            json['text'] = {'file':request.FILES['file'].name}
        else:
            print '**********INVALID********'
    else:

        return HttpResponse('Get Outta Here!')
    return HttpResponse(simplejson.dumps(json))
#handles POST requests to delete files from the database
@login_required
def delete_file(request):
    json = {
        'file': {},
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        form = DeleteFileForm(request.POST, request.FILES)
        ids = simplejson.loads(request.POST['ids'])
        for i in ids:
            rFile = DataFile.objects.get(id = i)
            print form.is_valid() , request.user.is_authenticated() , request.user.username == str(rFile.proposal_id) , request.user.is_superuser
            if form.is_valid() and request.user.is_authenticated() and (request.user.username == str(rFile.proposal_id) or request.user.is_superuser):
                DataFile.objects.get(id=i).delete()
                print os.path.join('db', rFile.md5 + '.file')
                os.remove(os.path.join('db', rFile.md5 + '.file'))
                json['success'] = True
            else:
                print 'invalid'
    else:
        return HttpResponse('Go Away!')
    return HttpResponse(simplejson.dumps(json))
@login_required
def all_files(request):
    return render_to_response('all_files.html')
@login_required
def pipeline(request):
    return render_to_response('pipeline.html')
@login_required
def evaluate(request):
    json = {
        'file': {},
        'errors': {},
        'text': {},
        'success': False,
    }
    print 'evaluate'
    if request.method == 'GET':
        form = EvaluateEquationForm(request.GET, request.FILES)
        if form.is_valid():
            print 'evaluating: ', request.GET['equation']
            eq = request.GET['equation']
            eq = eq.split();
            for i in range(len(eq)):
                try:
                    eq[i] = 'Data("db/" + DataFile.objects.get(id = ' + str(int(eq[i])) + ').md5 + ".file")'
                except ValueError:
                    print eq[i]
                    if eq[i] not in ['(', ')', '.add(','.detailed_balance()','.sub(',').sub(',',']:
                        if (eq[i][0] == "'" and eq[i][-1] == "'"):
                            for s in eq[i][1:-2]:
                                if s == "'":
                                    return HttpResponse('Stop haxing me!')
                        elif (eq[i][0:13] == '.scalar_mult(' and eq[i][-1] == ')'):
                            try:
                                float(eq[i][13:-1])
                            except:
                                return HttpResponse('Stop haxing me!')
                        elif (eq[i][0:12] == '.scalar_add(' and eq[i][-1] == ')'):
                            print eq[i][12:-1]
                            try:
                                float(eq[i][12:-1])
                            except:
                                return HttpResponse('Stop haxing me!')
                            
                        else:
                            return HttpResponse('Stop haxing me!')
            print '...................evaling..................'
            parsed_eq = eq[0]
            for a in eq[1:]:
                parsed_eq += ' ' + a
            print parsed_eq
            return HttpResponse(simplejson.dumps(displaystring(eval(parsed_eq).__str__())))
    return HttpResponse(simplejson.dumps(json))
@login_required
def evaluate_and_save(request):
    json = {
        'file': {},
        'errors': {},
        'text': {},
        'success': False,
    }
    print 'evaluate'
    if request.method == 'GET':
        form = EvaluateSaveEquationForm(request.GET, request.FILES)
        if form.is_valid():
            print 'evaluating: ', request.GET['equation']
            eq = request.GET['equation']
            eq = eq.split();
            for i in range(len(eq)):
                try:
                    eq[i] = 'Data("db/" + DataFile.objects.get(id = ' + str(int(eq[i])) + ').md5 + ".file")'
                except ValueError:
                    pass
            parsed_eq = eq[0]
            for a in eq[1:]:
                parsed_eq += ' ' + a
            print parsed_eq
            eval(parsed_eq + '.write("db/temp_eval")')
            addfile('db/temp_eval',request.GET['file_name'], request.user.username,False)
            json['success'] = True
            return HttpResponse(simplejson.dumps(json))
    return HttpResponse(simplejson.dumps(json))

@login_required
def view_file(request, idNum):
    return render_to_response('view_file.html', {'id': idNum})
    
@login_required
def download(request):
    if request.method == 'GET':
        form = DownloadFileForm(request.GET, request.FILES)
        print request.GET['id']
        rFile = DataFile.objects.get(id = request.GET['id'])
        if form.is_valid() and request.user.is_authenticated() and (request.user.username == str(rFile.proposal_id) or request.user.is_superuser):
            print 'Good To Go!'
            md5 = rFile.md5
            data = file('db/' + md5 + '.file')
            response = HttpResponse(data, mimetype='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=' + rFile.name
            return response
        else:
            print 'Not authenticated!'
    return HttpResponse('Go Login!')

@login_required
def batch_download(request):
    if request.method == 'GET':
        form = DownloadBatchForm(request.GET)
        file_ids = simplejson.loads(request.GET['ids'])
        valid = form.is_valid()
        for i in file_ids:
            if request.user.is_authenticated() and (request.user.username == str(DataFile.objects.get(id = i).proposal_id) or request.user.is_superuser):
                pass
            else:
                valid = False
        if(valid):
            z = zipfile.ZipFile('db/temp.zip', 'w')
            for i in file_ids:
                z.write('db/' + DataFile.objects.get(id = i).md5 + '.file', DataFile.objects.get(id = i).name)
            z.close()
            data = file('db/temp.zip')
            response = HttpResponse(data, mimetype='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=temp.zip'
            return response
            

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print 'Proposal ID: ', username, 'Tag: ', password
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            print '********LOGIN SUCCESSFUL*********'
            auth.login(request, user)
            return HttpResponseRedirect(request.GET.get('next'))
        else:
            return HttpResponse('Go Away!')
    elif request.method == 'GET':
        return render_to_response('registration/login.html')
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')
