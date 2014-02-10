#!/usr/bin/env python
"""
Usage:

./test.py
    - run all tests

./test.py --with-coverage
    - run all tests with coverage report
"""

import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0,os.path.dirname(__file__))
import run_helper as rh
del sys.path[0]

# rh.build()  # uncomment if program has compiled components
rh.nose(['reduction', 'dataflow', 'test/sample_reduction.py'])