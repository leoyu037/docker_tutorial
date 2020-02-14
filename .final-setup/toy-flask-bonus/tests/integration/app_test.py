import os

import requests

TOY_FLASK_HOST = os.environ.get('TOY_FLASK_HOST', 'localhost')
print(f'DEBUG: {TOY_FLASK_HOST}')


def test_get_owner():
    res = requests.get(f'http://{TOY_FLASK_HOST}/owner/My%20Grandma')
    assert res.status_code == 200

    owner = res.json()
    assert owner['name'] == 'My Grandma'


def test_get_owners_pets():
    res = requests.get(f'http://{TOY_FLASK_HOST}/owner/Bart%20Simpson/pets')
    assert res.status_code == 200

    pets = res.json()
    print(pets)
    pet_names = [pet['name'] for pet in pets]
    assert set(pet_names) == {'Santa\'s Little Helper', 'Snowball II'}
