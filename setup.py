#!/usr/bin/env python

from setuptools import setup

setup(
    name='Mezzanine on Openshift',
    version='0.2',
    description='Mezzanine on Openshift',
    author='Radek Svarz',
    author_email='',
    url='',
    install_requires=[
        'Django==1.6.5',
        'psycopg2==2.5.3', # important as Openshift default is the older 2.0.4 version throwing errors
        'mezzanine==3.1.5',
        'django_compressor==1.4',
        'South==0.8.4',
        ##################################### Requirements bellow are optional ###########################
        'django-tagging==0.3.2',
        # 'django-debug-toolbar',  - throws url errors on Openshift!
        'docutils==0.11',
        'django-reversion==1.8.1',
        'django-adminactions==0.4',
        'django-smuggler==0.4.1',
        'mezzanine-page-auth==0.3.1',
        'django-countries==2.1.2',
        'Whoosh==2.6.0',
        'raven==5.0.0', # for Sentry integration - see getsentry.com
    ],
)
