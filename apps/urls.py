
from django.conf.urls import patterns, include, url
#from tracks.views import xhr_test, mytest, home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    'apps.tracks.views',
    ('^accounts/', include('userena.urls')),
    #('^login/$', 'django.contrib.auth.views.login'),

    ('^hello/$', 'xhr_test'),
    ('^test/$', 'mytest'),
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
    
    #collaboration
    ('^project/collaborate/$', 'email_collaborator'),
    #('^project/join_collaboration/(?P<email_address>\[A-Za-z0-9_@.]+)/(?P<activation_key>\w+)$', 'add_collaborator'),
    ('^project/join_collaboration/(?P<email_activation_key>.+)$', 'add_collaborator'),

    # nd-plot interactor calculations
    ('^calculateSlice/', 'calculate_segment_interactor'),

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

    # FTP side loader
    ('^FTPloader/$', 'showFTPloader'),
    ('^loadFiles/getFTPdirs/', 'getFTPdirectories'),
    ('^uploadFTPFiles/$', 'uploadFTPFiles'),

    # File loader display urls (testing, 7/6)
    ('^loadFiles/$', 'displayFileLoad'),
    ('^saveUpdate/$', 'return_files_metadata'),

    # user projects/experiments/instruments/files interactions
    ('^projects/$', 'projects'),
    ('^projects/editProject/(?P<project_id>\d+)/$', 'editProject'),
    ('^projects/editProject/\d+/editExperiment/(?P<experiment_id>\d+)', 'editExperiment'),
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
                        #(r'^profiles/', include('profiles.urls')),
                        (r'', 'apps.tracks.views.home'),

                        )
