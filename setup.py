#!/usr/bin/env python

from setuptools import setup

setup(
    name='Mezzanine on Openshift',
    version='0.1',
    description='Mezzanine on Openshift',
    author='',
    author_email='',
    url='',
    install_requires=[
        'Django==1.5.8',
        'mezzanine==3.0.9',
        'django_compressor==1.3',
        'South==0.8.4',
        'django-tagging',
        'django-debug-toolbar',
        'docutils',
        'django-reversion',
        'django-adminactions',
    ],
)


