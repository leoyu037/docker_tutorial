
from celery import Celery
from flask import Flask

from toy_app.schedule import CELERYBEAT_SCHEDULE

broker_backend = 'redis://toy-celery-broker-backend:6379//0'
app = Celery(
    'toy_app',
    broker=broker_backend,
    backend=broker_backend,
    # necessary for celery.shared_task tasks
    include=['toy_app.task'],
)
app.conf.update(
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE
)

flask_app = Flask(__name__)


@flask_app.route('/')
def hello():
    return 'Hello World!'


@flask_app.post("/purge_hello_queue")
def purge_stats_queues():
    """ Purge hello queue

    Useful when the queue is backed up and we want to clear it out.

    Code lifted directly from the command line tool:
        https://github.com/celery/celery/blob/main/celery/bin/purge.py#L56
    """
    def purge(conn, queue: str):
        try:
            return conn.default_channel.queue_purge(queue) or 0
        except conn.channel_errors:
            return 0

    queues = ["hello"]
    with app.connection_for_write() as conn:
        messages = sum(purge(conn, queue) for queue in queues)

    if messages:
        print(f"Purged {messages} messages from hello queue.")
    else:
        print("No messages purged from hello queue.")

    return {
        "status": "OK",
        "messages_cleared": messages,
    }
