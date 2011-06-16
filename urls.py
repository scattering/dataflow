from django.conf.urls.defaults import patterns, include, url
#from tracks.views import xhr_test, mytest, home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('repo.tracks.views', 
		('^hello/$', 'xhr_test'),
		('^test/$','mytest'),
		('^listWirings/$', 'listWirings'),
		('^editor/$', 'displayEditor'),
		('^editor/listWirings/$', 'listWirings'),
		('', 'home'),
    # Examples:
    # url(r'^$', 'dataflow.views.home', name='home'),
    # url(r'^dataflow/', include('dataflow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
