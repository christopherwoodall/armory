#!/usr/bin/env bash
# Simple docker installation of Armory

trap cleanup SIGINT SIGTERM ERR EXIT

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  cd `cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P`
  docker-compose down
  rm -rf tmp
}

if ! [[ -x "`command -v git`" ]] || ! [[ -x "`command -v docker`" ]]; then
  echo "🚨 Error: Both 'git' and 'docker' are required to run this script. 🚑" >&2
  exit 1
fi

if ! [[ -d armory ]]; then
  git clone https://github.com/twosixlabs/armory.git
fi


SCRIPT_DIR=`cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P`
HOST_DOCKER_VERSION=`docker version --format '{{.Server.Version}}'`
COMPOSE_COMMAND="docker-compose"

if ! [ -x "$(command -v docker-compose)" ]; then
  COMPOSE_COMMAND="docker compose"
fi

mkdir --parents {data,tmp}
mkdir --parents data/{workspace,datasets,outputs,models,tmp,git,saved_models}

pushd armory
  git pull
  PROJECT_ROOT=`git rev-parse --show-toplevel`
popd

# Set up SSL Certificates
KEY_ALIAS="armory"
CERT_PATH="data/certs/keystore.p12"
CERT_ALIAS="armory"
CERT_PASS="QWASZX23wesdxc"
if ! [[ -f data/certs/server.crt ]] || ! [[ -f data/certs/server.key ]]; then
  mkdir --parents data/certs
  pushd data/certs
    keytool -genkey -alias ${KEY_ALIAS} -storetype PKCS12 -keystore keystore.p12 -dname cn=${KEY_ALIAS} -validity 365 -storepass QWASZX23wesdxc -keypass QWASZX23wesdxc
    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=US/ST=CA/L=San Francisco/O=Two Six Labs/OU=Armory/CN=armory.twosixlabs.com"
  popd
fi



pushd tmp
tee config.json <<EOF
{
    "local_git_dir": "./armory/",
    "dataset_dir": "./data/datasets",
    "output_dir": "./data/outputs",
    "saved_model_dir": "./data/models",
    "tmp_dir": "./data/tmp",
    "verify_ssl": true
}
EOF
cp config.json ../data/config.json

tee docker.management.patch <<EOF
--- /armory-repo/armory/docker/management.py	2022-10-26 14:27:07.632172258 +0000
+++ /armory-repo/armory/docker/management.py.patch	2022-10-26 14:26:55.236697880 +0000
@@ -29,14 +29,25 @@
         host_paths = paths.HostPaths()
         docker_paths = paths.DockerPaths()

