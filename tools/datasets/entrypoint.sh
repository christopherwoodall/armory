#!/usr/bin/env bash
# Entrypoint for the dataset service

trap cleanup SIGINT SIGTERM ERR EXIT

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
}



conda init bash
/bin/bash
