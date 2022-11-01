#!/usr/bin/env bash
# Ensure you have installed armory with the following command:
#   $ pip install -e '.[developer,dataset]'
# USAGE:
#   $ ./huggingface2tfds.sh <dataset_name> <dataset_version> <output_dir>
# EXAMPLE:
#   $ ./huggingface2tfds.sh glue/mrpc 1.0 /tmp/mrpc

DATASET_NAME="${1:-mnist}"  # Dataset name
SKIP_LFS="${2:-1}"          # Clone without large files


PROJECT_ROOT=`git rev-parse --show-toplevel`
# TODO: Add install prefix; e.g. `/opt/armory`
PROFILE_ROOT="${PROJECT_ROOT}/profile"


pushd "${PROJECT_ROOT}" > /dev/null || exit 1
  if [ ! -d "${PROFILE_ROOT}" ]; then
      mkdir -p "${PROFILE_ROOT}/"{datasets,models,workspace}
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
  mkdir -p datasets/${DATASET_NAME}/data
  pushd datasets/${DATASET_NAME}
    # git lfs install
    GIT_LFS_SKIP_SMUDGE="${SKIP_LFS}" git clone https://huggingface.co/datasets/${DATASET_NAME} .

    # echo "Converting ${DATASET_NAME} to TFDS format"
    # tfds new ${DATASET_NAME}
    # Tensorflow Dataset Directory
    TFDS_DATA_DIR="`pwd`/data" \
    tfds build     \
      --pdb        \
      --overwrite
      # --data_dir="${PROFILE_ROOT}/datasets/${DATASET_NAME}/data"

  popd
popd > /dev/null
