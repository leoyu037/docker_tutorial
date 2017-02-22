docker rmi -f $DOCKER_DEMO_IMAGE_NAME:$DOCKER_DEMO_IMAGE_TAG

# -f: force removal. docker won't let you remove an image if a container
#     references it, even if it's stopped
