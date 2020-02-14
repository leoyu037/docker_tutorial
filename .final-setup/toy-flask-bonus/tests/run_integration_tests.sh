#!/bin/bash
set -e

export GIT_ROOT="`git rev-parse --show-toplevel`"
export COMPOSE_PROJECT_NAME=tutorial

function teardown {
  echo "Tearing down Elasticsearch containers"
  cd "$GIT_ROOT/bonus-2/elasticsearch"
  docker-compose kill
  docker-compose down || true
  git restore data/
  git clean -f data/

  echo "Tearing down Toy Flask containers"
  cd "$GIT_ROOT/bonus-2/toy-flask"
  docker-compose kill
  docker-compose down || true
}

function wait_for_elasticsearch {
  while [[ "`curl -s -o /dev/null "localhost:9200/_cluster/health?wait_for_status=green" -w "%{http_code}"`" != "200" ]]; do
    echo "Waiting for Elasticsearch to be ready"
    sleep 3
  done
  echo "Elasticsearch ready"
}

function wait_for_toy_flask {
  while [[ "`curl -s -o /dev/null "localhost:80/" -w "%{http_code}"`" != "200" ]]; do
    echo "Waiting for Toy Flask to be ready"
    sleep 3
  done
  echo "Toy Flask ready"
}

# Always teardown on script exit
trap teardown EXIT

echo "Starting Elasticsearch"
cd "$GIT_ROOT/bonus-2/elasticsearch"
docker-compose up -d
wait_for_elasticsearch

echo "Starting Toy Flask"
cd "$GIT_ROOT/bonus-2/toy-flask"
docker-compose build
docker-compose up -d
wait_for_toy_flask

# Run tests
echo "Running tests"
docker-compose run toy-flask-test pytest -s tests/integration

