#!/usr/bin/env python

from setuptools import setup

setup(
    name='roadmapsupdates',
    version='mvp',
    description='Nas mezzanine na django.',
    author='',
    author_email='',
    url='',
    install_requires=[
        'Django==1.5.8',
        'mezzanine==3.0.9',
        'django_compressor==1.3',
        'South==0.8.4',
        'django-tagging',
        'docutils',
        'reversion',
        'debug_toolbar',
    ],
)


