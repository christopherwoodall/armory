###########################################################################################
#                           ARMORY Baseline Docker Image
#
# This File contains the baseline image for Armory docker images.  All framework
# based images should inhereit from this image using:
#       FROM twosixlabs/armory-baseline AS armory-baseline
#
#
###########################################################################################

ARG IMAGE_BASE="nvidia/cuda"
ARG IMAGE_TAG="11.3.1-cudnn8-runtime-ubuntu20.04"

ARG CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
ARG ARMORY_URL=""
ARG ART_URL=""

ARG CONDA_DIR="~/conda"

ARG USERNAME="armory"
ARG PASSWORD="armory"

FROM ${IMAGE_BASE}:${IMAGE_TAG} AS base

ENV DEBIAN_FRONTEND=noninteractive
USER root

# Install dependencies and utilities.
RUN apt-get -y -qq update && \
  apt-get install -y \
    build-essential \
    curl \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3 \
    python3-pip \
    sudo \
    tzdata \
    vim \
    wget \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
# Use the above args during building
#   https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG USERNAME
ARG PASSWORD

RUN useradd \
    --password '' \
    --system \
    --create-home \
    --home-dir /${USERNAME} \
    --groups sudo \
    --gid 0 \
    --uid 1000 \
    --shell /bin/bash \
    ${USERNAME} \
  && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/90-${USERNAME}" \
  && usermod -aG sudo ${USERNAME}

USER $USERNAME
ENV HOME=/$USERNAME

RUN mkdir -p ~/{conda,app,artifacts}


# Install Conda
FROM base AS miniconda

WORKDIR ${HOME}

ARG CONDA_URL
ARG CONDA_DIR

RUN curl -sL -o miniconda.sh "${CONDA_URL}" \
  && chmod +x miniconda.sh \
  && ./miniconda.sh -bfp ${CONDA_DIR} \
  && rm -rf miniconda.sh

ENV PATH=${CONDA_DIR}/bin:$PATH
# RUN conda init bash

