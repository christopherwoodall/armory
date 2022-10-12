#!/usr/bin/make -f
# -*- makefile -*-

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

.ONESHELL:             ;   # Recipes execute in same shell
.NOTPARALLEL:          ;   # Wait for this target to finish
.SILENT:               ; 	 # No need for @
.EXPORT_ALL_VARIABLES: ;   # Export variables to child processes.
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables # DEBUGGING
MAKEFLAGS += --no-builtin-rules         # DEBUGGING

# Modify the block character to be `-\t` instead of `\t`
ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = -

.DEFAULT_GOAL := run

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
run:	## Run the application
-	@echo "Running..."


.PHONY: image
image: ## Build the docker image
-	@echo "Building image..."
- @echo "Tagging image as $(TAG)"
-	docker build --force-rm --progress=auto --tag twosixarmory/$(IMAGE_NAME):$(TAG) --file ./docker/Dockerfile .


.PHONY: latest
image: ## Build and tag the latest local version
-	@echo "Building image..."
- @echo "Tagging image as $(TAG)"
-	docker build --force-rm --progress=auto --tag twosixarmory/$(IMAGE_NAME):$(TAG) --file ./docker/Dockerfile .
- docker tag twosixarmory/$(IMAGE_NAME):$(TAG) twosixarmory/$(IMAGE_NAME):latest


.PHONY: push
push: ## Push the docker image
-	@echo "Pushing image..."
-	docker push twosixarmory/$(IMAGE_NAME):$(TAG)
-	docker push twosixarmory/$(IMAGE_NAME):latest


.PHONY: compose
compose: ## Run docker-compose
-	@echo "Running docker-compose..."
-	docker-compose up --remove-orphans --build armory-$(IMAGE_NAME)


## Developer Notes
# WIP: Windows support
#   For Windows users, you can use the following command to run this Makefile:
#     $ choco install make
#     $ make -f Makefile
#		>>>
#		>>> ifeq ($(OS),Windows_NT)
#		>>> SHELL := powershell.exe
#		>>> .SHELLFLAGS := -NoProfile -Command
#		>>> endif
