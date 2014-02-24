# Django settings for dataflow project.
#
# Local settings are stored ROOT/private_settings.py (for deployment) or
# ROOT/debug_settings.py (for debugging).  Copy ROOT/settings_template.py
# over these files to override the settings.
#
# The default path when debugging is /tmp/APPNAME on unix-like systems, or
# c:\APPNAME-debug on windows.  The deployed system may use the standard
# unix directories /var/log, /var/cache and /var/lib, or it may use
#
# The server secret key for encrypted data is stored in secret.txt
import os,sys
import stat

APPNAME = 'tracks'
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DEBUG = 'DJANGO_PRODUCTION' not in os.environ

# =============================================================================
# *****************************************************************************
# Server configuration
# *****************************************************************************
# =============================================================================

# Default private configuration for debug server
WIN = sys.platform.startswith('win')
if WIN: data_root = (r'c:\%s-debug' if DEBUG else r'c:\%s')%APPNAME
else: data_root = '/tmp/%s'%APPNAME
DATA_DIR = os.path.join(data_root, 'data')
CACHE_DIR = os.path.join(data_root, 'cache')
LOG_FILE = os.path.join(data_root, 'error.log')
SECRET_KEY_FILE = os.path.join(data_root, 'secret.txt')
os.environ['MPLCONFIGDIR'] = os.path.join(ROOT, '.matplotlib/')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DATABASES = {'default': dict(ENGINE='django.db.backends.sqlite3',
                             NAME=os.path.join(data_root, 'user.db'))}
SITE_NAME = 'tracks debug'
SITE_DOMAIN = 'localhost:8000'
REDIS_HOST = 'localhost'
ALLOWED_HOSTS = ['localhost']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level':'ERROR',
            'class':'logging.StreamHandler',
            #'formatter': 'simple'
        },
        'file': {
            'level':'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

# =============================================================================
# *****************************************************************************
# Application configuration
# *****************************************************************************
# =============================================================================



ROOT_URLCONF = 'apps.urls'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# The userena package uses MEDIA_ROOT/mugshots to store mugshots
MEDIA_ROOT = os.path.join(DATA_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(ROOT,'static').replace('\\','/'),
                    # Put strings here, like "/home/html/static" or "C:/www/django/static".
                    # Always use forward slashes, even on Windows.
                    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


TEMPLATE_DIRS = (os.path.join(ROOT,'site-templates').replace('\\','/'),
                 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
                 # Always use forward slashes, even on Windows.
                 # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    # I do not have this file
    'django.contrib.staticfiles',

    'apps.tracks',
    'apps.accounts',
    'south',
    # Uncomment the next lines to enable the admin and admindocs.  Also need
    # to uncomment admin support in urls.py
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Account management
    'userena',
    'guardian',
    'easy_thumbnails',
)

# Account management settings, with userena and guardian
# See: http://docs.django-userena.org/en/latest/settings.html
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_URL = '/accounts/signin/'
#LOGIN_REDIRECT_URL = '/'
#LOGOUT_URL = '/'
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_ACTIVATION_DAYS = 2
USERENA_WITHOUT_USERNAMES = True
# Also requires email backend



# =============================================================================
# *****************************************************************************
# Private settings
# *****************************************************************************
# =============================================================================

PRIVATE_FILE = 'debug_settings.py' if DEBUG else 'private_settings.py'
PRIVATE_FILE = os.path.abspath(os.path.join(ROOT, PRIVATE_FILE))
if os.path.exists(PRIVATE_FILE):
    mode = os.stat(PRIVATE_FILE).st_mode
    #print "mode %o %o"%(mode,stat.S_IRUSR|stat.S_IWUSR)
    if mode&0o777 != stat.S_IRUSR|stat.S_IWUSR:
        print "Halt. %r is readable by group/others"%PRIVATE_FILE
        sys.exit()
    if DEBUG:
        from debug_settings import *
        del mode, sys.modules['debug_settings']
    else:
        from private_settings import *
        del mode, sys.modules['private_settings']
    LOGGING['handlers']['file']['filename'] = LOG_FILE
del PRIVATE_FILE

from apps.keygen import get_key
SECRET_KEY = get_key(SECRET_KEY_FILE)
