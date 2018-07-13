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

This tutorial assumes that you already have latest version of Docker installed 
and an account on Dockerhub per the requirements below.

- [Docker](https://store.docker.com/search?offering=community&type=edition)
  - Also available via homebrew for macOS: `brew cask install docker`
- [Dockerhub Account](https://hub.docker.com/)
  - Register for a Dockerhub account

First, clone this repository:

```bash
git clone https://github.com/leoyu037/docker_tutorial .
cd docker_tutorial/
```

## Reference

If case you don't understand something or get lost or stuck, here are a few
helpful links with more in-depth explanations of various features:

- Docker:
  - [Command line reference](https://docs.docker.com/engine/reference/commandline/docker/)
  - [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- Docker Compose:
  - [Command line reference](https://docs.docker.com/compose/reference/)
  - [Docker Compose file reference](https://docs.docker.com/compose/compose-file/#compose-file-structure-and-examples)
  
And if things get hairy, here is a command to help reset your docker environment:

```bash
# Kill all containers
docker kill `docker ps -q`
# Remove all containers, networks, and images that aren't related to a running container
docker system prune --all
```

--------------------------------------------------------------------------------

## Exercise 1

Creating and sharing reusable images is a big part of the Docker philosophy, so
we're going to start the tutorial by working with a pre-existing image that the
Elasticsearch developers build and maintain.

- Go to [DockerHub](https://hub.docker.com), enter 'Elasticsearch' into the
  search box, and find the official Elasticsearch repository. You should land on
  [this page](https://hub.docker.com/_/elasticsearch/). Here, you'll see
  documentation for how to use the image along with a list of image tags (read:
  versions) available for use. The `tags` tab contains a more exhaustive list of
  tags.

  (__NOTE__: you'll see that the official Elasticsearch repo has been
  deprecated because Elasticsearch has chosen to self-host its Docker
  images--ignore for now).

  ![Official Elasticsearch Repo](https://github.com/leoyu037/docker_tutorial/blob/revised-workshops/.readme-assets/official-elasticsearch-repo-screenshot.png)

- Let's download the latest Elasticsearch as our first image:

  ```bash
  > docker pull elasticsearch    # specifying an image with no tag defaults to 'latest'

  # Or more explicitly:
  > docker pull elasticsearch:latest
  ```

  > Anyone can build and register public Docker images to DockerHub, but like
  > Elasticsearch, most other technologies have official Docker images that are
  > actively maintained. If you're thinking about using a new technology in a
  > container, the first place to check is DockerHub.

- Examine our local images:

  ```bash
  > docker images

  REPOSITORY                                      TAG                 IMAGE ID            CREATED             SIZE
  elasticsearch                                   latest              <image_id>          9 days ago          486MB
  ```

- Start Elasticsearch and examine our running containers:

  ```bash
  > docker run -p 9200:9200 -d elasticsearch:latest

  # -p: map local port to container port.
  #     Elasticsearch runs on port 9200 by default inside the container.
  #     We need this mapping in order to be able to access the container port
  #     locally.
  # -d: run the container in the background.

  > docker ps

  # You should see your new container running w/ the port mapped, along with
  # the container name (scroll right):
  CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                              NAMES
  <container_id>      elasticsearch:latest   "/docker-entrypoint.…"   About an hour ago   Up About an hour    0.0.0.0:9200->9200/tcp, 9300/tcp   <container_name>
  ```

- Now that the container is running, we can start playing with it. Use the
  container name from the output of the `docker ps` command to examine the
  container's logs:

  ```bash
  # Reference the container by either name or id:
  > docker logs -f <container_name/id>

  # -f: (follow) show new logs as they are generated
  ```

  We should eventually see in the logs that Elasticsearch has started. Press
  `Ctrl-C` to exit the log tailing. To confirm that Elasticsearch is up, query
  it:

  ```bash
  > curl localhost:9200/

  # We should see something along the following lines to confirm that
  # Elasticsearch is healthy:
  {
    "name" : "8DfH16I",
    "cluster_name" : "elasticsearch",
    "cluster_uuid" : "fTN23epwSc-YZdOTkdsxDw",
    "version" : {
      "number" : "5.6.10",
      "build_hash" : "b727a60",
      "build_date" : "2018-06-06T15:48:34.860Z",
      "build_snapshot" : false,
      "lucene_version" : "6.6.1"
    },
    "tagline" : "You Know, for Search"
  }

  > curl 'localhost:9200/_cat/indices?v'

  health status index uuid pri rep docs.count docs.deleted store.size pri.store.size
  # No indexes have been created
  ```

- So our Elasticsearch container has no data in it, which is pretty boring.
  Let's seed it with some data by mounting a volume into the container at
  startup. First, we should shut down our existing Elasticsearch container:

  ```bash
  # Reference the container by either name or id:
  > docker kill <container_name/id>
  # OR a gentler way to stop containers:
  > docker stop <container_name/id>

  > docker ps -a

  # -a: show all containers, not just running ones

  # The container is status 'Exited'
  CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS                       PORTS               NAMES
  <container_id>      elasticsearch:latest   "/docker-entrypoint.…"   10 minutes ago      Exited (137) 2 seconds ago                       <container_name>
  ```

  Now create a new Elasticsearch instance with some seed data:

  ```bash
  # From docker_tutorial/:
  > cd exercise-1/elasticsearch/

  # We're going to use an officially supported image this time. If you try to
  # create a container from an image that you don't have stored locally, Docker
  # will try to download the image first.
  > docker run -p 9200:9200 -v `pwd`/data/:/usr/share/elasticsearch/data/ -d docker.elastic.co/elasticsearch/elasticsearch:6.3.0

  # -v: mount a file/directory into the container's file system as a volume.
  #     The source path must be an absolute path.
  ```

  Use the `docker logs` command to watch Elasticsearch as it initializes. When
  it's ready, let's query it to examine the data that we've seeded:

  ```bash
  > curl 'localhost:9200/_cat/indices?v'

  health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
  green  open   owner TXOuE_c-QhKO8q3Xy0P1og   1   0          7            0      7.4kb          7.4kb
  green  open   pet   PTRNI5eySsCVRFBit9GHHA   1   0          6            0      4.3kb          4.3kb

  > curl 'localhost:9200/owner/_search?pretty'

  {
    "took" : 72,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : 3,
      "max_score" : 1.0,
      "hits" : [
        {
          "_index" : "owner",
          "_type" : "doc",
          "_id" : "YOSDkGQBd9122Iwh9_nQ",
          "_score" : 1.0,
          "_source" : {
            "name" : "Bart Simpson",
            "age" : 12
          }
        },
        {
          "_index" : "owner",
          "_type" : "doc",
          "_id" : "Y-SDkGQBd9122Iwh-PlB",
          "_score" : 1.0,
          "_source" : {
            "name" : "Richard Tator",
            "age" : 40
          }
        },
        {
          "_index" : "owner",
          "_type" : "doc",
          "_id" : "ZuSDkGQBd9122Iwh-Plc",
          "_score" : 1.0,
          "_source" : {
            "name" : "My Grandma",
            "age" : 300
          }
        }
      ]
    }
  }
  ```

> So to recap, we now have a working instance of Elasticsearch running with seed
> data that can be used for development, and we didn't have to install
> Elasticsearch in our local development environment (yay for clean development
> environments!). We also have an easy way to start and stop our Elasticsearch
> container on demand, and we know how to seed fresh instances of our
> Elasticsearch with data (yay for being able to develop/test with a consistent
> data set! Also, most other data store images provide a similar way to seed
> data). Awesome!

### Introducing Docker Compose

As we've seen, the docker commands to start containers can get pretty
cumbersome, especially when working with multiple containers at once. Enter
Docker Compose, a handy container orchestration tool for saving and starting
container configurations. Running plain Docker commands is sometimes
appropriate, but a most of the time it's easier to write a `docker-compose.yaml`
and use Docker Compose to work with frequently used setups.

- Continuing with our Elasticsearch example, we can turn our Docker command into
  a `docker-compose.yaml` (which has conveniently been provided):

  ```bash
  # From docker_tutorial/:
  > cd exercise-1/elasticsearch/
  > cat docker-compose.yaml
  ```
  ```yaml
  # docker-compose.yaml
  version: '3'
  services:
    elasticsearch:
      image: docker.elastic.co/elasticsearch/elasticsearch:6.3.0
      environment:
        discovery.type: single-node
      ports:
        - 9200:9200
      volumes:
        # The mount source can be a relative path in docker-compose
        - ./data/:/usr/share/elasticsearch/data/
  ```

  As we can see, our `docker-compose.yaml` defines one "service" named
  `elasticsearch` and specifies the image to use, an environment variable to
  inject, the port to map, and a volume to mount. The `elasticsearch` service
  configuration is essentially the YAML equivalent to the following Docker
  command:

  ```bash
  docker run -e discovery.type=single-node -p 9200:9200 -v `pwd`/data/:/usr/share/elasticsearch/data/ docker.elastic.co/elasticsearch/elasticsearch:6.3.0
  ```

  > Refer back to the [reference links](https://github.com/leoyu037/docker_tutorial/blob/revised-workshops/README.md#reference)
  > for more documentation on Docker Compose files.

- So now if we start our Docker Compose configuration, we'll have started an
  Elasticsearch container with the same exact setup as before:

  ```bash
  > docker-compose up -d

  # 'docker-compose.yaml/yml' is the standard name of docker-compose
  # configurations, so we don't need to explicitly pass in a filename
  # -d: start containers in the background
  ```

  In addition to seeing our running containers with `docker ps`, we can also
  inspect only the containers associated with our Docker Compose configuration:

  ```bash
  > docker-compose ps

  # Docker Compose by default generates a container name based on the service
  # name and the directory name that the Docker Compose file is in
              Name                           Command               State                Ports
  ---------------------------------------------------------------------------------------------------------
  elasticsearch_elasticsearch_1   /usr/local/bin/docker-entr ...   Up      0.0.0.0:9200->9200/tcp, 9300/tcp
  ```

  We can also see the logs for the containers that Docker Compose starts:

  ```bash
  > docker-compose logs
  ```

  When you're done poking around, let's shut our container down:

  ```bash
  > docker-compose stop
  # OR
  > docker-compose kill
  ```

In the rest of this tutorial, we'll introduce most features by using plain
Docker commands and then switch over to using Docker Compose for convenience.

__TODO__: clean up images, containers, networks?

--------------------------------------------------------------------------------

## Exercise 2

Now that we know how to search for, download, and run Docker images, let's try
creating an image for a basic 'Hello World!' Flask app and publishing it to
DockerHub.

- Go to the second exercise:

  ```bash
  # From docker_tutorial/:
  > cd exercise-2/toy-flask/
  ```
  
  Here we have `app.py` defining a simple Flask server, a `setup.py` with a list
  of requirements, and a Dockerfile to build our image:
  
  
  ```bash
  > cat Dockerfile
  ```
  ```Dockerfile
  # Dockerfile
  FROM python:3-alpine

  WORKDIR /app

  COPY setup.py setup.py
  RUN python setup.py install

  COPY app.py app.py

  CMD flask run -h 0.0.0.0 -p 80
  ```
  
  This Dockerfile specifies a base image to build off of, sets a working
  directory, copies our source, installs some dependencies, and specifies the 
  default command to execute when a container is created from an image built
  from this Dockerfile.
  
  > All Docker images inherit from some parent image. In this case, we are basing
  > our image off of an [official Python 3 image](https://hub.docker.com/_/python/)
  > that was built off of an [official Alpine Linux image](https://hub.docker.com/_/alpine/).
  > In most cases, if you click on a tag in for an official Docker repo, you
  > should be able to view the Dockerfile that the tag was built from. 
  >
  > ![Official Python Repo](https://github.com/leoyu037/docker_tutorial/blob/revised-workshops/.readme-assets/official-python-repo-screenshot.png)
  > ![Python 3-alpine Dockerfile](https://github.com/leoyu037/docker_tutorial/blob/revised-workshops/.readme-assets/python-3-alpine-dockerfile-screenshot.png)
  
- Let's build and run the image and verify that it works:

  ```bash
  > docker build -t toy-flask:0.0.1 .
  
  # -t: (required) specify the image name and the tag
  # The last arg specifies the directory of the Docker build context. All files
  # that are added from the local filesystem at build time are relative to this
  # directory.

  > docker run -p 80:80 -d toy-flask:0.0.1
  > curl localhost/some/path/
  Hello World!
  Path: some/path/
  ```
  
- Now that we have a working image, let's publish it to DockerHub. First we need
  to create a new repository for our image. Go to [DockerHub](https://hub.docker.com),
  login, and create a new public repo called `toy-flask`:
  
  ![New Dockerhub Repo](https://github.com/leoyu037/docker_tutorial/blob/revised-workshops/.readme-assets/dockerhub-create-repo-screenshot.png)
  
  Note that the repo's full name will be `<your_username>/toy-flask`. Then login
  to DockerHub on the command line, re-tag your image to match your repo name,
  and push to DockerHub:
  
  ```bash
  > docker login
  > docker tag toy-flask:0.0.1 <your_username>/toy-flask:0.0.1
  > docker images
  
  REPOSITORY                                      TAG                 IMAGE ID            CREATED             SIZE
  <your_username>/toy-flask                       0.0.1               <image_id>          About an hour ago   95.2MB
  toy-flask                                       0.0.1               <image_id>          About an hour ago   95.2MB
  
  > docker push <your_username>/toy-flask:0.0.1
  ```
  
  Your newly uploaded tag should now appear at `https://hub.docker.com/r/<your_username>/toy-flask/tags/`.
  
  ![Newly Uploaded Tag](https://github.com/leoyu037/docker_tutorial/blob/revised-workshops/.readme-assets/dockerhub-newly-uploaded-tag-screenshot.png)
  
- Now that we have a 

--------------------------------------------------------------------------------

## Exercise 3

--------------------------------------------------------------------------------

## Exercise 4

--------------------------------------------------------------------------------

## Conclusion

## Further Reading

- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
