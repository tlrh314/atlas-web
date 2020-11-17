from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="AUYKxLm7jw3kA2LkDCa91BouaQTMAEy3hUKzMO0j9haSOMX1VGB5HACqyC0s4pBv",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
if env.bool("USE_DEBUG_TOOLBAR", default=False):
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    if env("USE_DOCKER") == "yes":
        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-silk
# ------------------------------------------------------------------------------
# https://github.com/jazzband/django-silk#installation
if env.bool("USE_SILK", default=True):
    INSTALLED_APPS += ["silk"]  # noqa F405
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]  # noqa F405
    SILKY_AUTHENTICATION = True
    SILKY_AUTHORISATION = True  # default is_staff=True; overwrite below
    SILKY_PERMISSIONS = lambda user: user.is_superuser  # noqa E731
    SILKY_PYTHON_PROFILER = False
    SILKY_PYTHON_PROFILER_BINARY = False
    SILKY_PYTHON_PROFILER_RESULT_PATH = str(ROOT_DIR / "profiles")  # noqa F405
    # SILKY_MAX_REQUEST_BODY_SIZE = -1     # Silk takes anything <0 as no limit
    # SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
    # SILKY_INTERCEPT_PERCENT = 50 # log only 50% of requests
    # SILKY_MAX_RECORDED_REQUESTS = 10**4  # garbage collection of old data
    # SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10
    SILKY_META = True  # to check the effect Silk itself has on response time

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# django-filebrowser-no-grappelli
# ------------------------------------------------------------------------------
#  https://github.com/smacker/django-filebrowser-no-grappelli
# We import the settings from the FileBrowser just now b/c the import must be
# done after the SECRET_KEY is already set (above)
from .filebrowser import *  # noqa isort:skip

# Celery
# ------------------------------------------------------------------------------

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# atlas-web
# ------------------------------------------------------------------------------#
