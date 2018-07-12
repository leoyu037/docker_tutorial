from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index

from documents import Owner, Pet


DATA = [
    {
        'owner': {'name': 'Bart Simpson', 'age': '12'},
        'pets': [
            {'name': 'Snowball II', 'species': 'cat', 'breed': 'black'},
            {'name': 'Santa\'s Little Helper', 'species': 'dog', 'breed': 'hound'},
        ],
    },
    {
        'owner': {'name': 'Richard Tator', 'age': '40'},
        'pets': [
            {'name': 'Adolf', 'species': 'cat', 'breed': 'sphynx'},
            {'name': 'Joe', 'species': 'dog', 'breed': 'pitbull'},
        ],
    },
    {
        'owner': {'name': 'My Grandma', 'age': '300'},
        'pets': [
            {'name': 'Garfield', 'species': 'cat', 'breed': 'orange tabby'},
            {'name': 'Odie', 'species': 'dog', 'breed': 'beagle'},
        ],
    },
]


def create_index(es, name, doc_type):
    idx = Index(name=name, using=es)
    idx.delete(ignore=404)
    idx.settings(
        number_of_shards=1,
        number_of_replicas=0,
    )
    idx.doc_type(doc_type)
    idx.create()
    idx.refresh()
    return idx


if __name__ == '__main__':
    es = Elasticsearch(hosts=['localhost'])
    owner_idx = create_index(es, 'owner', Owner)
    pet_idx = create_index(es, 'pet', Pet)

    owners = []
    pets = []

    for entry in DATA:
        owner = Owner(**entry['owner'])
        owner.save(index=owner_idx._name, using=es)
        owners.append(owner)

        for pet_entry in entry['pets']:
            pet = Pet(**pet_entry)
            pet.owner_id = owner._id
            pet.save(index=pet_idx._name, using=es)
            pets.append(pet)
