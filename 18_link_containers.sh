docker run --link ES:ES_alias --rm $DOCKER_DEMO_IMAGE_NAME:$DOCKER_DEMO_IMAGE_TAG curl ES_alias:9200

# --link: link this container to other container
#         [other_container]:[other_container_alias]

docker stop ES
docker rm ES
