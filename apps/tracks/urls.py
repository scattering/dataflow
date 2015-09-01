from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # user projects/experiments/instruments/files interactions
    (r'^project/view/$', 'view_projects'),
    (r'^project/edit/(?P<project_id>\d+)/$', 'edit_project'),
    (r'^project/experiments/$', 'view_experiments'),
    (r'^experiment/edit/(?P<experiment_id>\d+)', 'edit_experiment'),
)
