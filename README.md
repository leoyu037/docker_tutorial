# Docker Workshop

The goal of this workshop is to provide a practical understanding of how to work
with Docker and Docker Compose through some simple hands-on exercises. By the
end of these, exercises you should be able to:

- Write a simple Dockerfile and build a Docker image
- Push/pull images from the Dockerhub image repository
- Manage images, containers, networks locally
- Run multiple images locally with proper networking between them
- Inspect/debug running containers
- Write Docker Compose configurations to model your application architecture

## Table of Contents

1. [Requirements](#requirements)
1. [Reference](#reference)
1. [Exercise 1: using containers, seeding data stores](#exercise-1)
1. [Exercise 2: creating and pushing images](#exercise-2)
1. [Exercise 3: networking, container orchestration](#exercise-3)
1. [Exercise 4: local development and debugging](#exercise-4)
1. [Conclusion](#conclusion)
1. [Further Reading](#further-reading)

## Requirements

This tutorial assumes that you already have latest version of Docker installed
and an account on Dockerhub per the requirements below:

- [Docker](https://store.docker.com/search?offering=community&type=edition)
  - Also available via homebrew for macOS: `brew cask install docker`
- [Dockerhub Account](https://hub.docker.com/)
  - Register for a Dockerhub account

Also, it's recommended to increase Docker's memory and CPU allocation to at least 4gb
and 2 CPUS, since we'll be running quite a few containers simultaneously by the end.
No prior knowledge of Docker is required for this tutorial, but see
[here](https://docs.docker.com/engine/docker-overview/) for an overview of the
general concepts if you are interested.

First, clone this repository:

```bash
> git clone https://github.com/leoyu037/docker_tutorial .
> cd docker_tutorial/
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
> docker kill `docker ps -q`
# Remove all containers, networks, and images that aren't related to a running container
> docker system prune --all
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
  
  > If you choose to reference a container/image/network by id, you can use a
  > truncated version of it as long as the truncated version is still unique.

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
      // ...
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
    // ...
    "hits" : {
      // ...
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

- Kill (or stop) the container when you are done.

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
appropriate, but most of the time it's easier to write a `docker-compose.yaml`
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

  > Refer back to the [reference links](#reference) for more documentation
  > on Docker Compose files.

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

Let's remove any leftover containers and (optionally) images before moving on
to the next exercise:

```bash
> docker container prune

# Optional, will delete all images not being used by a container
> docker image prune --all
```

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

  # Install python dependencies
  COPY setup.py setup.py
  RUN python setup.py install

  # Copy source code
  COPY app.py app.py

  CMD exec flask run -h 0.0.0.0 -p 80
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

- Let's examine the contents of our container by 'sshing' into it. We do this by
  starting a second process inside the container (in this case, shell):

  ```bash
  > docker exec -it <container_name/id> sh
  
  # These two options together allow us to interact with a container from the
  # command line:
  # -i: keep STDIN open
  # -t: allocate a pseudo-tty
  
  # From inside the container:
  /app > ls
  
  __pycache__         build               setup.py
  app.py              dist                toy_flask.egg-info
  
  /app > ps
  
  PID   USER     TIME   COMMAND
    1 root       0:00 {flask} /usr/local/bin/python /usr/local/bin/flask run -h 0.0.0.0 -p 80
   15 root       0:00 sh
   19 root       0:00 ps  
  ```
  
  As we can see, we're dropped directly into the container's working directory
  (which we defined in the Dockerfile), and it contains the two files that we
  added to the image, as well as a bunch of build artifacts from installing the
  Python dependencies into the image. And besides our shell and ps processes, 
  there is only the Flask process running in the container.
  
  > Notice that Flask is PID 1--it's best practice to ensure that the container's
  > main process is PID 1 if you want your process to receive signals properly
  > from Docker. See this [Elastic.co blogpost](https://www.elastic.io/nodejs-as-pid-1-under-docker-images/)
  > for an in-depth explanation.

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

- We are now able to run our image without having it cached locally:

  ```bash
  > docker rmi <your_username>/toy-flask:0.0.1
  > docker run -p 80:80 -d <your_username>/toy-flask:0.0.1
  ```

- Let's stop and remove our containers before moving on.

> Cool, now we know the general structure of a Dockerfile and how to publish our
> own images to DockerHub. As we'll see later, the contents of a Docker image are
> fully transparent, so be very careful not to build sensitive information (e.g.
> keys and passwords) into an image.

--------------------------------------------------------------------------------

## Exercise 3

Let's make our Flask app more useful and give it some endpoints to query our
Elasticsearch instance.

- Go to the third exercise and check out the new endpoints:

  ```bash
  # From docker_tutorial/:
  > cd exercise-3/
  > cat toy-flask/app.py
  ```
  ```python
  # app.py
  # ...

  ES_HOST = os.environ['ES_HOST']

  # ...

  def _get_owner(owner_name):
      res = requests.get(f'http://{ES_HOST}/owner/_search?q=name:"{owner_name}"')
      first_entry = res.json()['hits']['hits'][0]
      owner = first_entry['_source']
      owner['id'] = first_entry['_id']
      return owner


  @app.route('/owner/<owner_name>')
  def get_owner(owner_name):
      try:
          return jsonify(_get_owner(owner_name))
      except KeyError:
          return f'Owner "{owner_name}" not found.', 404


  @app.route('/owner/<owner_name>/pets')
  def get_pets(owner_name):
      try:
          owner = _get_owner(owner_name)
          owner_id = owner['id']
      except KeyError:
          return f'Owner "{owner_name}" not found.', 404

      res = requests.get(f'http://{ES_HOST}/pet/_search?q=owner_id:"{owner_id}"')
      entries = res.json()['hits']['hits']
      pets = [entry['_source'] for entry in entries]
      for pet, entry in zip(pets, entries):
          pet['id'] = entry['_id']

      return jsonify(pets)

  # ...
  ```

  We've added a simple route to retrieve an owner by name (this is obviously a
  weird way to use a search engine, but just go with it) and another route to
  retrieve an owner's pets. We've also configured our app to read the
  Elasticsearch host from the environment variable `ES_HOST`.

  Let's rebuild our container:

  ```bash
  # From docker_tutorial/exercise-3/:
  > docker build -f toy-flask/Dockerfile -t toy-flask:0.0.2 toy-flask/

  # -f: specify the path of the Dockerfile
  ```

- In order for containers to communicate with each other, they must be in the
  same Docker network:

  ```bash
  > docker network create tutorial
  > docker network ls

  # Networks 'bridge', 'host', and 'none' are special networks - you can read
  # about them in the Docker docs
  NETWORK ID          NAME                DRIVER              SCOPE
  xxxxxxxxxxxx        bridge              bridge              local
  xxxxxxxxxxxx        host                host                local
  xxxxxxxxxxxx        none                null                local
  <network_id>        tutorial            bridge              local
  ```

  Now that we've created a network called `tutorial`, let's start our
  Elasticsearch and toy Flask containers in our new network:

  ```bash
  # From docker_tutorial/exercise-3/:
  > docker run --name tut-elasticsearch --network tutorial -p 9200:9200 \
      -v `pwd`/elasticsearch/data/:/usr/share/elasticsearch/data/ \
      -d docker.elastic.co/elasticsearch/elasticsearch:6.3.0

  # --name: give the container a custom name
  # --network: connect the container to a network

  # Once docker containers are in the same network, they can refer to each
  # other by container name
  > docker run --name tut-toy-flask --network tutorial -p 80:80 \
      -e ES_HOST=tut-elasticsearch:9200 -d toy-flask:local

  > curl localhost/owner/bart

  {"age":12,"id":"YOSDkGQBd9122Iwh9_nQ","name":"Bart Simpson"}
  ```

  Great, our Flask container is able to talk to our Elasticsearch container.
  Let's take a closer look at the state of the network that we've created:

  ```bash
  > docker network inspect tutorial

  [
      {
          "Name": "tutorial",
          "Id": "<network_id>",
          // ...
          "Containers": {
              "<container_id>": {
                  "Name": "tut-elasticsearch",
                  // ...
                  "IPv4Address": "172.18.0.2/16",
                  // ...
              },
              "<container_id>": {
                  "Name": "tut-toy-flask",
                  // ...
                  "IPv4Address": "172.18.0.3/16",
                  / ...
              }
          },
          // ...
      }
  ]
  ```

  Here we can see that our network has its own subnet and that our two containers
  each have an address in the subnet. Containers can refer to each other by local
  IP, but some Docker networking magic allows us the flexibility of having our
  containers reference each other by name.

- Our Docker commands are starting to get really hairy. Let's turn our commands
  into Docker Compose configurations instead. First, we should clean up our
  containers and network:

  ```bash
  > docker kill tut-elasticsearch tut-toy-flask
  > docker container prune
  > docker network rm tutorial
  ```

  Let's take a look at the Docker Compose configuration for our toy Flask:

  ```bash
  # From docker_tutorial/exercise-3/:
  > cat toy-flask/docker-compose.yaml
  ```
  ```yaml
  # docker-compose.yaml
  version: '3'
  services:
    toy-flask-1:
      build: .
      image: toy-flask:local
      environment:
        ES_HOST: elasticsearch:9200
    toy-flask-2:
      image: toy-flask:local
      environment:
        ES_HOST: elasticsearch:9200
    toy-flask-3:
      image: toy-flask:local
      environment:
        ES_HOST: elasticsearch:9200
    nginx:
      image: nginx
      ports:
        - 80:80
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
  ```

  So we've specified three replicas of our toy Flask app and we've put them
  behind an Nginx configured as a load balancer (just for fun). Each toy Flask
  is configured to point to `elasticsearch`, which is the service name that we
  defined in the other Docker Compose config in [Exercise 1](#introducing-docker-compose).
  When using Docker Compose, you can also refer to containers by service name.

  > There is sometimes a better way to scale services with Docker Compose, see
  > [`docker-compose scale`](https://docs.docker.com/compose/reference/scale/).

  With four services defined in one configuration, it's easy to see how starting
  the containers with Docker Compose will be much easier than starting them with
  plain Docker commands.

- Let's try running this new setup with our two Docker Compose configurations.
  By default, Docker Compose creates a network for the containers that it starts
  for us. However this means that by default, containers started by separate
  Docker Compose configurations won't be able to communicate with each other.

  While not an explicit feature, specifying the 'project name' of a Docker
  Compose session will result in a network with the same name being created if
  it doesn't already exist. We can leverage this behavior to connect containers
  from different Docker Compose setups to the same network (there are other ways
  to do this, but this way is the most streamlined):

  ```bash
  # From docker_tutorial/exercise-3/
  > cd elasticsearch
  > docker-compose -p tutorial up -d

  # -p: specify project name, which also specifies the network name; the same
  #     can also be done by setting the COMPOSE_PROJECT_NAME env var

  > cd ../toy-flask
  > docker-compose -p tutorial up -d
  ```

  If we inspect the network that was created, we'll see all five containers
  there:

  ```bash
  > docker network ls

  NETWORK ID          NAME                DRIVER              SCOPE
  xxxxxxxxxxxx        bridge              bridge              local
  xxxxxxxxxxxx        host                host                local
  xxxxxxxxxxxx        none                null                local
  <network_id>        tutorial_default    bridge              local

  > docker network inspect tutorial_default

  [
      {
          "Name": "tutorial_default",
          "Id": "<network_id>",
          // ...
          "Containers": {
              "<container_id>": {
                  "Name": "tutorial_toy-flask-2_1",
                  // ...
              },
              "<container_id>": {
                  "Name": "tutorial_elasticsearch_1",
                  // ...
              },
              "<container_id>": {
                  "Name": "tutorial_toy-flask-3_1",
                  // ...
              },
              "<container_id>": {
                  "Name": "tutorial_toy-flask-1_1",
                  // ...
              },
              "<container_id>": {
                  "Name": "tutorial_nginx_1",
                  // ...
              }
          },
          // ...
          "Labels": {
              "com.docker.compose.network": "default",
              "com.docker.compose.project": "tutorial",
              "com.docker.compose.version": "1.21.1"
          }
      }
  ]
  ```

  Let's see our Nginx container doing round-robin-style load balancing as we
  give it queries:
  
  ```bash
  # From docker_tutorial/exercise-3/toy-flask/:
  > curl localhost
  
  Hello World!
  
  > curl localhost/owner/grandma
  
  {"age":300,"id":"ZuSDkGQBd9122Iwh-Plc","name":"My Grandma"}
  
  > curl localhost/owner/grandma/pets
  
  [{"breed":"orange tabby","id":"Z-SDkGQBd9122Iwh-Pli","name":"Garfield","owner_id":"ZuSDkGQBd9122Iwh-Plc","species":"cat"},{"breed":"beagle","id":"aOSDkGQBd9122Iwh-Plp","name":"Odie","owner_id":"ZuSDkGQBd9122Iwh-Plc","species":"dog"}]

  > docker-compose -p tutorial logs 
  
  # ...
  toy-flask-1_1  | 172.20.0.4 - - [16/Jul/2018 20:39:11] "GET / HTTP/1.0" 200 -
  nginx_1        | 172.20.0.1 - - [16/Jul/2018:20:39:11 +0000] "GET / HTTP/1.1" 200 12 "-" "curl/7.54.0"
  toy-flask-2_1  | 172.20.0.4 - - [16/Jul/2018 20:40:23] "GET /owner/grandma HTTP/1.0" 200 -
  nginx_1        | 172.20.0.1 - - [16/Jul/2018:20:40:23 +0000] "GET /owner/grandma HTTP/1.1" 200 60 "-" "curl/7.54.0"
  toy-flask-3_1  | 172.20.0.4 - - [16/Jul/2018 20:41:06] "GET /owner/grandma/pets HTTP/1.0" 200 -
  nginx_1        | 172.20.0.1 - - [16/Jul/2018:20:41:06 +0000] "GET /owner/grandma/pets HTTP/1.1" 200 234 "-" "curl/7.54.0"
  ```
  
- Let's stop and remove the containers and networks that were created by Docker
  Compose:

  ```bash
  # From docker_tutorial/exercise-3/toy-flask/:
  > docker-compose -p tutorial down --remove-orphans
  
  # --remove-orphans: remove containers in the project that aren't specified in
  #                   in the current Docker Compose configuration (in this case,
  #                   the Elasticsearch container)
  ```

> So what have we done so far? We've learned how to connect containers together
> with Docker networking, and we've put a bunch of them together into a basic
> application stack with load balancing. On top of that, we're now able to do
> it easily and consistently with a couple of reusable configuration files and
> short commands. That we were able to reuse the Docker Compose configuration
> from the first exercise shows that we have the flexibility to both work with 
> parts of a stack and its entirety without rewriting config--that's incredibly
> convenient!

--------------------------------------------------------------------------------

## Exercise 4

In this exercise, we'll learn a basic local development flow for working with a
distributed app while tying all of our containers together. A toy Python app 
using [Celery](http://www.celeryproject.org/) has been provided. 

Celery is a distributed task queue that typically uses RabbitMQ or Redis as the
message broker and Python workers deployed to one or more servers. Our setup
also includes a scheduler process called Beat and a web UI called Flower.

- Lets take a look at the project contents:

  ```bash
  # From docker_tutorial/:
  > cd exercise-4/
  > tree toy-celery/
      
  toy-celery
  ├── Dockerfile
  ├── README.md
  ├── docker-compose.yaml
  ├── scripts
  │   └── start-celery.sh     # Docker entrypoint for starting the app components
  │                           # based on the RUN_MODE env var
  ├── setup.py
  └── toy_app
      ├── __init__.py
      ├── app.py              # Celery app definition
      ├── db.py               # Database driver
      ├── schedule.py         # Celery task schedule
      └── task.py             # Celery task definitions
  ```
  
  Our Celery app defines a dummy 'Hello World!' task that's scheduled to run
  every 5 seconds on its own queue. There are also two tasks to reindex owner
  and pet data from two Postgres databases to our Elasticsearch, and those run
  every 15 seconds. The database and Elasticsearch hosts are configurable via
  environment variables. The Dockerfile has a similar structure to the
  Dockerfile for our toy Flask app:
  
  ```bash
  # From docker_tutorial/exercise-4/:
  > cd toy-celery/
  > cat Dockerfile
  ```
  ```Dockerfile
  # Dockerfile
  FROM python:3-alpine

  ENV DIR /srv
  WORKDIR ${DIR}

  # Install system dependencies
  RUN apk add --update --no-cache \
          bash \
          curl \
          postgresql-dev && \
      rm -rf /var/cache/apk/*

  # Install psycopg2
  RUN apk add --update --no-cache --virtual build-dependencies \
          gcc musl-dev && \
      pip install psycopg2 && \
      apk del build-dependencies

  # Install python dependencies
  COPY ./setup.py ${DIR}/
  RUN pip install -e .

  # Copy source code
  COPY ./toy_app/ ${DIR}/toy_app/
  COPY ./scripts/ ${DIR}/scripts/

  CMD ["./scripts/start-celery.sh"]
  ```

  The Docker Compose config defines a Redis container that will serve as our
  Celery app's task broker, two workers configured to service the two different
  queues, and the Beat scheduler and Flower UI:
  
  ```bash
  # From docker_tutorial/exercise-4/toy-celery/:
  > cat docker-compose.yaml
  ```
  ```yaml
  # docker-compose.yaml     
  version: '3'
  services:
    toy-celery-broker-backend:
      image: redis
      ports:
        - '6379:6379'
    toy-celery-worker-hello:
      # Specifies the build context to use when Docker Compose is used to build
      # all images in this config
      build: .
      image: toy-celery:local
      volumes:
        # Mount current folder as the container working dir
        - ./:/srv/
      environment:
        - C_FORCE_ROOT=True         # Has to do w/ Celery, ignore
        - RUN_MODE=worker           # Start the container as a worker
        - QUEUES=hello              # Only service the 'hello' queue
    toy-celery-worker-tut:
      build: .
      image: toy-celery:local
      volumes:
        - ./:/srv/
      environment:
        - C_FORCE_ROOT=True
        - RUN_MODE=worker
        - QUEUES=docker_tut
        - ES_HOST=elasticsearch     # Refers to ES defined in another config
        - OWNER_DB_HOST=owner_db    # Refers to db defined in another config
        - OWNER_DB_PORT=5432
        - PET_DB_HOST=pet_db        # Refers to db defined in another config
        - PET_DB_PORT=5432
    toy-celery-beat:
      build: .
      image: toy-celery:local
      volumes:
        - ./:/srv/
      environment:
        - RUN_MODE=beat
      # Override the default Docker command when starting this container
      command: sh -c 'rm celerybeat*; ./scripts/start-celery.sh'
    toy-celery-flower:
      build: .
      image: toy-celery:local
      volumes:
        - ./:/srv/
      environment:
        - RUN_MODE=flower
      ports:
        - '5555:5555'
      command: sh -c 'sleep 5; ./scripts/start-celery.sh'
  ```
  
  All of our containers, save for the broker, use the same source and thus the
  same image (that's just how Celery works).
  
  > Another thing to note is that in each of our Celery services, we're
  > mounting the project directory into the working directory of the container,
  > effectively replacing the container's source with the source from our local
  > file system. You'll see that this can be sort of a shortcut for quickly
  > testing code changes in your app without having to rebuild the image each
  > time. However, in general it's better to have a Dockerfile optimized for
  > quick, cached builds in a local development flow.
  
- Let's build our toy Celery app image and start our app:

  ```bash
  # From docker_tutorial/exercise-4/toy-celery/:
  > docker-compose build
  
  # Let's set COMPOSE_PROJECT_NAME so we don't have to keep specifying
  # '-p tutorial' in all of our Docker Compose commands for the rest of the
  # tutorial.
  > export COMPOSE_PROJECT_NAME=tutorial
  
  > docker-compose up -d
  > docker-compose logs -f
  
  # ...
  toy-celery-beat_1            | [2018-07-18 18:50:23,028: INFO/MainProcess] Scheduler: Sending due task hello-every-5s (print.hello)
  toy-celery-worker-hello_1    | [2018-07-18 18:50:23,033: WARNING/ForkPoolWorker-1] 099f39f8d55a: Hello World!
  toy-celery-beat_1            | [2018-07-18 18:50:28,029: INFO/MainProcess] Scheduler: Sending due task hello-every-5s (print.hello)
  toy-celery-worker-hello_1    | [2018-07-18 18:50:28,036: WARNING/ForkPoolWorker-1] 099f39f8d55a: Hello World!
  toy-celery-beat_1            | [2018-07-18 18:50:33,029: INFO/MainProcess] Scheduler: Sending due task hello-every-5s (print.hello)
  toy-celery-beat_1            | [2018-07-18 18:50:33,038: INFO/MainProcess] Scheduler: Sending due task reindex-owners (docker_tut.reindex_owners)
  toy-celery-beat_1            | [2018-07-18 18:50:33,038: INFO/MainProcess] Scheduler: Sending due task reindex-pets (docker_tut.reindex_pets)
  toy-celery-worker-hello_1    | [2018-07-18 18:50:33,039: WARNING/ForkPoolWorker-1] 099f39f8d55a: Hello World!
  toy-celery-worker-tut_1      | [2018-07-18 18:50:33,049: WARNING/ForkPoolWorker-1] Error: could not translate host name "owner_db" to address: Name does not resolve
  toy-celery-worker-tut_1      | [2018-07-18 18:50:33,055: ERROR/ForkPoolWorker-1] Task docker_tut.reindex_owners[8d6fcba2-368a-45aa-9df4-18049f6dd513] raised unexpected: OperationalError('could not translate host name "owner_db" to address: Name does not resolve\n',)
  toy-celery-worker-tut_1      | Traceback (most recent call last):
  toy-celery-worker-tut_1      |   File "/usr/local/lib/python3.6/site-packages/celery/app/trace.py", line 382, in trace_task
  toy-celery-worker-tut_1      |     R = retval = fun(*args, **kwargs)
  toy-celery-worker-tut_1      |   File "/usr/local/lib/python3.6/site-packages/celery/app/trace.py", line 641, in __protected_call__
  toy-celery-worker-tut_1      |     return self.run(*args, **kwargs)
  toy-celery-worker-tut_1      |   File "/srv/toy_app/task.py", line 74, in reindex_owners
  toy-celery-worker-tut_1      |     return _etl(OWNER_DB_HOST, OWNER_DB_PORT, OWNER_SQL, ES_HOST, 'owner', 'owner_id')
  toy-celery-worker-tut_1      |   File "/srv/toy_app/task.py", line 29, in _etl
  toy-celery-worker-tut_1      |     host=psql_host, port=psql_port) as conn:
  toy-celery-worker-tut_1      |   File "/srv/toy_app/db.py", line 34, in __enter__
  toy-celery-worker-tut_1      |     raise exc
  toy-celery-worker-tut_1      |   File "/srv/toy_app/db.py", line 31, in __enter__
  toy-celery-worker-tut_1      |     self.conn = self._connection()
  toy-celery-worker-tut_1      |   File "/srv/toy_app/db.py", line 24, in _connection
  toy-celery-worker-tut_1      |     connect_timeout=60
  toy-celery-worker-tut_1      |   File "/usr/local/lib/python3.6/site-packages/psycopg2/__init__.py", line 130, in connect
  toy-celery-worker-tut_1      |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
  toy-celery-worker-tut_1      | psycopg2.OperationalError: could not translate host name "owner_db" to address: Name does not resolve
  toy-celery-worker-tut_1      |
  toy-celery-worker-tut_1      | [2018-07-18 18:50:33,078: WARNING/ForkPoolWorker-1] Error: could not translate host name "pet_db" to address: Name does not resolve
  toy-celery-worker-tut_1      | [2018-07-18 18:50:33,088: ERROR/ForkPoolWorker-1] Task docker_tut.reindex_pets[a621ae11-5443-49c1-a7e2-ccb0568dd37d] raised unexpected: OperationalError('could not translate host name "pet_db" to address: Name does not resolve\n',)
  toy-celery-worker-tut_1      | Traceback (most recent call last):
  toy-celery-worker-tut_1      |   File "/usr/local/lib/python3.6/site-packages/celery/app/trace.py", line 382, in trace_task
  toy-celery-worker-tut_1      |     R = retval = fun(*args, **kwargs)
  toy-celery-worker-tut_1      |   File "/usr/local/lib/python3.6/site-packages/celery/app/trace.py", line 641, in __protected_call__
  toy-celery-worker-tut_1      |     return self.run(*args, **kwargs)
  toy-celery-worker-tut_1      |   File "/srv/toy_app/task.py", line 96, in reindex_pets
  toy-celery-worker-tut_1      |     return _etl(PET_DB_HOST, PET_DB_PORT, PET_SQL, ES_HOST, 'pet', 'pet_id')
  toy-celery-worker-tut_1      |   File "/srv/toy_app/task.py", line 29, in _etl
  toy-celery-worker-tut_1      |     host=psql_host, port=psql_port) as conn:
  toy-celery-worker-tut_1      |   File "/srv/toy_app/db.py", line 34, in __enter__
  toy-celery-worker-tut_1      |     raise exc
  toy-celery-worker-tut_1      |   File "/srv/toy_app/db.py", line 31, in __enter__
  toy-celery-worker-tut_1      |     self.conn = self._connection()
  toy-celery-worker-tut_1      |   File "/srv/toy_app/db.py", line 24, in _connection
  toy-celery-worker-tut_1      |     connect_timeout=60
  toy-celery-worker-tut_1      |   File "/usr/local/lib/python3.6/site-packages/psycopg2/__init__.py", line 130, in connect
  toy-celery-worker-tut_1      |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
  toy-celery-worker-tut_1      | psycopg2.OperationalError: could not translate host name "pet_db" to address: Name does not resolve
  toy-celery-worker-tut_1      |
  # ...
  ```
  
  We should see from the logs that our Beat container is scheduling the two tasks
  as expected and the workers dequeueing the tasks off of their respective queues
  and executing them. We can also visit `localhost:5555` in a browser for the app
  UI. It looks like the dummy task is running properly, but the reindexer tasks
  are failing (because it can't connect to the Postgres databases that we didn't
  start).
  
- To fix this, `Ctrl-C` out of the Docker Compose log tailing and start the
  Elasticsearch and Postgres databases:
  
  ```bash
  # From docker_tutorial/exercise-4/toy-celery/:
  > cd ../elasticsearch
  > docker-compose up -d
  > cd ../postgres
  > docker-compose up -d
  > cd ../toy-celery
  > docker-compose logs -t 50 -f
  
  # -t, --tail: show the last N lines of logs
  
  # We should begin to see the reindexer tasks complete successfully
  # ...
  toy-celery-beat_1            | [2018-07-18 18:50:18,028: INFO/MainProcess] Scheduler: Sending due task hello-every-5s (print.hello)
  toy-celery-worker-hello_1    | [2018-07-18 18:50:18,037: WARNING/ForkPoolWorker-1] 099f39f8d55a: Hello World!
  toy-celery-beat_1            | [2018-07-18 18:50:18,038: INFO/MainProcess] Scheduler: Sending due task reindex-owners (docker_tut.reindex_owners)
  toy-celery-beat_1            | [2018-07-18 18:50:18,053: INFO/MainProcess] Scheduler: Sending due task reindex-pets (docker_tut.reindex_pets)
  toy-celery-worker-tut_1      | [2018-07-18 18:50:18,176: WARNING/ForkPoolWorker-1] owner ETL result: {'success': 3, 'failed': 0, 'failed_items': []}
  toy-celery-worker-tut_1      | [2018-07-18 18:50:18,292: WARNING/ForkPoolWorker-1] pet ETL result: {'success': 8, 'failed': 0, 'failed_items': []}
  # ...
  ```
  
  > Side note: if you look at `postgres/docker-compose.yaml`, you'll see that the
  > two services are actually running two different versions of Postgres. This is a
  > perfect example of how Docker's environment isolation makes running apps
  > concurrently easy and clean--I haven't tried to run two different versions of a
  > datastore on my local development machine at the same time, but I imagine that
  > it'd be painful.
  
- Let's comment out the dummy task since we don't need it running anymore:
  
  ```python
  # toy_app/schedule.py
  CELERYBEAT_SCHEDULE = {
    # Running in default 'celery' queue
    # 'hello-every-5s': {
    #     'task': 'print.hello',
    #     'schedule': 5,  # 5s
    #     'options': {'queue': 'hello'},
    # },

    # Reindex owners every 15s
    'reindex-owners': {
        'task': 'docker_tut.reindex_owners',
        'schedule': 15,
        'options': {'queue': 'docker_tut'},
    },

    # Reindex pets every 15s
    'reindex-pets': {
        'task': 'docker_tut.reindex_pets',
        'schedule': 15,
        'options': {'queue': 'docker_tut'},
    },
  }
  ```
  
  Stop the Beat container and start it again:
  
  ```bash
  # From docker_tutorial/exercise-4/toy-celery/:
  > docker-compose kill toy-celery-beat
  > docker-compose up -d toy-celery-beat
  > docker-compose logs -f toy-celery-beat
  
  toy-celery-beat_1            | [2018-07-18 19:25:32,083: INFO/MainProcess] Scheduler: Sending due task reindex-owners (docker_tut.reindex_owners)
  toy-celery-beat_1            | [2018-07-18 19:25:32,091: INFO/MainProcess] Scheduler: Sending due task reindex-pets (docker_tut.reindex_pets)
  toy-celery-beat_1            | [2018-07-18 19:25:47,091: INFO/MainProcess] Scheduler: Sending due task reindex-pets (docker_tut.reindex_pets)
  toy-celery-beat_1            | [2018-07-18 19:25:47,094: INFO/MainProcess] Scheduler: Sending due task reindex-owners (docker_tut.reindex_owners)
  ```
  
  We should see that the new Beat container doesn't enqueue the dummy task
  anymore, leaving the worker servicing that queue idle. And we didn't have to
  rebuild our image because we're mounting the source from our local file system
  into the container.
  
- To tie this all together, start the toy Flask setup:

  ```bash
  # From docker_tutorial/exercise-4/toy-celery/:
  > cd ../toy-flask/
  > docker-compose up -d
  > docker ps
  
  CONTAINER ID        IMAGE                                                 COMMAND                  CREATED                  STATUS              PORTS                              NAMES
  <container_id>      nginx                                                 "nginx -g 'daemon of…"   Less than a second ago   Up 4 seconds        0.0.0.0:80->80/tcp                 tutorial_nginx_1
  <container_id>      toy-flask:local                                       "/bin/sh -c 'flask r…"   Less than a second ago   Up 5 seconds                                           tutorial_toy-flask-1_1
  <container_id>      toy-flask:local                                       "/bin/sh -c 'flask r…"   Less than a second ago   Up 5 seconds                                           tutorial_toy-flask-2_1
  <container_id>      toy-flask:local                                       "/bin/sh -c 'flask r…"   Less than a second ago   Up 5 seconds                                           tutorial_toy-flask-3_1
  <container_id>      toy-celery:local                                      "sh -c 'sleep 5; ./s…"   Less than a second ago   Up 19 seconds       0.0.0.0:5555->5555/tcp             tutorial_toy-celery-flower_1
  <container_id>      redis                                                 "docker-entrypoint.s…"   Less than a second ago   Up 19 seconds       0.0.0.0:6379->6379/tcp             tutorial_toy-celery-broker-backend_1
  <container_id>      toy-celery:local                                      "./scripts/start-cel…"   Less than a second ago   Up 20 seconds                                          tutorial_toy-celery-worker-hello_1
  <container_id>      toy-celery:local                                      "./scripts/start-cel…"   Less than a second ago   Up 20 seconds                                          tutorial_toy-celery-worker-tut_1
  <container_id>      toy-celery:local                                      "sh -c 'rm celerybea…"   Less than a second ago   Up 20 seconds                                          tutorial_toy-celery-beat_1
  <container_id>      docker.elastic.co/elasticsearch/elasticsearch:6.3.0   "/usr/local/bin/dock…"   8 seconds ago            Up 34 seconds       0.0.0.0:9200->9200/tcp, 9300/tcp   tutorial_elasticsearch_1
  <container_id>      postgres:10-alpine                                    "docker-entrypoint.s…"   24 seconds ago           Up 49 seconds       0.0.0.0:5434->5432/tcp             tutorial_pet_db_1
  <container_id>      postgres:11-alpine                                    "docker-entrypoint.s…"   24 seconds ago           Up 49 seconds       0.0.0.0:5433->5432/tcp             tutorial_owner_db_1

  > curl localhost/owner/alice
  
  {"age":20,"created":"2018-07-18T19:28:26.291558+00:00","id":"1","last_modified":"2018-07-18T19:28:26.291558+00:00","name":"Alice","owner_id":1}
  ```
  
  It all works! We have 12 containers representing a full application stack
  running on our local machine. This is the end of the tutorial, but feel free
  to play around and make changes to the system to get a feel for the Docker
  Compose development flow. Some things to try:
  
  - Changing data in the databases/Elasticsearch and watching it propagate
    through the system
  - Changing application code, stopping the relevant container, rebuilding, and
    restarting the container into the stack
  - Restarting the entire stack and reseting it to base state

- When you're done experimenting, shut everything down:

  ```bash
  > docker rm `docker ps -aq` --force
  > docker network prune
  ```

--------------------------------------------------------------------------------

## Conclusion

Hopefully going through these exercises has given you a taste for how to work
with Docker and what local development can be like.

## More Resources

- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Python Docker Driver](https://github.com/docker/docker-py)
