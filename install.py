#!/usr/bin/python
import sys
from subprocess import Popen, call

# Please run sudo -s before this script.
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
        s='apt-get -y install %s'%(command,)
        print s
        call(s,shell=True)
        #Popen(['apt-get','install','-y',command])
    
    call('easy_install pip',shell=True)
    for command in easy_commands:
        call('pip install %s'%(command,),shell=True)


