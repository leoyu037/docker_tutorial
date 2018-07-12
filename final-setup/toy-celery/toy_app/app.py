

from celery import Celery

from toy_app.schedule import CELERYBEAT_SCHEDULE

broker_backend = 'redis://toy-celery-broker-backend:6379//0'
app = Celery('toy_app',
    broker=broker_backend,
    backend=broker_backend,
    # necessary for celery.shared_task tasks
    include=['toy_app.task'],
)
app.conf.update(
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE
)
