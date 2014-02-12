#!/usr/bin/env python
import sys, os
from django.core.management import execute_from_command_line

sys.dont_write_bytecode = True
# put the current directory on the path
sys.path.insert(0, os.path.dirname(__file__))

# Make sure UB matrix calculator is compiled
import run_helper as rh
rh.build('reduction/tas/ubmatrix')

# Run django
import settings
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
