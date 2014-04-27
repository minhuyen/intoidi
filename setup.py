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
        'Django==1.6.3',
        'psycopg2==2.5.2', # important as Openshift default is the older 2.0.4 version throwing errors
        'mezzanine==3.1.3',
        'django_compressor==1.3',
        'South==0.8.4',
        # requirements bellow are optional
        'django-tagging==0.3.2',
        # 'django-debug-toolbar',  - throughs url errors on Openshift!
        'docutils==0.11',
        'django-reversion==1.8.0',
        'django-adminactions==0.4',
        'django-smuggler==0.4.1',
    ],
)


