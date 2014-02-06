#!/usr/bin/env python
import imp, sys, os
from django.core.management import execute_from_command_line

#try:
#   imp.find_module('settings') # Assumed to be in the current directory.
#except ImportError:
#    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
#    sys.exit(1)

# put the current directory on the path
sys.path.insert(0, os.path.dirname(settings.__file__))
import settings

if __name__ == "__main__":
    execute_from_command_line(settings)
