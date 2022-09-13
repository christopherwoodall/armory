#! /usr/bin/env bash

CONTAINER="armory-launcher/testing:latest"

if [ "$1" = "run" ]; then
    shift
    docker run \
      --rm \
      -it \
      --gpus all \
      --entrypoint bash \
      ${CONTAINER}
    # docker run --rm -it --entrypoint bash -v ${PWD}/docker-test/resources:/armory/resources --net=host armory-ml/testing:latest
    # docker run $(docker build -q --build-arg environment=production .) cat /value_of_environment
elif [ "$1" = "build" ]; then
  shift
  docker build --force-rm --file Dockerfile-GPU -t armory-gpu/testing:latest --progress=auto .
  docker build --force-rm --file Dockerfile-Client -t armory-client/testing:latest --progress=auto .
  docker compose up -d
  docker compose up --build -d
  docker exec -it armory-gpu bash
  docker compose down
    # --target miniconda
    # --output type=tar,dest=out.tar .
    #  -o - . > out.tar
    # --compress
    # --squash
    # --no-cache
    # --build-arg name=Baeldung
  # docker build --force-rm --no-cache --file ./docker-test/Dockerfile -t armory-ml/testing:latest --progress=auto .
  # docker build --force-rm --progress=auto --target miniconda --file ./docker-test/Dockerfile-Armory -t armory-launcher/testing:latest .
else
    echo "Usage: docker.sh [run|build] [command]"
fi



# https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html
# https://docs.docker.com/config/daemon/
# https://0xn3va.gitbook.io/cheat-sheets/container/escaping/exposed-docker-socket






