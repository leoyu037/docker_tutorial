# Docker Workshop

The goal of this workshop is to provide a practical understanding of how to work
with Docker and Docker Compose through some simple hands-on exercises. By the
end of these, exercises you should be able to:

- Write a simple Dockerfile and build a Docker image
- Push/pull images from the Dockerhub image repository
- Manage images, containers, networks locally
- Run multiple images locally with proper networking between them
- Inspect/debug running containers
- Write Docker Compose configurations to store architecture configuration

## Requirements

- [Docker](https://store.docker.com/search?offering=community&type=edition)
    - Also available via homebrew for macOS: `brew cask install docker`
- [Dockerhub Account](https://hub.docker.com/)
    - Register for a Dockerhub account

--------------------------------------------------------------------------------

## Format

Short intro, then everyone starts going through the exercises. I'll walk
around and help people debug.

- `master` branch with resources
- `solutions` branch with answers

## Agenda

Start w/ data store
Then connect flask
Then connect celery

### Exercises
Docker
1. Play with elasticsearch
  - Seed it with data and run/inspect/query
  - Tasks covered:
    - Dockerhub search
    - Docker pull
    - run
1. Add toy flask
  - Take toy flask source, write a Dockerfile, build an image, create a repo,
    push
  - Delete image locally, run
  - Add endpoint to app to query documents from ES, rebuild, run w/
    elasticsearch, inspect/query
1. Scale toy flask
  - Connect a second toy-flask instance to ES
  - Reverse proxy w/ nginx
  - Do it w/ docker-compose
1. Toy celery
  - Run w/ docker-compose, inspect
  - Add tasks to index from the 2 postgres to ES, rebuild, add postgres w/ seed
    data, restart beat and workers
1. Connect toy celery to toy flask
  - Configure services to point to each other
  - Start both docker-compose setups

```
postgres > toy celery > elasticsearch > toy flask
               ^
postgres 2 ----|
```

### Workflows

- Create a new repo
  - Write > build > create repo > push
- Run a data store/tool/service locally
  - Search > pull > run > debug > stop/kill
- Local development
  - Build > run > debug > change code > rebuild > run
- Clear out old containers/images/networks
  - Clean

### Tasks
- Dockerhub
  - search
  - pull
  - login
  - push
  - create repo
- Dockerfile
  - write
- Image
  - ls
  - build
  - rm
    - force
  - prune
- Container
  - ps
  - run
    - environment variables
    - ports
    - volumes
    - network
    - entrypoint
    - {command}
  - logs
  - exec
  - stop
  - restart
  - kill
  - prune
- Network
  - ls
  - create
  - inspect
  - rm
  - prune
- Docker Compose
  - write
  - build
  - run
    - project
  - exec
  - logs
  - kill
  - down

--------------------------------------------------------------------------------

## Resources/Examples

- Toy Flask w/ Nginx
- Toy Celery
- Docker cleaning script

  ```bash
  docker container prune --force
  docker network prune --force
  docker image prune --force
  ```

## What I want to show

- Docker images are portable
  - Can search dockerhub for the technologies that you want to use
- Docker images are self-contained
  - Can run multiple versions of the same data store/service
  - Different apps can easily use different versions of the same dependency
- Keeps your local environment clean
  - Don't actually have to install software on your machine

- Benefits of using docker
  - Puts provisioning in developer's hands
  - Standardizes deployment
  - Dependency separation/encapsulation/environment isolation
  - Keeps local environment clean
  - Makes local development easier
    - You can be sure that the application is running in the exact same
      software environment, whether that's locally or in prod
  - Makes integration testing much easier
  - Rerequisite to using kuberenetes
  - It's lightweight, very little overhead in terms of performance
- Cons
  - Moderate learning curve
    - Learning to write optimized docker images
    - Learning to debug applications running inside containers
    - Learning the docker networking
