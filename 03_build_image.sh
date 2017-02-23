docker build -f 02_write_dockerfile -t $DOCKER_DEMO_IMAGE_NAME:$DOCKER_DEMO_IMAGE_TAG .

# -f: dockerfile to build from. By default, docker looks for a file named
#     Dockerfile
# -t: [namespace]/[image_name]:[tag]
# Last argument is the path of the 'context' to build from
