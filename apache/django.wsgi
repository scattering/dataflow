import os, sys

#having trouble with relative imports, so using this is as a (temp) fix
PROJ_PATH = os.path.dirname(os.path.dirname(__file__))
PROJ_NAM =  os.path.basename(PROJ_PATH)
#PROJ_NAM = 'dataflow'
DIR_PATH = os.path.dirname(PROJ_PATH)
#print 'proj', PROJ_NAM
#print 'dir', DIR_PATH

sys.path.append(DIR_PATH)
sys.path.append(PROJ_PATH)
sys.path.append(os.path.join(PROJ_PATH, 'apps', 'tracks'))

#sys.path = [DIR_PATH,DIR_PATH+PROJ_NAM, DIR_PATH+PROJ_NAM +'/apps/tracks'] + sys.path
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = PROJ_NAM + '.settings'
os.environ['MPLCONFIGDIR'] = os.path.join(PROJ_PATH, '.matplotlib/')
import django.core.handlers.wsgi as wsgi
application = wsgi.WSGIHandler()
