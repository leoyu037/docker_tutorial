# Docker Tutorial

Here are a bunch of examples that are meant to be read and run __IN ORDER__. You're on your own if you don't and end up breaking something. But don't worry, the error messages are pretty informative :)

```bash
> source ./00_setup.sh
> source ./01_pull_image.sh
> ...
```

## Cheatsheet

__NOTE__: `[image]` can be as simple as `[image_name]` but can optionally include namespace and/or tag: `[namespace]/[image_name]:[tag]`

| Operation                               | Example                                                 |
| --------------------------------------- | ------------------------------------------------------- |
| __Building Images__                     |                                                         |
| Pull an image                           | `docker pull [image]`                                   |
| Build an image                          | `docker build -t [image] .`                             |
| Specify Dockerfile to use               | `docker build -f [Dockerfile_path] [...]`               |
| Login to Dockerhub                      | `docker login`                                          |
| Push an image                           | `docker push [image]`                                   |
|                                         |                                                         |
| __Image Operations__                    |                                                         |
| Show images                             | `docker images`                                         |
| Run an image                            | `docker run [image]`                                    |
| Override default command                | `docker run [image] [alt_command]`                      |
| Run image in background                 | `docker run -d [image]`                                 |
| Interactive mode                        | `docker run -it [image]`                                |
| Remove container after exit             | `docker run --rm [image]`                               |
| Expose port                             | `docker run -p [host_port]:[container_port] [...]`      |
| Mount volume                            | `docker run -v [host_abs_path]:[container_path] [...]`  |
| Link container                          | `docker run --link [container]:[alias] [...]`           |
| Join network                            | `docker run --network [network] [...]`                  |
| Remove image                            | `docker rmi [image]`                                    |
| Force removal                           | `docker rmi -f [image]`                                 |
| Remove all images                       | `docker rmi $(docker images -q)`                        |
| Clean cached image fragments            | `docker rmi $(docker images -fq dangling=true)`         |
|                                         |                                                         |
| __Container Operations__                |                                                         |
| Show running containers                 | `docker ps`                                             |
| Show all containers                     | `docker ps -a`                                          |
| Start container                         | `docker start [container]`                              |
| Run additional process in container     | `docker exec [container] [command]`                     |
| Interactive mode                        | `docker exec -it [...]`                                 |
| Start bash shell in container           | `docker exec -it [container] /bin/bash`                 |
| Inspect container                       | `docker inspect [container]`                            |
| Show container logs                     | `docker logs [container]`                               |
| Stop container                          | `docker stop [container]`                               |
| Remove container                        | `docker rm [container]`                                 |
| Force removal                           | `docker rm -f [container]`                              |
| Remove exited containers                | `docker rm $(docker ps --filter status-exited -q)`      |
| Remove all containers                   | `docker rm $(docker ps -aq)`                            |
|                                         |                                                         |
| __Network Operations__                  |                                                         |
| Show networks                           | `docker network ls`                                     |
| Create network                          | `docker network create [network]`                       |
| Inspect network                         | `docker network inspect [network]`                      |
| Remove network                          | `docker network rm [network]`                           |
| Remove unused networks                  | `docker network prune --force`                          |
|                                         |                                                         |
| __Docker Compose__                      |                                                         |
| Start docker-compose                    | `docker-compose up`                                     |
| Specify docker-compose config to use    | `docker-compose -f [docker_compose_config] [...]`       |
| Start in background                     | `docker-compose up -d`                                  |
| Execute command in a container          | `docker-compose exec [service] [cmd]                    |
| Show docker-compose service statsu      | `docker-compose ps`                                     |
| Show docker-compose service logs        | `docker-compose logs`                                   |
| Tail logs for a set of services         | `docker-compose logs --tail [n_lines] -f [services]     |
| Stop docker-compose                     | `docker-compose kill`                                   |
| Stop and clean docker-compose           | `docker-compose down`                                   |
| Build images defined in docker-compose  | `docker-compose build`                                  |
| Get updated images for each service     | `docker-compose pull`                                   |
|                                         |                                                         |

