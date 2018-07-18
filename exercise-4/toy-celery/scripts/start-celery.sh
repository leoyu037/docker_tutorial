#!/bin/bash
set -ex

queues=${QUEUES:-'celery,goodbye'}

if [ -z "$RUN_MODE" ]; then
  RUN_MODE="noop"
fi

if [ "$RUN_MODE" == 'worker' ]; then
  echo "STARTING TOY CELERY WORKER WITH QUEUES $queues"
  exec celery worker -A toy_app.app -Q ${queues} --concurrency 1
elif [ "$RUN_MODE" == 'beat' ]; then
  echo "STARTING TOY CELERY BEAT"
  exec celery beat -A toy_app.app -l info
elif [ "$RUN_MODE" == 'flower' ]; then
  echo "STARTING TOY CELERY FLOWER"
  exec celery flower -A toy_app.app --max-tasks=10000
elif [ "$RUN_MODE" == 'noop' ]; then
  echo "NOOP"
else
  echo "RUN_MODE $RUN_MODE blank/not supported."
fi
