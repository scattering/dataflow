#Author: Joe Redmon
#urls.py

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from WRed.display.views import *
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from WRed.display.models import DataFile, MetaData

urlpatterns = patterns('',
    (r'^files/all$',all_files),
    (r'^files/all/$',all_files),
    (r'^files/forms/download/$', download),
    (r'^files/forms/download/batch/$', batch_download),
    (r'^files/(\w+)$', view_file),
    (r'^files/json/evaluate/$', evaluate),
    (r'^files/json/evaluate/save/$', evaluate_and_save),
    (r'^files/json/(\w+)/$', json_file_display),
    
    (r'^files/all/json/$', json_all_files),

    (r'^files/all/json_pipelines/$', json_pipelines),
    (r'^files/forms/save_pipeline/$', save_pipeline),

    (r'^files/forms/upload/$', upload_file),
    (r'^files/forms/upload/live/$', upload_file_live),
    (r'^files/forms/delete/$', delete_file),
    (r'^files/pipeline/$', pipeline),
    (r'^files/fitting/(\w+)/$', fitting_request_action),
    
    (r'^(?i)Alex/angleCalculator/', direct_to_template, {'template': 'angleCalculator.html'}),
    
    (r'^(?i)files/calcUBmatrix/', calculateUB),
    (r'^(?i)files/refineUBmatrix/', refineUB),
    (r'^(?i)files/calcTheta/', runcalcTheta),
	(r'^(?i)files/omegaZero/', runcalc1),
    (r'^(?i)files/scatteringPlane/', runcalc2),
    (r'^(?i)files/phiFixed/', runcalc3),
    (r'^(?i)files/latticeParameters/', getLatticeParameters),
    (r'^(?i)files/savingData/', makeSaveFile),
    (r'^(?i)files/downloadingData/', download_file_angleCalc),
    (r'^(?i)files/uploadingData/', upload_file_angleCalc),
)
