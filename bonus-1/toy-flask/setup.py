#!/usr/bin/env python

from setuptools import setup

setup(
    name='toy-flask',
    version='0.0.0',
    requires=['flask'],
    install_requires=[
        'flask>=0.10',
        'requests',
    ],
    extras_require={
        'testing': [
            'pytest',
            'pytest-cov',
            'pytest-flake8',
            'pytest-mock',
        ],
    },
)
