docker run --name ES --network demo_network -p 9200:9200 -v $(pwd)/resources:/resources -d elasticsearch

# --network: join a docker network. All containers in a network can access each
#            other by container name. This saves effort on manually linking
#            containers

echo Waiting for ES to initialize. Sleeping 15 seconds...; sleep 15
docker run --network demo_network $DOCKER_DEMO_IMAGE_NAME:$DOCKER_DEMO_IMAGE_TAG curl ES:9200
