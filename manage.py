#!/usr/bin/env python
import sys, os

# put the current directory on the path
path=os.path.dirname(__file__)
sys.path.insert(0, path)

# Make sure UB matrix calculator is compiled and on the path
sys.dont_write_bytecode = True
import run_helper as rh

# Run django
if __name__ == "__main__":
    rh.build('reduction/tas/ubmatrix')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
