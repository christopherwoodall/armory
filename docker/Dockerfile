##########################################################################################
#
#                           ARMORY Baseline Docker Image
#
# This File contains the baseline image for Armory docker images.  All framework
# based images should inhereit from this image using:
#       FROM twosixlabs/armory-baseline AS armory-baseline
#
#
#            ~~! Please remove/modify the following lines as updates are made to the image. !~~
# Notes:
#   [1] https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/dockerfiles/dockerfiles/gpu.Dockerfile
#   [2] https://bcourses.berkeley.edu/courses/1478831/pages/glibcxx-missing
#   [3] https://docs.ycrc.yale.edu/clusters-at-yale/guides/conda/#mamba-the-conda-alternative
#   [4] https://github.com/tensorflow/models/tree/master/research/object_detection
#   [5]
#
##########################################################################################

ARG UBUNTU_VERSION=20.04
ARG CUDNN_VERSION=8
ARG CUDA_VERSION=11.6.2
ARG CUDA=11.6
ARG LIBNVINFER_MAJOR_VERSION=8


FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-runtime-ubuntu${UBUNTU_VERSION} AS base

ARG CUDA
ARG CUDA_VERSION
ARG LIBNVINFER_MAJOR_VERSION
ARG UBUNTU_VERSION
ARG UID=1000
ARG GID=$UID
ARG USER="armory"
ARG PASSWORD="armory"
# set pip's cache directory using this environment variable, and use
# ARG instead of ENV to ensure its only set when the image is built
ARG PIP_CACHE_DIR="/tmp/pip-cache"

ENV ARMORY_CONTAINER="1"              \
    PYTHONDONTWRITEBYTECODE="1"       \
    PYTHON_VERSION="3.9"              \
    CONDA_DIR="/opt/conda"            \
    TZ="UTC"                          \
    LC_ALL="C.UTF-8"                  \
    LANG="C.UTF-8"                    \
    DEBIAN_FRONTEND="noninteractive"  \
    PATH="/opt/conda/envs/base/bin:/opt/conda/bin:${PATH}"

WORKDIR /workspace

COPY ./ /workspace/app/

USER root

SHELL ["/bin/bash", "-c"]

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh


# Basic Apt-get Bits
RUN apt-key adv --fetch-keys \
        "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu${UBUNTU_VERSION/./}/x86_64/7fa2af80.pub" && \
    apt-key adv --fetch-keys \
        "https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu${UBUNTU_VERSION/./}/x86_64/7fa2af80.pub" && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu${UBUNTU_VERSION/./}/x86_64 /" \
        > /etc/apt/sources.list.d/tensorRT.list && \
    apt-get -y -qq update                                                        && \
    apt-get -qq -y upgrade                                                       && \
    apt-get install -y                                                              \
        sudo                                                                        \
        wget                                                                        \
        vim                                                                         \
        git                                                                         \
        curl                                                                        \
        # TF dependencies ( 1 )
        build-essential                                                             \
        ca-certificates                                                             \
        cuda-command-line-tools-${CUDA/./-}                                         \
        libcublas-${CUDA/./-}                                                       \
        cuda-nvrtc-${CUDA/./-}                                                      \
        libcufft-${CUDA/./-}                                                        \
        libcurand-${CUDA/./-}                                                       \
        libcusolver-${CUDA/./-}                                                     \
        libcusparse-${CUDA/./-}                                                     \
        libfreetype6-dev                                                            \
        libhdf5-serial-dev                                                          \
        libzmq3-dev                                                                 \
        pkg-config                                                                  \
        software-properties-common                                                  \
        unzip                                                                       \
        # TensorRT ( 1 )
        libnvinfer${LIBNVINFER_MAJOR_VERSION}                                       \
        libnvinfer-plugin${LIBNVINFER_MAJOR_VERSION}                                \
        # libgl1-mesa-glx is needed for cv2 (opencv-python)
        libgl1-mesa-glx                                                          && \
    # ln -snf /usr/share/zoneinfo/$TZ /etc/localtime                               && \
    #     echo $TZ > /etc/timezone                                                 && \
    ldconfig

# Install Conda
# NOTE: with conda version 5, will need to set channel priority to flexible (as strict will become default)
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash miniconda.sh -b -p /opt/conda                             && \
    rm miniconda.sh                                                     && \
    conda install --yes --channel conda-forge --name base nomkl mamba   && \
    conda config --set auto_activate_base true                          && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh     && \
    # Some TF tools expect a "python" binary ( 1 )
    ln -s $(which python3) /usr/local/bin/python                        && \
    conda init bash

# TensorFlow requirement ( 2 )
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/envs/base/lib/

# TensorFlow requirement ( 4 )
# TODO: Object Detection API

# Create a non-root user
RUN groupadd -r armory && \
    # TODO: UID/GID
    #   useradd --gid $GID --uid $UID -r -g armory -m -d /workspace -s /bin/bash armory && \
    useradd -r -g ${USER} -m -d /workspace -s /bin/bash ${USER}      && \
    usermod -aG sudo ${USER}                                         && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER}   && \
    cp /etc/skel/{.bashrc,.profile} /workspace                       && \
    chmod 0440 /etc/sudoers.d/${USER}                                && \
    chown -R --from=root ${USER} /workspace

ENV HOME /workspace


# ------------------------------------------------------------------
# Environment Setup
# ------------------------------------------------------------------
FROM base AS staging

# Utilize mamba for faster conda installs ( 3 )
RUN mamba env update --name base --file /workspace/app/environment.yml --prune && \
    mamba clean --all --yes


# ------------------------------------------------------------------
# Configuration & Clean Up
# ------------------------------------------------------------------
FROM staging AS pre-release

ENV HOME /workspace

RUN armory configure --use-default

# Clean Up
RUN apt-get purge $( dpkg --list | grep -P -o "linux-image-\d\S+"| head -n-1 ) -y && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    apt-get clean -y && \
    conda clean -afy
    # mamba clean --all --quiet --yes && \
    # pip cache purge && \
    # rm -rf /var/lib/apt/lists/* && \
    # rm -f /var/log/*gz

# ------------------------------------------------------------------
# Final Image
# ------------------------------------------------------------------
FROM pre-release AS release

USER armory

WORKDIR /workspace

ENV HOME /workspace

VOLUME ["/workspace", "/workspace/app", "/tmp", "/home/armory"]

# Jupyter
EXPOSE 8888

STOPSIGNAL SIGQUIT

CMD ["/bin/bash"]
