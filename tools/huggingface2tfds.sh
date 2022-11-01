#!/usr/bin/env bash

PROJECT_ROOT=`git rev-parse --show-toplevel`


pushd $PROJECT_ROOT > /dev/null || exit 1

  mkdir -p huggingface2tfds



popd > /dev/null