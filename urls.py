
from django.conf.urls.defaults import patterns, include, url
#from tracks.views import xhr_test, mytest, home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
REPO_ROOT=settings.REPO_ROOT


urlpatterns = patterns(REPO_ROOT + '.apps.tracks.views',
    ('^hello/$', 'xhr_test'),
    ('^test/$', 'mytest'),
    #('^login/$', 'django.contrib.auth.views.login'),
    ('^listWirings/$', 'listWirings'),
    ('^interactors/$', 'showInteractors'),
    ('^plotWindow/$', 'showPlotWindow'),
    ('^sliceWindow/$', 'showSliceWindow'),
    ('^uploadFiles/$', 'uploadFiles'),
    ('^filesExist/$', 'filesExist'),
    ('^getBinaryData/', 'getBinaryData'),
    ('^json/$','return_data'),
    ('^metadatajson/$', 'return_metadata'),
    ('^test_table/$','testTable'),

    # Wiring editor display urls
    ('^editor/$', 'displayEditor'),
    ('^editor/langSelect/$', 'languageSelect'),

    # Wiring editor adapter urls
    ('^editor/listWirings/$', 'listWirings'),
    ('^editor/saveWiring/$', 'saveWiring'),
    ('^editor/runReduction/$', 'runReduction'),
    ('^editor/saveData/$', 'saveData'),
    ('^editor/uploadFiles/$', 'uploadFiles'),
    ('^editor/getCSV/$', 'getCSV'),


    # File loader display urls (testing, 7/6)
    ('^loadFiles/$', 'displayFileLoad'),
    ('^loadFiles/getNCNRdirs/', 'getNCNRdirectories'),
    ('^saveUpdate/$', 'return_files_metadata'),

    # user projects/experiments/instruments/files interactions
    ('^myProjects/$', 'myProjects'),
    ('^myProjects/editProject/(?P<project_id>\d+)/$', 'editProject'),
    ('^myProjects/editProject/\d+/editExperiment/(?P<experiment_id>\d+)', 'editExperiment'),
    ('^editProject/editExperiment/$', 'editExperiment'),


    # Examples:
    # url(r'^$', 'dataflow.views.home', name='home'),
    # url(r'^dataflow/', include('dataflow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        (r'', include('registration.urls')),
                        (r'^profiles/', include('profiles.urls')),
                        (r'', REPO_ROOT + '.apps.tracks.views.home'),

                        )
