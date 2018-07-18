from setuptools import setup

setup(
    name='toy-celery',
    version='0.0.1',
    install_requires=[
        'celery',
        'flower',
        'redis',
    ],
)
