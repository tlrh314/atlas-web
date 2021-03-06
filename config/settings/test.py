"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="bJBitj3nrOYBIfXWyog5Ch0xYnp5UhNDC6eEcHnv5P2FxwYOG60Kg205IDrrNb2Y",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# django-filebrowser-no-grappelli
# ------------------------------------------------------------------------------
#  https://github.com/smacker/django-filebrowser-no-grappelli
# We import the settings from the FileBrowser just now b/c the import must be
# done after the SECRET_KEY is already set (above)
from .filebrowser import *  # noqa isort:skip


# django-simple-captcha
# -------------------------------------------------------------------------------
# django-simple-captcha - https://django-simple-captcha.readthedocs.io/

# https://django-simple-captcha.readthedocs.io/en/latest/advanced.html#captcha-test-mode
CAPTCHA_TEST_MODE = True

# atlas-web specific settings
# ------------------------------------------------------------------------------
