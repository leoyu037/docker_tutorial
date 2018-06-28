# Toy Flask

This is a barebones flask setup. Includes:
1. A simple flask server that returns "Hello World!" at the base route
1. Alpine-based Dockerfile
1. Docker-compose file to run 3 replicas behind an nginx loadbalancer

----------

## Requirements

1. Docker
1. Docker Compose (preinstalled w/ DOcker for Mac)

## Starting the application

```bash
  docker-compose build
  docker-compose up
```
