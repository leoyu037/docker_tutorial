echo Enter docker image name to use for this demo:
read image_name
export DOCKER_DEMO_IMAGE_NAME=$image_name

echo Enter docker image tag:
read image_tag
export DOCKER_DEMO_IMAGE_TAG=$image_tag

virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
