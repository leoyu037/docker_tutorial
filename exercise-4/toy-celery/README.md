# Toy Celery

This is a barebones celery setup. Includes:
1. Some Celery tasks running in different queues
1. Beat schedule (`worker/schedule.py`)
1. Celery app instance (`worker/app.py`) that imports the tasks and schedule
1. Shell script entrypoint for starting the Celery worker, beat, flower
1. Alpine-based Dockerfile
1. Docker Compose file to build and run the setup locally

-----------

## Requirements

1. Docker
1. Docker Compose (preinstalled w/ Docker for Mac)

## Starting the application locally

```bash
  # Build image
  docker-compose build

  # Start app
  docker-compose up -d
```
