import os, sys

sys.path = ['/home/andrew/DATAFLOW/dataflow', '/home/andrew/DATAFLOW/dataflow/apps/tracks'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'dataflow.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
