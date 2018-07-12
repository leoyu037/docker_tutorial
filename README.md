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

This tutorial assumes that you already have Docker installed and an account on
Dockerhub per the requirements below.

- [Docker](https://store.docker.com/search?offering=community&type=edition)
    - Also available via homebrew for macOS: `brew cask install docker`
- [Dockerhub Account](https://hub.docker.com/)
    - Register for a Dockerhub account

First, clone this repository:

```bash
git clone https://github.com/leoyu037/docker_tutorial .
cd docker_tutorial/
```

## Exercise 1

- Go to the first exercise directory:

    ```bash
    # From docker_tutorial:
    cd exercise-1/
    ```

Creating and sharing reusable images is a big part of the Docker philosophy, so
we're going to start the tutorial by working with a pre-existing image that the
Elasticsearch developers build and maintain.

- Go to [DockerHub](hub.docker.com), enter 'Elasticsearch' into the search box,
  and find the official Elasticsearch repository. You should land on [this
  page](https://hub.docker.com/_/elasticsearch/). Here, you'll see documentation
  for how to use the image along with a list of image tags (read: versions)
  available for use. The `tags` tab contains a more exhaustive list of tags.
  (__NOTE__: you'll see that the official Elasticsearch repo has been
  deprecated because Elasticsearch has chosen to self-host its Docker
  images--ignore for now).
  
  ![Official Elasticsearch Repo](https://octodex.github.com/images/yaktocat.png)

- Let's download the latest Elasticsearch as our first image:

    ```bash
    docker pull elasticsearch    # specifying an image with no tag defaults to 'latest'

    # Or more explicitly:
    docker pull elasticsearch:latest
    ```

    > Anyone can build and register public Docker images to DockerHub, but like
    > Elasticsearch, most other technologies have official Docker images that are
    > actively maintained. If you're thinking about using a new technology in a
    > container, the first place to check is DockerHub.

- Examine your local images:

    ```bash
    docker image ls
    ```

    You should see `elasticsearch:latest` in your list of downloaded images.
