import os,sys

if sys.platform=='win32':
    HOMEDIR=r'c:\dataflow'
    REPO_ROOT = os.path.split(HOMEDIR)[-1] 
else:
    HOMEDIR = __file__
    REPO_ROOT = HOMEDIR.split('/')[-2]
ROOT_URLCONF = REPO_ROOT + '.urls'
