##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine / environment. 

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "43f53fa5-4f39-4491-a1d6-ff80434f601ca6dab232-4b44-402c-bf41-54d69e5a143a57fcc763-a5ab-4889-8611-85abec4a37cd"
NEVERCACHE_KEY = "871fffc1-dbfd-4d89-adea-432acfbe67a30045cd59-8ddf-4096-8024-cc7278df6647dea34a30-c2ee-436f-bdeb-7589ffc2b42b"

import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["PGDATABASE"],
        "USER": os.environ["OPENSHIFT_POSTGRESQL_DB_USERNAME"],
        "PASSWORD": os.environ["OPENSHIFT_POSTGRESQL_DB_PASSWORD"],
        "HOST": os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        "PORT": os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
    }
}

# Media are stored in the persistent directory 
MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')

# Fix Django debug toolbar error, see here:
# http://django-debug-toolbar.readthedocs.org/en/1.0/installation.html#explicit-setup
# http://stackoverflow.com/questions/20963856/improperlyconfigured-the-included-urlconf-project-urls-doesnt-have-any-patte
DEBUG_TOOLBAR_PATCH_SETTINGS = False