+        prefix = "${SCRIPT_DIR}"
+
+        mount_map = {
+            f"{prefix}/data/workspace": "/workspace",
+            f"{prefix}/data/datasets/": "/armory/datasets/",
+            f"{prefix}/armory": "/armory/git",
+            f"{prefix}/data/outputs": "/armory/outputs",
+            f"{prefix}/data/models": "/armory/saved_models",
+            f"{prefix}/data/tmp": "/armory/tmp",
+        }
+
         mounts = [
             docker.types.Mount(
-                source=getattr(host_paths, dir),
-                target=getattr(docker_paths, dir),
+                source=src,
+                target=dest,
                 type="bind",
                 read_only=False,
             )
-            for dir in "cwd dataset_dir local_git_dir output_dir saved_model_dir tmp_dir".split()
+            for src, dest in mount_map.items()
         ]

         container_args = {
EOF

tee entrypoint.sh <<EOF
#!/usr/bin/env bash

touch /.patched

export WORKER_DOCKER_VERSION=${HOST_DOCKER_VERSION}

apt-get update
apt-get install --yes tmux

curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${HOST_DOCKER_VERSION}.tgz
tar xzvf docker-${HOST_DOCKER_VERSION}.tgz --strip 1 -C /usr/local/bin docker/docker
rm docker-${HOST_DOCKER_VERSION}.tgz

# diff -Naur \
#   /armory-repo/armory/docker/management.py.orig \
#   /armory-repo/armory/docker/management.py      \
#     > docker.management.patch
patch --force /armory-repo/armory/docker/management.py < /tmp/docker.management.patch

# cp --force /root/.armory/config.json /workspace/data/config.json

ifconfig

# Start Jupyter
# TODO: Move into config
# (nohup jupyter-lab
jupyter lab                            \
  --ip=0.0.0.0                         \
  --port=8888                          \
  --no-browser                         \
  --allow-root                         \
  --ServerApp.token=''                 \
  --ServerApp.password=''              \
  --ServerApp.allow_origin='*'         \
  --notebook-dir=/workspace/notebooks


  # --ServerApp.disable_check_xsrf=True  \
  # --ServerApp.base_url=/               \

  # --app-dir=/workspace
  # --ServerApp.base_url=/        &)
# cat nohup.out


conda init bash

# exec "$@"
/bin/bash
EOF
chmod +x entrypoint.sh
popd


tee docker-compose.yml <<EOF
---
version: "3"
services:
  armory-launcher:
    container_name: armory-launcher
    hostname: armory-launcher

    image: twosixarmory/pytorch:latest

    # command: ["tail", "-f", "/dev/null"]
    # entrypoint: [ "/bin/bash" ]

    networks:
      armory_network:
        aliases:
          - armory-launcher

    ports:
      - 8888:8888

    # environment:
    #   - CERT_ALIAS=${CERT_ALIAS?err}
    #   - CERT_KEYSTORE_PASS=${CERT_PASS?err}
    #   - CERT_TRUSTSTORE_PASS=${CERT_PASS?err}

    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:rw

      - ./tmp/entrypoint.sh:/tmp/entrypoint.sh:z
      - ./tmp/docker.management.patch:/tmp/docker.management.patch:z

      - ./data/:/workspace/data/:z

      - ./notebooks/:/workspace/notebooks/:z

      - ./tmp/config.json:/root/.armory/config.json:z

      - ./armory/scenario_configs/:/workspace/scenarios/:z

      - ./armory:/armory-repo/:z
      # - ./armory:/workspace/src/:z

    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           capabilities: [gpu]

    # tty: true
    stdin_open: true


networks:
  armory_network:
    driver: bridge
EOF


$COMPOSE_COMMAND run --entrypoint="/bin/bash -c /tmp/entrypoint.sh" --workdir="/workspace" armory-launcher

# docker-compose up --detach armory-launcher

# docker-compose exec -T \
#   --workdir="/workspace" \
#   armory-launcher \
#     /bin/bash -c /tmp/entrypoint.sh

# docker-compose exec \
#   --workdir="/workspace" \
#   armory-launcher \
#     /bin/bash -c tmux new-session -d -s armory; tmux attach-session -t armory


# wsl_win_proxy() {
#     wsl_ip="$(ip route | grep -oP '^.*src \K[0-9\.]+')"
#     wsl_port="8888"

#     win_ip="0.0.0.0"
#     win_port="8888"

#     rule_name="Inbound TCP ${win_port}"
#     win_get_fw_rule_cmd="Get-NetFirewallRule | Where { \$_.DisplayName -eq '${rule_name}' }"
#     win_new_fw_rule_cmd="New-NetFirewallRule -DisplayName '${rule_name}' -Direction Inbound -Action Allow -Protocol TCP -LocalPort ${win_port}"

#     if ! netsh.exe interface portproxy show all | grep -q -P "${win_ip}\s+${win_port}\s+${wsl_ip}\s+${wsl_port}"
#     then
#         powershell.exe Start-Process -Verb runAs -FilePath "netsh.exe" \
#             -ArgumentList "interface","portproxy","add","v4tov4",\
#                     "listenport=$win_port","listenaddress=$win_ip",\
#                     "connectport=$wsl_port","connectaddress=$wsl_ip"

#         if [[ $? -eq 0 ]]
#         then
#             echo "Port proxy '${win_ip}:${win_port} > ${wsl_ip}:${wsl_port}' is created."
#         else
#             echo "Port proxy '${win_ip}:${win_port} > ${wsl_ip}:${wsl_port}' failed."
#         fi

#         if ! powershell.exe ${win_get_fw_rule_cmd} | grep -q "$rule_name"
#         then
#             echo "Open PowerShell as Admin and create the following firewall rule:"
#             echo -e '\033[1;33m'"$win_new_fw_rule_cmd"'\033[0m'
#         fi
#     fi
# }
# wsl_win_proxy