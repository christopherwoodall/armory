#!/usr/bin/make -f
# -*- makefile -*-

SHELL         := /bin/bash
.SHELLFLAGS   := -eu -o pipefail -c
.DEFAULT_GOAL := help

.ONESHELL:             ;   # Recipes execute in same shell
.NOTPARALLEL:          ;   # Wait for this target to finish
.SILENT:               ; 	 # No need for @
.EXPORT_ALL_VARIABLES: ;   # Export variables to child processes.
.DELETE_ON_ERROR:      ;   # Delete target if recipe fails.

# MAKEFLAGS += --warn-undefined-variables # DEBUGGING
# MAKEFLAGS += --no-builtin-rules         # DEBUGGING

# Modify the block character to be `-\t` instead of `\t`
ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = -

ifeq ($(OS),Windows_NT)
SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command
.DEFAULT_GOAL := windows
endif


default: $(.DEFAULT_GOAL)
all: help

TAG = $(shell armory --version 2> /dev/null | sed -r 's/\+/\./g')
IMAGE_NAME = fortress


.PHONY: help
help: ## List commands
-	@echo -e "USAGE: make \033[36m[COMMAND]\033[0m\n"
-	@echo "Available commands:"
-	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\t\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: run
run: ## Place a commonly used command here
- ARMORY_DEV_MODE=1 ARMORY_PRETEND_VERSION=0.17.0 armory run scenario_configs/cifar10_baseline.json --check


.PHONY: venv
venv:	## Setup a Virtual Environment
-	echo -e "\033[36mSetting up virtual environment...\033[0m"
- rm -rf venv
- python -m pip install --upgrade virtualenv
- python -m virtualenv venv
- source venv/bin/activate
- python -m pip install --upgrade pip
- pip install -e '.[developer]'


.PHONY: ipython
ipython:	## Setup an iPython Virtual Environment
-	echo -e "\033[36mSetting up virtual environment...\033[0m"
- rm -rf venv
- python -m pip install --upgrade virtualenv
- python -m virtualenv venv
- source venv/bin/activate
- python -m pip install --upgrade pip
- pip install ipykernel
- pip install -e '.[developer]'
- ipykernel


# TODO: check that armory is installed
.PHONY: image
image: ## Build the docker image
-	echo -e "\033[36mBuilding image...\033[0m"
-	echo -e "\033[36mTagging image as $(TAG)\033[0m"
-	docker build --target base --tag twosixarmory/$(IMAGE_NAME)-base:$(TAG) --file ./docker/Dockerfile .
- docker build --target staging --cache-from twosixarmory/$(IMAGE_NAME)-base:$(TAG) --tag twosixarmory/$(IMAGE_NAME)-staging:$(TAG) --file ./docker/Dockerfile .
- docker build --target pre-release --cache-from twosixarmory/$(IMAGE_NAME)-staging:$(TAG) --tag twosixarmory/$(IMAGE_NAME)-pre-release:$(TAG) --file ./docker/Dockerfile .
- docker build --target release --cache-from twosixarmory/$(IMAGE_NAME)-pre-release:$(TAG) --tag twosixarmory/$(IMAGE_NAME):$(TAG) --file ./docker/Dockerfile .


.PHONY: latest
latest: ## Tag local version as latest
# -	echo -e "\033[36mBuilding image..."
- echo -e "\033[36mTagging image as $(TAG)\033[0m"
# -	docker build --force-rm --compress --progress=auto --tag twosixarmory/$(IMAGE_NAME):$(TAG) --file ./docker/Dockerfile .
- docker tag twosixarmory/$(IMAGE_NAME):$(TAG) twosixarmory/$(IMAGE_NAME):latest


.PHONY: push
push: ## Push the docker image
-	echo -e "\033[36mPushing image...\033[0m"
# TODO: Build make image latest first
-	docker push twosixarmory/$(IMAGE_NAME):$(TAG)
-	docker push twosixarmory/$(IMAGE_NAME):latest


.PHONY: compose
compose: ## Run docker-compose
-	echo -e "\033[36mRunning docker-compose...\033[0m"
-	docker-compose up --remove-orphans --build armory-$(IMAGE_NAME)


##
# WIP: Windows support
#   For Windows users, you can use the following command to run this Makefile:
#     $ choco install make
#     $ make -f Makefile
.PHONY: windows
windows: ## WIP: Windows
-	echo "Work in Progress..."
-	echo "Check back soon!"


.PHONY: lint
lint: ## Lint the code
-	echo -e "\033[36mLinting the code...\033[0m"
- ./tools/pre-commit.sh
