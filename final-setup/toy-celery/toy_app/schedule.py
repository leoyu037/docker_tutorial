from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    # Running in default 'celery' queue
    'hello-every-5s': {
        'task': 'print.hello',
        'schedule': 5,  # 5s
    },

    # Running in a different queue
    'goodbye-every-5s': {
        'task': 'print.goodbye',
        'schedule': timedelta(seconds=5),  # another way to specify frequency
        'options': {'queue': 'goodbye'},
    },

    # Reindex owners every 15s
    'reindex-owners': {
        'task': 'docker_tut.reindex_owners',
        'schedule': 15,
        'options': {'queue': 'docker_tut'},
    },

    # Reindex pets every 15s
    'reindex-pets': {
        'task': 'docker_tut.reindex_pets',
        'schedule': 15,
        'options': {'queue': 'docker_tut'},
    },
}
