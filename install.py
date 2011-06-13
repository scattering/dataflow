#!/usr/bin/python
import sys
from subprocess import Popen

if __name__=="__main__":
    apt_commands=['ipython',
                  'git',
                  'git-doc',
                  'git-core',
                  'git-gui',
                  'python-django',
                  'python-setuptools',
                  'python-numpy',
                  'python-scipy',
                  'python-dev',
                  ]
    easy_commands=['simplejson','openopt','stompservice','orbited']
    
    for command in apt_commands:
        Popen(['apt-get','install',command])
        
    for command in easy_commands:
        Popen(['apt-get','install',command])

