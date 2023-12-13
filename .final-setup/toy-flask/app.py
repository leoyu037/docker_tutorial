import os

from celery import Celery
from flask import Flask, jsonify
import requests

ES_HOST = os.environ['ES_HOST']

app = Flask(__name__)

# Celery
broker_backend = 'redis://toy-celery-broker-backend:6379//0'
celery_app = Celery(
    'toy_app',
    broker=broker_backend,
    backend=broker_backend,
)


@app.route('/')
def hello():
    return 'Hello World!'


@app.post("/purge_hello_queue")
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
    print("Purging queue...")
    messages = 0
    # with celery_app.connection_for_write() as conn:
    #     messages = sum(purge(conn, queue) for queue in queues)

    # if messages:
    #     print(f"Purged {messages} messages from hello queue.")
    # else:
    #     print("No messages purged from hello queue.")

    return {
        "status": "OK",
        "messages_cleared": messages,
    }


def _get_owner(owner_name):
    res = requests.get(f'http://{ES_HOST}/owner/_search?q=name:"{owner_name}"')
    first_entry = res.json()['hits']['hits'][0]
    owner = first_entry['_source']
    owner['id'] = first_entry['_id']
    return owner


@app.route('/owner/<owner_name>')
def get_owner(owner_name):
    try:
        return jsonify(_get_owner(owner_name))
    except KeyError:
        return f'Owner "{owner_name}" not found.', 404


@app.route('/owner/<owner_name>/pets')
def get_pets(owner_name):
    try:
        owner = _get_owner(owner_name)
        owner_id = owner['id']
    except KeyError:
        return f'Owner "{owner_name}" not found.', 404

    res = requests.get(f'http://{ES_HOST}/pet/_search?q=owner_id:"{owner_id}"')
    entries = res.json()['hits']['hits']
    pets = [entry['_source'] for entry in entries]
    for pet, entry in zip(pets, entries):
        pet['id'] = entry['_id']

    return jsonify(pets)


if __name__ == '__main__':
    app.run()
