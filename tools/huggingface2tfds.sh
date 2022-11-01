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
  # docker-compose down
  # rm -rf tmp
}

DATASET_NAME="${1:-mnist}"  # Dataset name
SKIP_LFS="${2:-1}"          # Clone without large files


SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
PROJECT_ROOT=`git rev-parse --show-toplevel`
# TODO: Add install prefix; e.g. `/opt/armory`
PROFILE_ROOT="${PROJECT_ROOT}/profile"


# HOST_DOCKER_VERSION=`docker version --format '{{.Server.Version}}'`
# COMPOSE_COMMAND="docker-compose"
# if ! [ -x "$(command -v docker-compose)" ]; then
#   COMPOSE_COMMAND="docker compose"
# fi

pushd "${PROJECT_ROOT}" > /dev/null || exit 1
  if [ ! -d "${PROFILE_ROOT}" ]; then
      mkdir -p "${PROFILE_ROOT}/"{datasets,models,tmp,workspace}
  fi

  if [ ! -d "${PROFILE_ROOT}/workspace/jupyter/notebooks" ]; then
    mkdir -p "${PROFILE_ROOT}/workspace/"{scenarios,tutorials,jupyter}
    mkdir -p "${PROFILE_ROOT}/workspace/jupyter/notebooks"
    mv scenario_configs "${PROFILE_ROOT}/workspace/scenarios"
    mv tutorials "${PROFILE_ROOT}/workspace/tutorials"
    mv notebooks "${PROFILE_ROOT}/workspace/jupyter/notebooks"
  fi
popd > /dev/null


pushd "${PROFILE_ROOT}" > /dev/null || exit 1
  mkdir -p datasets/${DATASET_NAME}
  pushd datasets/${DATASET_NAME}
    if [ ! -d .git ]; then
      # git lfs install
      GIT_LFS_SKIP_SMUDGE="${SKIP_LFS}" git clone https://huggingface.co/datasets/${DATASET_NAME} .
    fi
    git pull

    # echo "Converting ${DATASET_NAME} to TFDS format"
    mkdir -p ./data
    # Patch the file
    sed -i 's/import datasets/import tensorflow_datasets as datasets/g' mnist.py
    sed -i 's/from datasets.tasks import ImageClassification/from datasets import image_classification/g' mnist.py
    sed -i 's/ImageClassification/image_classification/g' mnist.py

    # Tensorflow Dataset Directory
    TFDS_DATA_DIR="`pwd`/data" tfds build \
      --pdb \
      --overwrite
      # --data_dir="${PROFILE_ROOT}/datasets/${DATASET_NAME}/data"

  popd
popd > /dev/null
