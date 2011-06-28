import os

HOMEDIR = __file__
REPO_ROOT = HOMEDIR.split('/')[-2]
ROOT_URLCONF = REPO_ROOT + '.urls'
