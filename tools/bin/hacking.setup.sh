#! /usr/bin/env bash
set -e

PROJECT="armory"
LATEST_RELEASE="twosixarmory/pytorch:0.14.6"


SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
BDIR="$( cd -P "$( dirname "$SOURCE" )/../.." && pwd )"

pushd $BDIR

# Setup venv
pip3 install venv
python3 -m venv venv
source venv/bin/activate

# pip install
pip install --force-reinstall --no-compile --progress-bar="emoji" --editable '.[developer]'

# Get the VCS version
TAG=`armory --version`

# Retag images
DOCKER_IMAGE=`docker images 'twosixarmory/*' --all --format "{{.ID}}:{{.Repository}}:{{.Tag}}" | head -n 1`
IMAGE_IDS=`echo $DOCKER_IMAGE    | cut -d: -f1`
IMAGE_NAME=`echo ${DOCKER_IMAGE} | cut -d: -f2 | tr -d ' '`
IMAGE_TAG=`echo ${DOCKER_IMAGE}  | cut -d: -f3 | tr -d ' '`

echo "Retagging ${IMAGE_IDS} to ${IMAGE_NAME}:${TAG}"
docker tag ${IMAGE_IDS} ${IMAGE_NAME}:${TAG}

# Optionally save the image
# docker save `docker images 'twosixarmory/*' --format '{{.ID}}' | head -n 1` -o twosixarmory.tar
# Add load it
# docker load < twosixarmory.tar

popd
