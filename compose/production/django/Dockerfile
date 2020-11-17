# syntax = docker/dockerfile:experimental
FROM node:10-stretch-slim as client-builder

WORKDIR /app
COPY ./package.json /app
RUN npm install && npm cache clean --force
COPY . /app
RUN npm run build

# Python build stage
FROM python:3.8-slim-buster
LABEL maintainer="Timo Halbesma <timo@halbesma.com>"
ENV PYTHONUNBUFFERED 1

RUN --mount=type=cache,mode=0755,target=/var/cache/apt --mount=type=cache,mode=0755,target=/var/lib/apt set -ex \
  && rm -f /etc/apt/apt.conf.d/docker-clean \
  && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
  && apt-get update \
  # dependencies for building Python packages
  && apt-get install --no-install-recommends -y build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  # non-privileged user
  && groupadd -g 1000 atlas \
  && useradd -r -u 1000 -g atlas atlas -s /bin/bash -d /atlas

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip set -ex \
  && pip install --no-cache-dir -r /requirements/production.txt

COPY --from=client-builder --chown=atlas:atlas /app /app

# Application layers
COPY --chown=atlas:atlas [ \
# Source
  "./compose/production/django/entrypoint", \
  "./compose/production/django/start", \
  "./compose/production/django/celery/worker/start-celeryworker", \
  "./compose/production/django/celery/beat/start-celerybeat", \
  "./compose/production/django/celery/flower/start-celeryflower", \
# Destination
  "/" \
]
RUN set -ex \
  && sed -i 's/\r$//g' /entrypoint \
  && chmod +x /entrypoint \
\
  && sed -i 's/\r$//g' /start \
  && chmod +x /start \
\
  && sed -i 's/\r$//g' /start-celeryworker \
  && chmod +x /start-celeryworker \
\
  && sed -i 's/\r$//g' /start-celerybeat \
  && chmod +x /start-celerybeat \
\
  && sed -i 's/\r$//g' /start-celeryflower \
  && chmod +x /start-celeryflower



USER atlas
WORKDIR /app

ENTRYPOINT ["/entrypoint"]
