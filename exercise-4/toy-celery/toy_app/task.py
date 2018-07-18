import os

from celery import shared_task
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from psycopg2.extras import DictCursor

from toy_app.db import PostgresDBConnection


@shared_task(name='print.hello')
def hello():
    print('{}: Hello World!'.format(os.environ.get('HOSTNAME')))


@shared_task(name='print.goodbye')
def goodbye():
    print('{}: Goodbye Cruel World!'.format(os.environ.get('HOSTNAME')))


def _psql_row_to_es_doc(row, index, id_field='id'):
    doc = {}
    doc['_index'] = index
    doc['_op_type'] = 'index'
    doc['_type'] = 'doc'
    doc['_id'] = row[id_field]
    doc['_source'] = {k: v for k, v in row.items()}
    return doc


def _etl(psql_host, psql_port, sql, es_host, es_index, id_field):
    # Extract
    with PostgresDBConnection(db='docker_tut', user='postgres', passwd='pass',
            host=psql_host, port=psql_port) as conn:
        cursor = conn.cursor('toy-celery-cur', cursor_factory=DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()

    # Transform
    docs = [_psql_row_to_es_doc(row, es_index, id_field) for row in rows]

    # Load
    es = Elasticsearch(hosts=[es_host])
    res = parallel_bulk(
        client=es,
        actions=docs,
        raise_on_error=False,
        raise_on_exception=False
    )

    result = dict(success=0, failed=0, failed_items=[])
    for ok, item in res:
        if not ok:
            result['failed'] += 1
            result['failed_items'].append(item)
        else:
            result['success'] += 1
    print('{} ETL result: {}'.format(es_index, result))
    return result


@shared_task(name='docker_tut.reindex_owners')
def reindex_owners():
    ES_HOST = os.environ['ES_HOST']
    OWNER_DB_HOST = os.environ['OWNER_DB_HOST']
    OWNER_DB_PORT = os.environ['OWNER_DB_PORT']
    OWNER_SQL = """
        SELECT
            owner_id,
            name,
            age,
            created,
            last_modified
        FROM
            public.owner
        WHERE
            owner_id > 0
    """
    return _etl(OWNER_DB_HOST, OWNER_DB_PORT, OWNER_SQL, ES_HOST, 'owner', 'owner_id')


@shared_task(name='docker_tut.reindex_pets')
def reindex_pets():
    ES_HOST = os.environ['ES_HOST']
    PET_DB_HOST = os.environ['PET_DB_HOST']
    PET_DB_PORT = os.environ['PET_DB_PORT']
    PET_SQL = """
        SELECT
            pet_id,
            name,
            species,
            breed,
            owner_id,
            created,
            last_modified
        FROM
            public.pet
        WHERE
            pet_id > 0
    """
    return _etl(PET_DB_HOST, PET_DB_PORT, PET_SQL, ES_HOST, 'pet', 'pet_id')
