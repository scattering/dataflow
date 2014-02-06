import os, sys

PROJ_PATH = os.path.dirname(os.path.dirname(__file__))
PROJ_NAM =  os.path.basename(PROJ_PATH)

sys.path.insert(0,PROJ_PATH)
sys.path.append(os.path.join(PROJ_PATH, 'apps', 'tracks'))

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = PROJ_NAM + '.settings'
os.environ['MPLCONFIGDIR'] = os.path.join(PROJ_PATH, '.matplotlib/')
import django.core.handlers.wsgi as wsgi
application = wsgi.WSGIHandler()
