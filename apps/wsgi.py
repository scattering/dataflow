import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(0,os.path.join(ROOT,'reduction','tas','ubmatrix'))
sys.path.insert(0,ROOT)

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_PRODUCTION'] = '1'
import django.core.handlers.wsgi as wsgi
application = wsgi.WSGIHandler()
