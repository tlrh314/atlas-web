.PHONY: all $(MAKECMDGOALS)

SHELL=/bin/bash

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

docker-pull:  ## Pull the latest Docker images from Dockerhub
	@docker pull python:3.8-slim-buster

django:  ## Build image for Django+Celery container
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

django-start:  ## Start Django+Celery
	@docker-compose -f local.yml up -d django celeryworker

django-stop:  ## Stop Django+Celery
	@docker-compose -f local.yml stop django celeryworker
	@docker-compose -f local.yml rm -f django celeryworker

django-restart:  ## Restart Django+Celery
	@make django
	@make django-stop
	@make django-start

bash:  ## Open an interactive bash shell in the django container
	@docker exec -it django bash

manage:  ## Open an interactive Django shell [iPython interpreter]
	@docker exec -it django bash -c "python manage.py shell_plus"

django-log:  ## Continously monitor the Django application server log
	@while true; do \
		docker logs -f --tail 1 django; \
		sleep 10; \
	done || true

django-run-from-image:  ## Run command in a tmp container from image, but /w postgres database connection
	@docker-compose -f local.yml up -d postgres
	@docker run --network atlas \
		--env-file .envs/.local/.django \
		--env-file .envs/.local/.postgres \
		-it --rm --entrypoint=""\
		-v"$$(pwd):/app" \
		docker.gitlab.gwdg.de/solve/atlas-web:local \
		bash -c "python manage.py makemigrations users"


django-sites-fix:  ## Set the correct Site instance (locally)
	@docker exec django python manage.py shell -c \
		"from django.contrib.sites.models import Site; print(Site.objects.all()); \
		Site.objects.all().delete(); \
		print(Site.objects.get_or_create(pk=1, domain='localhost:8000', name='localhost:8000'))"; \

log-all:  ## Continously monitor all containers
	@while true; do \
		docker-compose -f local.yml logs -f --tail 1; \
		sleep 10; \
	done || true

stop-all:  ## Stop Django and dependencies
	@docker-compose -f local.yml down

test:  ## Run the test suite (locally)
	@docker exec -it django bash -c "coverage run -m pytest && coverage html && coverage report"

docs:  ## Build the documentation for Read the Docs
	@DOCKER_BUILDKIT=1 docker build \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		-f compose/local/docs/Dockerfile \
		-t docker.gitlab.gwdg.de/solve/atlas-web:docs .

docs-start:  ## Start Docs
	@docker-compose -f local.yml up -d docs

docs-stop:  ## Stop Docs
	@docker-compose -f local.yml stop docs
	@docker-compose -f local.yml rm -f docs

docs-restart:  ## Restart Docs
	@make docs
	@make docs-stop
	@make docs-start

production:  ## Build production image for Django+Celery
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

production-start:  ## Start Django+Celery running from from production build
	@docker-compose -f production.yml up --build -d django celeryworker

production-stop:  ## Stop Django+Celery running from the production build
	@docker-compose -f production.yml stop django celeryworker
	@docker-compose -f production.yml rm -f django celeryworker

production-restart:  ## Restart Django+Celery running from the production build
	@# Note that this command relies on a project access token created at
	@# https://gitlab.gwdg.de/SOLVe/atlas-web/-/settings/access_tokens
	@# with scopes read_repository, read_registry, and write_registry. The command
	@# `git remote get-url origin` then shows
	@# https://<username>:<token>@gitlab.gwdg.de/SOLVe/atlas-web where you would
	@# replace <username> and <token> with the real values (i.e. the characters
	@# '<' and '>' are not present in the real origin url.).
	@# Example: https://prototype:secret@gitlab.gwdg.de/SOLVe/atlas-web.
	@#   For Docker authentication+authorization to the registry we used
	@# `docker login docker login docker.gitlab.gwdg.de` once, which saved a hash
	@# of the username (name of the token) and password on disk ~/.docker/config.json.
	@echo -e "\n\033[0;35mPulling in latest changes on master\033[0;49m\n"
	@git pull
	@echo -e "\n\033[0;35mPulling in latest image from registry\033[0;49m\n"
	@docker pull docker.gitlab.gwdg.de/solve/atlas-web:production || true
	@echo -e "\n\033[0;35mBuilding new production image /w latest code on master\033[0;49m\n"
	@make production
	@echo -e "\n\033[0;35mStopping the running Django+Celery containers\033[0;49m\n"
	@make production-stop
	@echo -e "\n\033[0;35mStarting the running Django+Celery containers from our newly build image\033[0;49m\n"
	@make production-start
	@echo -e "\n\033[0;35mPushing the latest production build to our registry\033[0;49m\n"
	@docker push docker.gitlab.gwdg.de/solve/atlas-web:production
	@echo -e "\n\033[0;35mCleaning up dangling images\033[0;49m\n"
	@docker image prune -f
	@# The last step is to check on localhost that our public-facing container
	@# is responding to requests for the given hostname that Django accepts, and
	@# to return non-zero exit status (--fail) such that the pipeline will fail if
	@# it's not healthy. If you need to debug: remove the -s (silent) flag to see output.
	@# Note that the -k flag is because we curl on https://localhost, but the Let's Encrypt
	@# certificate is only valid for the real host (atlas.halbesma.com).
	@echo -e "\n\033[0;35mChecking if our Django container is ready to serve\033[0;49m\n"
	@curl -k --fail --retry 5 --retry-delay 3 --connect-timeout 30 -I -H "Host: atlas.halbesma.com" https://localhost
	@# We can also check the real host, but DNS resolves to the reverse proxy (MPS webserver)
	@# so that might not tell us about problems with the application server (the exposed)
	@# Docker container on localhost.
	@echo -e "\n\033[0;35mChecking if our public domain is healthy\033[0;49m\n"
	@curl --fail -s -I https://atlas.halbesma.com

remove-pycache:  ## Recursively clean pycache in path
	find .  ! -path "."  -type d -name '__pycache__' -exec rm -rvf {} \;

remove-buildkit-cache:  ## Clear the BuildKit cache
	@docker builder prune --filter type=exec.cachemount
	@echo "If prune of BuildKit cache /w cachemount filter still leaves too much dangling"
	@echo "cache such that your Docker data storage is still full, dare prune w/o filter"

prototype-start:  ## Deploy prototype at Hetzner Cloud
	@hcloud server create --location nbg1 --ssh-key tlrh314 --type cx11 \
		--image debian-10 --name atlasprototype \
		--user-data-from-file compose/hetzner/prototype/cloudinit

ssh-prototype:  ## SSH to the prototype VPS
	@ssh -i ~/.ssh/hcloud_runner -o StrictHostKeyChecking=no tlrh314@$$(hcloud server ip atlasprototype) || true

destroy-prototype:  ## Destroy prototype at Hetzner Cloud
	@hcloud server shutdown atlasprototype || true
	@hcloud server delete atlasprototype || true
