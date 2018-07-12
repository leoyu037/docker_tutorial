# Toy Celery

This is a barebones celery setup. Includes:
1. A task running on default queue, a task running on a different queue (`worker/task.py`)
1. Beat schedule (`worker/schedule.py`)
1. Celery app instance (`worker/app.py`) that imports the tasks and schedule
1. Makefile entrypoint for starting worker, beat, flower
1. Alpine-based Dockerfile
1. Docker Compose file to build and run the setup locally

-----------

## Requirements

1. Docker
1. Docker Compose (preinstalled w/ Docker for Mac)

## Starting the application locally

```bash
  # Build image
  make build

  # Start app
  make run-local
```
