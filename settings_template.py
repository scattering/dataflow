# =============================================================================
# *****************************************************************************
#
# Private configuration
#
# A private configuration file is needed for information such as e-mail
# host and passwords and database passwords.  This will be retrieved from
# ~/.APPNAME/settings.py (unix) or C:\APPNAME\settings.py (windows) when
# the server is run in production mode.
#
# The settings will be loaded after all other settings, so it may override
# anything in apps.settings.
#
# Put the server in production mode by setting DJANGO_PRODUCTION=1 in the
# environment.
#
# *****************************************************************************
# =============================================================================
import os
APPNAME="tracks"

# Site name/domain will be plugged into the database on resetdb.sh.  To change
# it you will need to set
#
SITE_NAME=""

DATA_DIR = os.path.expanduser('/var/lib/%s'%APPNAME)
CACHE_DIR = os.path.expanduser('/var/cache/%s'%APPNAME)
LOG_FILE = os.path.expanduser('/var/log/%s'%APPNAME)
SECRET_KEY_FILE = os.path.join(DATA_DIR, 'secret.txt'%APPNAME)
os.environ['MPLCONFIGDIR'] = os.path.join(CACHE_DIR, '.matplotlib/')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'accounts@drneutron.org'
EMAIL_HOST_PASSWORD = '<enter email password>'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'accounts@drneutron.org <accounts@drneutron.org>'

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Use 'postgresql_psycopg2', 'postgresql', 'mysql', or 'oracle'.
DB = dict(ENGINE='django.db.backends.postgresql_pyscopg2',
          NAME=APPNAME,
          USER=APPNAME,
          PASSWORD = '<enter database password>',
          HOST='',  # empty string for localhost
          PORT='',  # empty string for localhost
          )
DATABASES = { 'default': DB }

REDIS_HOST = 'localhost'

SITE_NAME = "Dr. Neutron's Diet Tablets (for reduction)!"
SITE_DOMAIN = 'www.drneutron.org'
ALLOWED_HOSTS = ['.drneutron.org']

TIME_ZONE = 'America/New_York'
