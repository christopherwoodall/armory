#!/usr/bin/env bash
# Ensure you have installed armory with the following command:
#   $ pip install -e '.[developer,dataset]'
# USAGE:
#   $ ./huggingface2tfds.sh <dataset_name> <dataset_version> <output_dir>
# EXAMPLE:
#   $ ./huggingface2tfds.sh glue/mrpc 1.0 /tmp/mrpc
trap cleanup SIGINT SIGTERM ERR EXIT

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  COMPOSE_COMMAND="docker-compose"
  if ! [ -x "$(command -v docker-compose)" ]; then
    COMPOSE_COMMAND="docker compose"
  fi
  $COMPOSE_COMMAND down
}


DATASET_NAME="${1:-mnist}"  # Dataset name
SKIP_LFS="${2:-1}"          # Clone without large files


SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
PROJECT_ROOT=`git rev-parse --show-toplevel`
# TODO: Add install prefix; e.g. `/opt/armory`
PROFILE_ROOT="${PROJECT_ROOT}/workspace"


# HOST_DOCKER_VERSION=`docker version --format '{{.Server.Version}}'`
COMPOSE_COMMAND="docker-compose"
if ! [ -x "$(command -v docker-compose)" ]; then
  COMPOSE_COMMAND="docker compose"
fi

pushd "${PROJECT_ROOT}" > /dev/null || exit 1
  if [ ! -d "${PROFILE_ROOT}" ]; then
      mkdir -p "${PROFILE_ROOT}/"{datasets,models,tmp,workspace}
  fi

#   if [ ! -d "${PROFILE_ROOT}/workspace/jupyter/notebooks" ]; then
#     mkdir -p "${PROFILE_ROOT}/workspace/"{scenarios,tutorials,jupyter}
#     mkdir -p "${PROFILE_ROOT}/workspace/jupyter/notebooks"
#     mv scenario_configs "${PROFILE_ROOT}/workspace/scenarios"
#     mv tutorials "${PROFILE_ROOT}/workspace/tutorials"
#     mv notebooks "${PROFILE_ROOT}/workspace/jupyter/notebooks"
#   fi
popd > /dev/null


$COMPOSE_COMMAND run --entrypoint="/bin/bash -c /tmp/entrypoint.sh" --workdir="/workspace" armory-datasets


######
# NOTES
#
# docker-compose --file docker-compose.yml up -d --build armory-datasets
# docker-compose exec armory-datasets /bin/bash
#
# docker compose run --entrypoint="/bin/bash -c /tmp/entrypoint.sh" --workdir="/workspace" armory-datasets

# docker-compose up --detach armory-launcher

# docker-compose exec -T \
#   --workdir="/workspace" \
#   armory-launcher \
#     /bin/bash -c /tmp/armory-shell.sh

# docker-compose exec \
#   --workdir="/workspace" \
#   armory-launcher \
#     /bin/bash -c tmux new-session -d -s armory; tmux attach-session -t armory