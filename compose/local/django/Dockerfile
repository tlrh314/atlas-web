FROM python:3.8-slim-buster as local-build-stage

# BuildKit allows to mount cache for apt (and pip) to prevent re-downloading every time
# a full build is required.
# Sys layer /w build time dependencies
RUN set -ex \
  && apt-get update \
  # dependencies for building Python packages
  && apt-get install --no-install-recommends -y build-essential \
  # psycopg2 dependencies
    libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements /requirements
RUN set -ex \
  && pip wheel --no-deps --use-feature=2020-resolver --wheel-dir /usr/src/app/wheels \
    -r /requirements/local.txt

FROM python:3.8-slim-buster as local-run-stage
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
LABEL maintainer="Timo Halbesma <timo@halbesma.com>"

# Sys layer /w runtime dependencies
RUN set -ex \
  && rm -f /etc/apt/apt.conf.d/docker-clean \
  && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
  && apt update \
  # tlrh314 dependencies
  && apt install --no-install-recommends -y vim curl \
  # psycopg2 dependencies
    libpq-dev \
  # Translations dependencies
    gettext \
  # Pillow dependencies
    libz-dev libjpeg-dev libfreetype6-dev python-dev \
  # cleaning up unused files
  && apt purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  # non-privileged user
  && groupadd -g 1000 atlas \
  && useradd -r -u 1000 -g atlas atlas -s /bin/bash -d /atlas

# Pip layer
COPY --from=local-build-stage --chown=atlas:atlas /usr/src/app/wheels  /wheels
RUN pip install --no-cache /wheels/* \
  && rm -rf /wheels

# Application layers
COPY [ \
# Source
  "./compose/production/django/entrypoint", \
  "./compose/local/django/start", \
  "./compose/local/django/celery/worker/start-celeryworker", \
  "./compose/local/django/celery/beat/start-celerybeat", \
  "./compose/local/django/celery/flower/start-celeryflower", \
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
