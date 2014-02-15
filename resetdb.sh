#!/bin/bash

rm /tmp/tracks/user.db
python manage.py syncdb
python manage.py migrate
python manage.py check_permissions