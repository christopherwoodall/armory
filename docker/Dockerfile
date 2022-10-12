##########################################################################################
#
#                           ARMORY Baseline Docker Image
#
# This File contains the baseline image for Armory docker images.  All framework
# based images should inhereit from this image using:
#       FROM twosixlabs/armory-baseline AS armory-baseline
#
##########################################################################################

FROM nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04 AS base

# set pip's cache directory using this environment variable, and use
# ARG instead of ENV to ensure its only set when the image is built
ARG PIP_CACHE_DIR="/tmp/pip-cache"   \
    USER="armory"                    \
    PASSWORD="armory"

ENV PYTHON_VERSION="3.9"               \
    CONDA_DIR="/opt/conda"             \
    TZ="UTC"                           \
    PATH="/opt/conda/bin:$PATH"

# # TensorFlow requirement
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/

COPY ./ /app/

WORKDIR /app

USER root

SHELL ["/bin/bash", "-c"]


# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh


# Basic Apt-get Bits
RUN apt-get -y -qq update                                                        && \
    apt-get -qq -y upgrade                                                       && \
    apt-get install -y                                                              \
        wget                                                                        \
        vim                                                                         \
        build-essential                                                             \
        curl                                                                        \
        # libgl1-mesa-glx is needed for cv2 (opencv-python)
        libgl1-mesa-glx                                                          && \
    apt-get -y autoclean                                                         && \
    apt-get -y autoremove                                                        && \
    rm -rf /var/lib/apt/lists/*                                                  && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone   && \
    ldconfig

# Install Conda
# NOTE: with conda version 5, will need to set channel priority to flexible (as strict will become default)
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash miniconda.sh -b -p /opt/conda                             && \
    rm miniconda.sh                                                     && \
    conda install --yes --channel conda-forge --name base nomkl mamba   && \
    conda config --set auto_activate_base true                          && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh     && \
    conda init bash

# Create a user
RUN useradd -m ${USER} && \
    cp /root/.bashrc /home/${USER}/ && \
    mkdir -p /workspace && \
    chown -R --from=root ${USER} {/app,/workspace,/home/$USER}


# ------------------------------------------------------------------
# Environment Setup
# ------------------------------------------------------------------
FROM base AS staging
RUN mamba env update --name base --file /app/environment.yml --prune && \
    mamba clean --all --yes


# ------------------------------------------------------------------
# Configuration & Clean Up
# ------------------------------------------------------------------
FROM staging AS pre-release
RUN armory configure --use-default && \
    rm -rf /tmp/pip-cache

# Useful for updating pinned packages
# RUN mamba update --name base --all && \
#     mamba clean --all --yes && \
#     conda env export --no-builds > environment.yml


# ------------------------------------------------------------------
# Final Image
# ------------------------------------------------------------------
FROM pre-release AS release

USER armory

ENV HOME /workspace

VOLUME ["/workspace", "/app", "/tmp", "/home/armory"]

# Jupyter
EXPOSE 8888

WORKDIR /workspace


# ------------------------------------------------------------------
# DEVELOPER NOTES:
# ------------------------------------------------------------------
# TODO: determine if this environment setup is needed
#  $ ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/cuda/lib64"
#
# NOTE: Conda/Mamba commands
#   - Search through the revision history of an environment.
#     $ mamba list --name base --revisions
#   - Search for an available package, the command is slightly different in mamba.
#     $ mamba repoquery search <package>
#     $ mamba repoquery depends -a <package>
#   - Export an environment to a YAML file.
#     $ mamba env export --name base > environment.yml
#
# NOTE:
#  - pytorch-lightning >= 1.5.0 will break Deep Speech 2
#  - torchmetrics >= 0.8.0 will break pytorch-lightning 1.4
#  - hydra-lightning installs omegaconf
#  - google-cloud-storage needed for checkpoint.py import
#  - only sox python bindings are installed; underlying sox binaries not needed
#
# NOTE: Listed dependencies of PyTorch Deep Speech 2, but do not appear
#       to be used for inference (only for training), they are not installed:
#         - torchelastic
#         - wget
#         - flask
#         - fairscale
# ------------------------------------------------------------------
