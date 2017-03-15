"""Production settings and globals."""

from __future__ import absolute_import
import os
from os.path import join

from .base import *


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']
########## END SECRET CONFIGURATION

DEBUG = bool(int(os.environ.get('DJANGO_DEBUG'), False))

SITENAME = "geoconnect"

SITEURL = os.environ['HEROKU_SITEURL'] # e.g. "https://geoconnect-dev.herokuapp.com"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
#
STATIC_ROOT = join(SITE_ROOT, 'staticfiles') #join(SITE_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
#
STATICFILES_DIRS = (
    join(SITE_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#MEDIA_ROOT = '/var/www/geoconnect/media/'   #' join(GEOCONNECT_FILES_DIR, 'media' )

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
#ROOT_URLCONF = '%s.urls' % SITE_NAME
ROOT_URLCONF = 'geoconnect.urls_prod'

########## END URL CONFIGURATION

ADMINS = [('Raman', 'raman_prasad@harvard.edu'),]


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', None)

########## END EMAIL CONFIGURATION

# -----------------------------------
# Site ID
# -----------------------------------
SITE_ID = 1

########## DATABASE CONFIGURATION
# Update database configuration with $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


# Set Template debug to False
try:
    TEMPLATES[0]['OPTIONS']['debug'] = False
except:
    assert False, """Make sure TEMPLATES list is set with 1 entry that has an OPTIONS dict.
e.g. TEMPLATES = [ { 'OPTIONS' : { 'debug' : False }}]"""


# -----------------------------------
# INTERNAL_IPS for admin access
# -----------------------------------
INTERNAL_IPS = ['140.247', # Harvard
                '65.112',  # Harvard
                '10.252']  # Internal IP


########## SESSION_COOKIE_NAME
SESSION_COOKIE_NAME = 'geoconnect_h1'
########## END SESSION_COOKIE_NAME

# -----------------------------------
# ALLOWED_HOSTS
# -----------------------------------
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True

# Allow all host headers
ALLOWED_HOSTS = [os.environ['HEROKU_SERVER_NAME'],
                 'geoconnect.datascience.iq.harvard.edu']

########## LOGIN_URL
# To use with decorator @login_required
LOGIN_URL = "admin:index"
########## END LOGIN_URL


########## DATAVERSE_SERVER_URL
# Used to make API calls
# e.g.  http://dvn-build.hmdc.harvard.edu
#
DATAVERSE_SERVER_URL = os.environ['DATAVERSE_SERVER_URL']
DATAVERSE_METADATA_UPDATE_API_PATH = '/api/worldmap/update-layer-metadata/'
########## DATAVERSE_SERVER_URL

########### DIRECTORY TO STORE DATA FILES COPIES FROM DV
# Do NOT make this directory accessible to a browser
#
DV_DATAFILE_DIRECTORY = None    # use S3

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Credentials from Heroku, generated by Bucketeer
#
AWS_ACCESS_KEY_ID = os.environ['BUCKETEER_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['BUCKETEER_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['BUCKETEER_BUCKET_NAME']


########## GISFILE_SCRATCH_WORK_DIRECTORY
# Used for opening up files for processing, etc
GISFILE_SCRATCH_WORK_DIRECTORY = '/tmp'
########## END GISFILE_SCRATCH_WORK_DIRECTORY

########## WORLDMAP TOKEN/SERVER | DATAVERSE TOKEN AND SERVER
#

# RETRIEVE WORLDMAP INFO
WORLDMAP_SERVER_URL = os.environ['WORLDMAP_SERVER_URL']
WORLDMAP_ACCOUNT_USERNAME = os.environ['WORLDMAP_ACCOUNT_USERNAME']
WORLDMAP_ACCOUNT_PASSWORD = os.environ['WORLDMAP_ACCOUNT_PASSWORD']
WORLDMAP_ACCOUNT_AUTH = (WORLDMAP_ACCOUNT_USERNAME, WORLDMAP_ACCOUNT_PASSWORD)

########## END WORLDMAP TOKEN/SERVER | DATAVERSE TOKEN AND SERVER

WSGI_APPLICATION = 'geoconnect.wsgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

########## LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'gc_apps': {
            'handlers': ['console', 'mail_admins'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}
