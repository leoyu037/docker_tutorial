import os

from flask import Flask, jsonify
import requests

ES_HOST = os.environ.get('ES_HOST', 'localhost')

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


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
