#!/usr/bin/env python

from setuptools import setup

setup(
    name='hello-flask-server',
    version='1.0',
    requires=['flask'],
    install_requires=[
        'flask>=0.10',
        'requests',
    ],
)
