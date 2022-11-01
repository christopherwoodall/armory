#!/usr/bin/env bash
# Entrypoint for the dataset service

trap cleanup SIGINT SIGTERM ERR EXIT

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
}


DATASET_NAME="${1:-mnist}"  # Dataset name
SKIP_LFS="${2:-1}"          # Clone without large files
OUTPUT_DIR="${3:-/tmp/mnist}"  # Output directory

PROFILE_ROOT="/workspace"
SOURCE_ROOT="${PROFILE_ROOT}/src"


export HOME="${PROFILE_ROOT}"

conda init bash
source ~/.bashrc


pushd "${SOURCE_ROOT}" > /dev/null || exit 1
  pip install --upgrade pip
  pip install -e '.[datasets]'
popd > /dev/null


pushd "${PROFILE_ROOT}" > /dev/null || exit 1
  mkdir -p datasets/${DATASET_NAME}
  pushd datasets/${DATASET_NAME}
    if [ ! -d .git ]; then
      # git lfs install
      GIT_LFS_SKIP_SMUDGE="${SKIP_LFS}" git clone https://huggingface.co/datasets/${DATASET_NAME} .
    fi
    git pull

    echo "Converting ${DATASET_NAME} to TFDS format"
    mkdir -p ./data
    # Patch the file
    sed -i 's/import datasets/import tensorflow_datasets as datasets/g' mnist.py
    sed -i 's/from datasets.tasks import ImageClassification/# from datasets import image_classification/g' mnist.py
    # sed -i 's/from datasets.tasks import ImageClassification/from datasets import image_classification/g' mnist.py
    sed -i 's/ImageClassification/datasets.image_classification/g' mnist.py
    sed -i 's/datasets.GeneratorBasedBuilder/datasets.core.GeneratorBasedBuilder/g' mnist.py

    # Tensorflow Dataset Directory
    TFDS_DATA_DIR="`pwd`/data" tfds build \
      --pdb \
      --overwrite
      # --data_dir="${PROFILE_ROOT}/datasets/${DATASET_NAME}/data"

  popd
popd > /dev/null


/bin/bash
