from setuptools import setup

setup(
    name='toy-celery',
    version='0.0.1',
    # packages=['toy_app'],
    install_requires=[
        'celery',
        'flower',
        'redis',
        'psycopg2',
        'elasticsearch',
    ],
)
