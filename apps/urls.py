
from django.conf.urls import patterns, include, url
#from tracks.views import xhr_test, mytest, home

def allow_admin(baseurl='admin', docs=True):
    """
    Url patterns for admin access.

    Call to add admin support to the app.
    """
    from django.contrib import admin
    admin.autodiscover()
    urls = []
    if docs:
        urls += patterns('', url(r'^%s/doc/'%baseurl, include('django.contrib.admindocs.urls')))
    urls += patterns('', url('^%s/'%baseurl, admin.site.urls))
    return urls

urlpatterns = []

# Uncomment the following line for admin support.  Also need to uncomment
# lines in settings.py
urlpatterns += allow_admin(baseurl="admin", docs=True)

# userena account access urls
#urlpatterns += url(r'^accounts/', include('userena.urls'))
#urlpatterns += url(r'^tracks/', include('tracks.urls'))

# tracks application urls
urlpatterns += patterns(
    'apps.tracks.views',
    ('^$', 'home'),
    ('^index.html$', 'home'),


    ('^listWirings/$', 'listWirings'),
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

)

