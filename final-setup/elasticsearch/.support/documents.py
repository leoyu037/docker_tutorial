""" Document mappings/schemas for tutorial data model """
from elasticsearch_dsl import DocType, Text, Integer


class Owner(DocType):
    name = Text()
    age = Integer()


class Pet(DocType):
    name = Text()
    species = Text()
    breed = Text()
    owner_id = Text()
