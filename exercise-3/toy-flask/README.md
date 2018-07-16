# Toy Flask

This is a barebones flask setup. Includes:
1. A simple flask server that has routes to query the tutorial Elasticsearch
  instance
1. Alpine-based Dockerfile
1. Docker-compose file to run 3 replicas behind an nginx loadbalancer and
  corresponding nginx config

----------

## Requirements

1. Docker
1. Docker Compose (preinstalled w/ Docker for Mac)

## Starting the application

```bash
  export COMPOSE_PROJECT_NAME=tutorial
  docker-compose build
  docker-compose up
```
