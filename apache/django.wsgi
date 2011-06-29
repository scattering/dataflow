import os, sys

sys.path = ['var/www/DATAFLOW','var/www/DATAFLOW/dataflow', '/var/www/DATAFLOW/dataflow/apps/tracks'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'dataflow.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
