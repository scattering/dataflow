from django.conf.urls.defaults import patterns, include, url
#from tracks.views import xhr_test, mytest, home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

## PULLS VIEWS FROM TRACKS/VIEWS
## WE WOULD LIKE IT TO PULL FROM APPS/TRACKS/VIEWS
from django.conf import settings

urlpatterns = patterns(settings.REPO_ROOT + '.apps.tracks.views', 
		('^hello/$', 'xhr_test'),
		('^test/$','mytest'),
		('^listWirings/$', 'listWirings'),
		
		# Wiring editor display urls
		('^editor/$', 'displayEditor'),
		('^editor/langSelect/$', 'languageSelect'),

		# Wiring editor adapter urls
		('^editor/listWirings/$', 'listWirings'),
		('^editor/saveWiring/$', 'saveWiring'),
		('^editor/runReduction/$', 'runReduction'),

		('', 'home'),
    # Examples:
    # url(r'^$', 'dataflow.views.home', name='home'),
    # url(r'^dataflow/', include('dataflow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
