# Tutorial Postgreses

This folder contains a Docker Compose configuration to bring up two Postgres
containers, one seeded with owner data, one seeded with pet data. The two
database instances run on different versions of Postgres.

To start the containers:

```bash
export COMPOSE_PROJECT_NAME=tutorial
docker-compose up
```
