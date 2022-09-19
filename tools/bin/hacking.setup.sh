#! /usr/bin/env bash
set -e

PROJECT="armory"

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
BDIR="$( cd -P "$( dirname "$SOURCE" )/../.." && pwd )"

pushd $BDIR

# Setup venv
pip install venv
python -m venv venv
source venv/bin/activate

# pip install
pip install -e .
pip install -r requirements.txt

# Get the VCS version
TAG=`armory --version`

# Retag images
DOCKER_IMAGE=`docker images --all --format "{{.ID}}:{{.Repository}}:{{.Tag}}" | grep twosixarmory`
IMAGE_IDS=`echo $DOCKER_IMAGE | cut -d: -f1`
IMAGE_NAME=`echo ${DOCKER_IMAGE} | cut -d: -f2 | tr -d ' '`
IMAGE_TAG=`echo ${DOCKER_IMAGE} | cut -d: -f3 | tr -d ' '`

echo "Retagging ${IMAGE_IDS} to ${IMAGE_NAME}:${TAG}"
docker tag ${IMAGE_IDS} ${IMAGE_NAME}:${TAG}


popd
