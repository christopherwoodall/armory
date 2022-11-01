#!/usr/bin/env bash
# Ensure you have installed armory with the following command:
#   $ pip install -e '.[developer,dataset]'
# USAGE:
#   $ ./huggingface2tfds.sh <dataset_name> <dataset_version> <output_dir>
# EXAMPLE:
#   $ ./huggingface2tfds.sh glue/mrpc 1.0 /tmp/mrpc

DATASET_NAME="${1:-mnist}"

PROJECT_ROOT=`git rev-parse --show-toplevel`
# TODO: Add install prefix; e.g. `/opt/armory`
PROFILE_ROOT="${PROJECT_ROOT}/profile"


pushd "${PROJECT_ROOT}" > /dev/null || exit 1
  if [ ! -d "${PROFILE_ROOT}" ]; then
      mkdir -p "${PROFILE_ROOT}/"{datasets,models,workspace}
  fi

  mkdir -p "${PROFILE_ROOT}/workspace/"{scenarios,tutorials,jupyter}
  mkdir -p "${PROFILE_ROOT}/workspace/jupyter/notebooks"
  mv scenario_configs "${PROFILE_ROOT}/workspace/scenarios"
  mv tutorials "${PROFILE_ROOT}/workspace/tutorials"
  mv notebooks "${PROFILE_ROOT}/workspace/jupyter/notebooks"
popd > /dev/null


pushd "${PROFILE_ROOT}" > /dev/null || exit 1
  mkdir -p datasets/${DATASET_NAME}
  pushd datasets/${DATASET_NAME}
    # git lfs install
    # Clone without large files
    # GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/${DATASET_NAME} .
    git clone https://huggingface.co/datasets/${DATASET_NAME} .

    # echo "Converting ${DATASET_NAME} to TFDS format"

  popd
popd > /dev/null
