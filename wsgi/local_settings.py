##################
# LOCAL SETTINGS #
##################

#
# These are settings crafted to fit both Openshift environment and local development
# You should not need to change anything either here nor in main settings.py file
# Best practice is to inspire form the main settings.py file and 
# use the project_override_settings.py for project related adjustements
# This practice assures you can safely and carbon upgrade settings related to the next upgrade of Mezzanine
# 

import os

ON_OPENSHIFT = os.environ.has_key('OPENSHIFT_DATA_DIR')

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Following is the minimum line, you should add your custom domain here also.
ALLOWED_HOSTS = [
    os.environ.get('OPENSHIFT_GEAR_DNS'),
]

# If running on Openshift set DEBUG True only if explicitly set in environment variable DJANGO_DEBUG
# set it via ssh@openshift:  export DJANGO_DEBUG=True
# or using rhc from local PC: rhc env-set DJANGO_DEBUG=True --app <appname>
# set DEBUG true for local PC dev
DEBUG = not ON_OPENSHIFT
if os.environ.has_key('DJANGO_DEBUG'):
    DEBUG = os.environ['DJANGO_DEBUG']
    TEMPLATE_DEBUG = os.environ['DJANGO_DEBUG']

# Make these unique, and don't share it with anybody.
# These keys should be set and generated in the build hook

SECRET_KEY = "Looks like you are not running on Openshift or your build script failed and you need to change this key manualy."
NEVERCACHE_KEY = "Looks like you are not running on Openshift and need to change this key manualy."
if os.environ.has_key('DJANGO_SECRET_KEY'):
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
if os.environ.has_key('DJANGO_NEVERCACHE_KEY'):
    NEVERCACHE_KEY = os.environ['DJANGO_NEVERCACHE_KEY']

# DB settings based on Openshift variables
    
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('OPENSHIFT_APP_NAME'),
            'USER': os.environ.get('OPENSHIFT_POSTGRESQL_DB_USERNAME'),
            'PASSWORD': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PASSWORD'),
            'HOST': os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST'),
            'PORT': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT'),
        }
    }
elif os.environ.has_key('OPENSHIFT_MYSQL_DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('OPENSHIFT_APP_NAME'),
            'USER': os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME'),
            'PASSWORD': os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD'),
            'HOST': os.environ.get('OPENSHIFT_MYSQL_DB_HOST'),
            'PORT': os.environ.get('OPENSHIFT_MYSQL_DB_PORT'),
        }
    }
elif ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'sqlite3.db'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.db',
        }
    }
    

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# We want to collect static files to the persistent data dir, so it is not deleted during Openshift git push deployment
# On Openshift it is symlinked to the ./repo/wsgi/static
# If using on local PC, the default project static dir is used
if os.environ.has_key('OPENSHIFT_DATA_DIR'):
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'static') 

# old Openshift compatibility (static files are deleted during git push)
#if os.environ.has_key('OPENSHIFT_REPO_DIR'):
#    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static') 

# Media are stored in the persistent directory 
# On Openshift it is symlinked under static dir
# If using on local PC, the default project static/media dir is used
if os.environ.has_key('OPENSHIFT_DATA_DIR'):
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')

# Fix Django debug toolbar error on Openshift, see here:
# http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
# http://stackoverflow.com/questions/20963856/improperlyconfigured-the-included-urlconf-project-urls-doesnt-have-any-patte
if ON_OPENSHIFT:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

####################
# PROJECT SETTINGS #
####################

# Allow any settings to be overriden and additionaly defined in project_override_settings.py
# Best practice is to inspire form the main settings.py file and 
# use the project_override_settings.py for project related adjustements
# This practice assures you can safely and carbon upgrade settings related to the next upgrade of Mezzanine

try:
    from project_override_settings import *
except ImportError:
    pass
