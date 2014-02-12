#!/usr/bin/env python
"""
Helper for running code and tests in place.
"""

import os, sys
import contextlib
import inspect



from distutils.util import get_platform
PLATFORM = '.%s-%s'%(get_platform(),sys.version[:3])
_caller_file = inspect.getmodule(inspect.stack()[1][0]).__file__
ROOT = os.path.abspath(os.path.dirname(_caller_file))
BUILD_PATH = os.path.join('build','lib'+PLATFORM)


def find(pattern, *paths):
    import fnmatch
    matches = []
    if not paths: paths = ['.']
    for path in paths:
        for root, dirnames, filenames in os.walk(os.path.join(ROOT,path)):
              for filename in fnmatch.filter(filenames, pattern):
                  matches.append(os.path.join(root, filename))
    return matches

def debug_numpy_warnings():
    """
    Turn numpy warnings into exceptions
    """
    import numpy
    numpy.seterr(all='raise')

def setup_pylab():
    """
    Prepare .mplconfig directory and set default plotter to 'Agg'
    """
    mplconfig = os.path.join(os.getcwd(), '.mplconfig')
    os.environ['MPLCONFIGDIR'] = mplconfig
    if not os.path.exists(mplconfig): os.mkdir(mplconfig)
    import matplotlib
    matplotlib.use('Agg')
    #print(matplotlib.__file__)
    import pylab; pylab.hold(False)

def addpath(path):
    """
    Add a directory to the python path environment, and to the PYTHONPATH
    environment variable for subprocesses.  Paths are relative to the root
    of the project.
    """
    path = os.path.abspath(os.path.join(ROOT,path))
    if 'PYTHONPATH' in os.environ:
        PYTHONPATH = path + os.pathsep + os.environ['PYTHONPATH']
    else:
        PYTHONPATH = path
    os.environ['PYTHONPATH'] = PYTHONPATH
    sys.path.insert(0, path)

sys.stderr = sys.stdout # Doctest doesn't see sys.stderr


def check_in_root():
    """Check that we are running from the root."""
    working_dir = os.path.abspath(os.getcwd())
    assert ROOT == working_dir

@contextlib.contextmanager
def pushdir(path="."):
    """
    Do work in a subdirectory, then return.
    """
    old_path = os.getcwd()
    os.chdir(os.path.join(ROOT,path))
    yield
    os.chdir(old_path)

def build(package="."):
    """
    Run setup.py in directory package relative to root.  Default is to build
    the current project.
    """
    import subprocess

    with pushdir(package):
        # Build the package
        print("-"*70)
        print("Building %s ..."%os.path.basename(os.getcwd()))
        print("-"*70)
        subprocess.call((sys.executable, "setup.py", "build"), shell=False)
        print("-"*70)
        # Add the package build directory to the path
        addpath(os.path.join(os.getcwd(), BUILD_PATH))

_FIRST_TEST = True
def nose(trees, args=[], docext='.rst', docpath='.'):
    """
    Run nose.

    Check all modules for functions like *test_fn*, *_test_fn*, *fn_test*,
    or plain *test*.

    Unless *docext=None*, add doctest to the nose command.
    """
    import nose
    nose_args = ['-v', '--all-modules',
                 '-m(^_?test_|_test$|^test$)',
                 ]
    # Assume trees is a list of packages to test
    for t in trees:
        if not '/' in t and not '.' in t:
            nose_args.append('--cover-package='+t)
    # Clear the coverage data before the first test
    if _FIRST_TEST: nose_args += ['--cover-erase']
    if docext:
        nose_args += [
            '--with-doctest', '--doctest-extension=%s'%docext,
            '--doctest-options=+ELLIPSIS,+NORMALIZE_WHITESPACE',
        ]
        nose_args += find('*'+docext, docpath)

    nose_args += args
    nose_args += sys.argv[1:]  # allow coverage arguments

    # Add targets
    nose_args += [os.path.join(ROOT,t) for t in trees]

    print("nosetests "+" ".join(nose_args))
    if not nose.run(argv=nose_args): sys.exit(1)

