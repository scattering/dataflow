#!/bin/bash

# Remove the default user database for the debug user
rm /tmp/tracks/user.db

# Create an empty database.  The --noinput suppresses the request to create
# an admin user, which is instead created by the filldb command.
python manage.py syncdb --noinput

# Fill in the instruments by running apps.tracks.management.commands.filldb
# In debug mode, this also creates the default admin user
python manage.py filldb

# User profile management through userena uses migrate to create its tables
python manage.py migrate

# userena requires check_permissions to set the correct table permissions
python manage.py check_permissions
