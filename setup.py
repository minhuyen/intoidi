#!/usr/bin/env python

from setuptools import setup

setup(
    name='Mezzanine on Openshift',
    version='0.2',
    description='Mezzanine project template for Openshift Online',
    author='Radek Svarz',
    author_email='',
    url='https://bitbucket.org/radeksvarz/mezzanineopenshift',
    install_requires=[
        'Django==1.6.5',             # 
        'psycopg2==2.5.3',           # important as Openshift default is the older 2.0.4 version throwing errors
        'mezzanine==3.1.9',          # Mezzanine itself
        'django_compressor==1.4',    # Compresses linked, inline Javascript, CSS in a template into cacheable static files
        'South==1.0',                # Intelligent database migrations library for the Django web framework.

        ##################################### Libraries bellow are tested as not working ###########################
        # 'django-debug-toolbar',    # !!! - throws url errors on Openshift! Do not use !
        
        ##################################### Requirements bellow are working and optional ###########################
        'django-tagging==0.3.2',     # Tagging feature for Django models
        'docutils==0.11',            # Autodocumentation in admin 
        'django-reversion==1.8.1',   # Historical versions of records in admin
        'django-adminactions==0.4',  # mass admin import / export / graph actions in the admin lists
        'django-smuggler==0.4.1',    # data load / dump in json from the admin URL
        'mezzanine-page-auth==0.3.1',# group-level permission to pages
        'django-countries==2.1.2',   # Countries model field incl. combo box implementation
        'Whoosh==2.6.0',             # search in pure python 
        'raven==5.0.0',              # for Sentry integration - see getsentry.com
    ],
)
