#!/bin/bash
set -ex

queues=${QUEUES:-'celery,hello,docker_tut'}

if [ -z "$RUN_MODE" ]; then
  RUN_MODE="noop"
fi

if [ "$RUN_MODE" == 'worker' ]; then
  echo "STARTING TOY CELERY WORKER WITH QUEUES $queues"
  exec celery -A toy_app.app worker -Q ${queues} --concurrency 1
elif [ "$RUN_MODE" == 'beat' ]; then
  echo "STARTING TOY CELERY BEAT"
  exec celery -A toy_app.app beat -l info
elif [ "$RUN_MODE" == 'flower' ]; then
  echo "STARTING TOY CELERY FLOWER"
  exec celery -A toy_app.app flower --max-tasks=10000
elif [ "$RUN_MODE" == 'noop' ]; then
  echo "NOOP"
else
  echo "RUN_MODE $RUN_MODE blank/not supported."
fi
