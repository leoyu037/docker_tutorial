import os

from celery import shared_task


@shared_task(name='print.hello')
def hello():
    print('{}: Hello World!'.format(os.environ.get('HOSTNAME')))


@shared_task(name='print.goodbye')
def goodbye():
    print('{}: Goodbye Cruel World!'.format(os.environ.get('HOSTNAME')))
