# Tutorial Elasticsearch

This folder contains a Docker Compose configuration to bring up an Elasticsearch
container listening on port `9200` and some seed data to mount into the
container.

To start the Elasticsearch container:

```bash
export COMPOSE_PROJECT_NAME=tutorial
docker-compose up
```
