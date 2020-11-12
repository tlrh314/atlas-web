.PHONY: all $(MAKECMDGOALS)

SHELL=/bin/bash

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

docker-pull:  ## Pull the latest Docker images from Dockerhub
	@docker pull python:3.8-slim-buster

django:  ## Build container for Django+Celery
	@make docker-pull
	@DOCKER_BUILDKIT=1 docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from tlrh314/atlas-web:local-build-stage \
		-f compose/local/django/Dockerfile \
		--target local-build-stage \
		-t tlrh314/atlas-web:local-build-stage .
	@DOCKER_BUILDKIT=1 docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from tlrh314/atlas-web:local-build-stage \
		--cache-from tlrh314/atlas-web:local \
		-f compose/local/django/Dockerfile \
		-t tlrh314/atlas-web:local .

django-start:  ## Start Django
	@docker-compose -f local.yml up -d django celeryworker

django-stop:  ## Stop Django
	@docker-compose -f local.yml stop django celeryworker
	@docker-compose -f local.yml rm -f django celeryworker

django-log:  ## Continously monitor the Django application server log
	@while true; do \
		docker logs -f --tail 1 django; \
		sleep 10; \
	done

log-all:  ## Continously monitor all containers
	@while true; do \
		docker-compose -f local.yml logs -f --tail 1; \
		sleep 10; \
	done

stop-all:  ## Stop Django and dependencies
	@docker-compose -f local.yml down
