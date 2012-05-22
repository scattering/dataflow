#!/usr/bin/python
import sys
from subprocess import Popen, call

# Please run sudo -s before this script.
if __name__ == "__main__":
    apt_commands = ['ipython',
                  'git',
                  'git-doc',
                  'git-core',
                  'git-gui',
                  #'python-django',
                  'python-setuptools',
                  'python-redis',
                  'redis-server',
                  'python-numpy',
                  'python-scipy',
                  'python-matplotlib',
                  'python-dev',
                  'python-simplejson', # no need for easy-install on this one.
	              'python-psycopg2', # this is already being installed from easy_install below - conflicts!!
	              #'python-h5py', #need newer version than is in Ubuntu 10.04
	              'libhdf5-serial-dev',
	              'build-essential',
                  'vim',
                  'subversion',
	              'apache2',
	              'libapache2-mod-wsgi',
	              'postgresql',
	              'pgadmin3',
	              'mercurial',
                  'python-wxgtk2.8', # wx used in offspecular - check version # in future
	              'python-imaging' # not installed by default on UTK server.  go figure.
                  ]
    easy_commands = ['stompservice', 'orbited', '-U Django', '-U psycopg2', 'South', 'django-registration', 'django-profiles', 'h5py', 'wxpython']
    #easy_commands = ['stompservice', 'orbited', '-U Django', 'South', 'django-registration', 'django-profiles']
    merc_commands = ['https://bitbucket.org/ubernostrum/django-registration', 'https://bitbucket.org/ubernostrum/django-profiles']
    
    for command in apt_commands:
        s = 'apt-get -y install %s' % (command,)
        print s
        call(s, shell=True)
        #Popen(['apt-get','install','-y',command])
    call('apt-get build-dep python-psycopg2', shell=True)
    call('easy_install pip', shell=True)
    call('easy_install openopt', shell=True)
    call('easy_install django', shell=True)
    #call('wget http://trac.openopt.org/openopt/changeset/latest/PythonPackages?old_path=%2F&format=zip',shell=True)
    call('svn co svn://openopt.org/PythonPackages OOSuite', shell=True)
    call('cd OOSuite; python install_all.py; cd ..', shell=True)
    for command in merc_commands:
    	call('hg clone %s' % (command,), shell=True) # Default: clones into directory where you're running install.py
    	
    # install the two modules downloaded from mercurial above:
    call('cd django-registration; python setup.py install; cd ..', shell=True)
    call('cd django-profiles; python setup.py install; cd ..', shell=True)

    for command in easy_commands:
        call('pip install %s' % (command,), shell=True)

    # build and install reduction and bumps
    call('cd ~; git clone https://github.com/reflectometry/reduction.git;', shell=True)
    call('cd reduction/; python settings.py build; python settings.py install; cd ..', shell=True)
    call('cd ~; git clone https://github.com/bumps/bumps.git;', shell=True)
    call('cd bumps/; python settings.py build; python settings.py install; cd ..', shell=True)
        

#NOTE: Also install matplotlib and download and install natgrid (https://github.com/matplotlib/natgrid)
#PNOTE: psycopg2 might give you a bit of trouble

