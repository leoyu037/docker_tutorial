#!/usr/bin/env python

from setuptools import setup

setup(
    name='toy-flask',
    version='0.0.0',
    requires=['flask'],
    install_requires=[
        'celery',
        'flask>=0.10',
        'redis',
        'requests',
    ],
)
