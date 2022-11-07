#!/usr/bin/env bash

touch /.patched

export WORKER_DOCKER_VERSION=20.10.17

apt-get update
apt-get install --yes net-tools tmux

curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-20.10.17.tgz
tar xzvf docker-20.10.17.tgz --strip 1 -C /usr/local/bin docker/docker
rm docker-20.10.17.tgz

# diff -Naur #   /armory-repo/armory/docker/management.py.orig #   /armory-repo/armory/docker/management.py      #     > docker.management.patch
patch --force /armory-repo/armory/docker/management.py < /tmp/docker.management.patch

# cp --force /root/.armory/config.json /workspace/data/config.json

# Start Jupyter
# TODO: Move into config
# (nohup jupyter-lab
jupyter lab                              --ip=0.0.0.0                           --port=8888                            --no-browser                           --allow-root                           --ServerApp.token=''                   --ServerApp.password=''                --ServerApp.allow_origin='*'           --notebook-dir=/workspace/notebooks


  # --ServerApp.disable_check_xsrf=True    # --ServerApp.base_url=/               
  # --app-dir=/workspace
  # --ServerApp.base_url=/        &)
# cat nohup.out


conda init bash

# exec ""
/bin/bash
