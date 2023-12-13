CELERYBEAT_SCHEDULE = {
    # Running in default 'celery' queue
    'hello-every-5s': {
        'task': 'print.hello',
        'schedule': 5,  # 5s
        'options': {'queue': 'hello'},
    },

    # # Reindex owners every 15s
    # 'reindex-owners': {
    #     'task': 'docker_tut.reindex_owners',
    #     'schedule': 15,
    #     'options': {'queue': 'docker_tut'},
    # },

    # # Reindex pets every 15s
    # 'reindex-pets': {
    #     'task': 'docker_tut.reindex_pets',
    #     'schedule': 15,
    #     'options': {'queue': 'docker_tut'},
    # },
}
