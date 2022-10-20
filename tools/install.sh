#!/usr/bin/env bash

######
# USAGE: curl -sSL https://raw.githubusercontent.com/.../install.sh | bash
######

# Set the default values
DEFAULT_VERSION="0.1.0"
DEFAULT_INSTALL_DIR="/usr/local/bin"

# Get the version and install directory from the cli
VERSION=${1:-$DEFAULT_VERSION}
INSTALL_DIR=${2:-$DEFAULT_INSTALL_DIR}

