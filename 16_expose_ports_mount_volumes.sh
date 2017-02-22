docker run --name ES -p 9200:9200 -v $(pwd)/resources:/resources -d elasticsearch

# -p: port forwarding
# -v: mount volume on host to container, must use absolute paths
#     This is what you might use to mount a configuration file to a dockerized
#     microservice container

# We can now communicate w/ elasticsearch
# curl localhost:9200
