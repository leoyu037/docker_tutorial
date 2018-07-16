
## Format

Short intro, then everyone starts going through the exercises. I'll walk
around and help people debug.

- `master` branch with resources
- `solutions` branch with answers

## Exercises

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
1. Connect to elasticsearch and scale toy flask
  - Add endpoint to app to query documents from ES, rebuild, run w/
    elasticsearch, inspect/query
  - Connect a second toy-flask instance to ES
  - Reverse proxy w/ nginx
  - Do it w/ docker-compose

add endpoint
create network
list network
run flask and elasticsearch together
inspect network
remove containers
remove network

write docker-compose
connect to elasticsearch docker-compose
observe load balancing

1. Toy celery
  - Run w/ docker-compose, inspect
  - Add tasks to index from the 2 postgres to ES, rebuild, add postgres w/ seed
    data, restart beat and workers
1. Connect toy celery to toy flask
  - Configure services to point to each other
  - Start both docker-compose setups

Final configuration:

```
postgres > toy celery > elasticsearch > toy flask
               ^
postgres 2 ----|
```

### Workflows to cover

- DONE: Create a new repo
  - Write > build > create repo > push
- DONE: Run a data store/tool/service locally
  - Search > pull > run > debug > stop/kill
- Local development
  - Build > run > debug > change code > rebuild > run
- Clear out old containers/images/networks
  - Clean

### Tasks to cover
- Dockerhub
  - DONE: search
  - DONE: pull
  - DONE: login
  - DONE: push
  - DONE: create repo
- Dockerfile
  - DONE: write
- Image
  - DONE: ls
  - DONE: build
  - DONE: tag
  - DONE: rm
    - force
  - DONE: prune
- Container
  - DONE: ps
  - DONE: run
    - DONE: environment variables
    - DONE: ports
    - DONE: volumes
    - TODO: network
    - entrypoint
    - {command} - introduce a bug to debug
  - DONE: logs
  - exec
  - DONE: stop
  - restart
  - DONE: kill
  - DONE: prune
- Network
  - TODO: ls
  - TODO: create
  - TODO: inspect
  - TODO: rm
  - prune
- Docker Compose
  - DONE: write
  - build
  - DONE: up
    - project
  - DONE: ps
  - run
  - exec
  - DONE: logs
  - DONE: stop
  - DONE: kill
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
