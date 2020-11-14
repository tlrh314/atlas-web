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
		--cache-from docker.gitlab.gwdg.de/solve/atlas-web:local-build-stage \
		-f compose/local/django/Dockerfile \
		--target local-build-stage \
		-t docker.gitlab.gwdg.de/solve/atlas-web:local-build-stage .
	@DOCKER_BUILDKIT=1 docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from docker.gitlab.gwdg.de/solve/atlas-web:local-build-stage \
		--cache-from docker.gitlab.gwdg.de/solve/atlas-web:local \
		-f compose/local/django/Dockerfile \
		-t docker.gitlab.gwdg.de/solve/atlas-web:local .

django-start:  ## Start Django
	@docker-compose -f local.yml up -d django celeryworker

django-stop:  ## Stop Django
	@docker-compose -f local.yml stop django celeryworker
	@docker-compose -f local.yml rm -f django celeryworker

django-restart:  ## Restart Django
	@make django-stop
	@make django-start

django-log:  ## Continously monitor the Django application server log
	@while true; do \
		docker logs -f --tail 1 django; \
		sleep 10; \
	done

django-run-from-image:  ## Run command in a tmp container from image, but /w database connection
	@docker-compose -f local.yml up -d postgres
	@docker run --network atlas \
		--env-file .envs/.local/.django \
		--env-file .envs/.local/.postgres \
		-it --rm --entrypoint=""\
		-v"$$(pwd):/app" \
		docker.gitlab.gwdg.de/solve/atlas-web:local \
		bash -c "python manage.py makemigrations users"

log-all:  ## Continously monitor all containers
	@while true; do \
		docker-compose -f local.yml logs -f --tail 1; \
		sleep 10; \
	done

stop-all:  ## Stop Django and dependencies
	@docker-compose -f local.yml down

test:  ## Run the test suite locally
	@docker exec -it django bash -c "coverage run -m pytest && coverage html && coverage report"


production:  ## Build production image (locally) for Django+Celery
	@make docker-pull
	@DOCKER_BUILDKIT=1 docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from docker.gitlab.gwdg.de/solve/atlas-web:production-client-builder \
		-f compose/production/django/Dockerfile \
		--target client-builder \
		-t docker.gitlab.gwdg.de/solve/atlas-web:production-client-builder .
	@DOCKER_BUILDKIT=1 docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		--cache-from docker.gitlab.gwdg.de/solve/atlas-web:production-client-builder \
		--cache-from docker.gitlab.gwdg.de/solve/atlas-web:production \
		-f compose/production/django/Dockerfile \
		-t docker.gitlab.gwdg.de/solve/atlas-web:production .

production-start:  ## Start Django locally from production build
	@docker-compose -f local.yml up -d django celeryworker

production-stop:  ## Stop Django locally from production build
	@docker-compose -f local.yml stop django celeryworker
	@docker-compose -f local.yml rm -f django celeryworker


runner-start:  ## Deploy GitLab runner at Hetzner Cloud
	@hcloud server create --location nbg1 --ssh-key tlrh314 --type cx11 \
		--image debian-10 --name atlasgitlabrunner \
		--user-data-from-file compose/hetzner/runner/cloudinit

ssh-runner:  ## SSH to the Runner VPS at Hetzner Cloud
	@ssh -i ~/.ssh/hcloud_runner -o StrictHostKeyChecking=no tlrh314@$$(hcloud server ip atlasgitlabrunner)

destroy-runner:  ## Destroy GitLab runner at Hetzner Cloud
	@hcloud server shutdown atlasgitlabrunner || true
	@hcloud server delete atlasgitlabrunner || true

runner-do-start:  ## Deploy GitLab runner at Digital Ocean
	@doctl compute droplet create dorunner \
		--user-data-file compose/hetzner/runner/cloudinit --region ams3 --image debian-10-x64 \
		--size s-1vcpu-1gb

ssh-do-runner:  ## SSH to the Runner VPS at Hetzner Cloud
	ssh -i ~/.ssh/hcloud_runner -o StrictHostKeyChecking=no tlrh314@$$(doctl compute droplet get dorunner --format PublicIPv4 | tail -n 1)


prototype-start:  ## Deploy prototype at Hetzner Cloud
	@hcloud server create --location nbg1 --ssh-key tlrh314 --type cx11 \
		--image debian-10 --name atlasprototype \
		--user-data-from-file compose/hetzner/prototype/cloudinit

ssh-prototype:  ## SSH to the prototype VPS
	@ssh -i ~/.ssh/hcloud_runner -o StrictHostKeyChecking=no tlrh314@$$(hcloud server ip atlasprototype)

destroy-prototype:  ## Destroy prototype at Hetzner Cloud
	@hcloud server shutdown atlasprototype || true
	@hcloud server delete atlasprototype || true
