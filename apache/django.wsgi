import os, sys

#having trouble with relative imports, so using this is as a (temp) fix
PROJ_NAM =  __file__.split('/')[-3]
DIR_PATH = __file__[:-27] #includes a final '/'
#print 'proj', PROJ_NAM
#print 'dir', DIR_PATH

sys.path = [DIR_PATH,DIR_PATH+PROJ_NAM, DIR_PATH+PROJ_NAM +'/apps/tracks'] + sys.path
sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = PROJ_NAM + '.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
