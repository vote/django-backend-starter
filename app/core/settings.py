"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from typing import Any, Dict, Optional

import ddtrace
import environs
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

env = environs.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


#### ANALYTICS & TRACKING TAGS SETUP

ENV = env.str("ENV", default="dev")
TAG = env.str("TAG", default="")
BUILD = env.str("BUILD", default="0")

#### END ANALYTICS & TRACKING TAGS SETUP


#### STANDARD DJANGO SETTINGS SETUP

SECRET_KEY = env.str("SECRET_KEY", default="SET_THIS_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default="localhost")
DEBUG = env.bool("DEBUG", default=False)
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

#### END STANDARD DJANGO SETTINGS SETUP


#### CELERY & CELERY BEAT SETUP

CELERY_BROKER_URL = env.str("REDIS_URL", default="redis://redis:6379")
CELERY_RESULT_BACKEND = "django-db"
CELERY_WORKER_CONCURRENCY = env.int("CELERY_WORKER_CONCURRENCY", default=8)
CELERY_TASK_SERIALIZER = "json"

# specify a max_loop_interval AND lock timeout that ensure we don't
# pause too long during/after a redeploy
CELERY_BEAT_MAX_LOOP_INTERVAL = 5
CELERY_REDBEAT_LOCK_TIMEOUT = 30

CELERY_TASK_DEFAULT_QUEUE = "default"

# CELERY BEAT SCHEDULE

CELERY_BEAT_SCHEDULE: Any = {}

#### END CELERY & CELERY BEAT SETUP


#### APPLICATION SETUP

DEFAULT_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS: list[str] = [
    "rest_framework",
    "django_celery_results",
    "django_alive",
]

FIRST_PARTY_APPS: list[str] = [
    # "first_party_app",
]

INSTALLED_APPS: list[str] = DEFAULT_APPS + THIRD_PARTY_APPS + FIRST_PARTY_APPS

#### END APPLICATION SETUP


#### MIDDLEWARE SETUP

MIDDLEWARE: list[str] = [
    "django_alive.middleware.healthcheck_bypass_host_check",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

#### END MIDDLEWARE SETUP


#### TEMPLATES SETUP

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates",],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#### END TEMPLATES SETUP


#### DATABASE SETUP

DATABASES: dict[str, Any] = {
    "default": env.dj_db_url(
        "DATABASE_URL", default="postgres://postgres:django@postgres:5432/django"
    ),
}

#### END DATABASE SETUP


#### PASSWORD SETUP
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

#### END PASSWORD SETUP


#### INTERNATIONALIZATION SETUP

LANGUAGE_CODE: str = "en-us"

TIME_ZONE: str = "UTC"

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

#### END INTERNATIONALIZATION SETUP


#### FILE HANDLING SETUP

# STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL: str = "/static/"
STATIC_ROOT: str = os.path.join(BASE_PATH, "static")


#### END FILE HANDLING SETUP


#### LOGGING SETUP

# Use JSON logging in production, but standard logging during development
LOGGING_HANDLER: str = "console" if DEBUG else "json"

DJANGO_LOGGING_LEVEL = env.str("DJANGO_LOGGING_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler",},
        "json": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(name) %(message)s %(levelname) %(module) %(filename) %(funcName) %(lineno)",
        }
    },
    # INDIVIDUAL LOGGERS
    "loggers": {
        "django": {"handlers": [LOGGING_HANDLER], "level": DJANGO_LOGGING_LEVEL,},
        "ddtrace": {"handlers": [LOGGING_HANDLER], "level": DJANGO_LOGGING_LEVEL,},
        "common": {
            "handlers": [LOGGING_HANDLER],
            "level": DJANGO_LOGGING_LEVEL,
            "propagate": False,
        },
    },
}

#### END LOGGING SETUP


#### AWS CONFIGURATION

AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="")
AWS_DEFAULT_REGION = env.str("AWS_DEFAULT_REGION", default="us-east-1")

#### END AWS CONFIGURATION


#### DJANGO-ALIVE HEALTHCHECK CONFIGURATION

ALIVE_CHECKS: dict[str, dict[Optional[str], Optional[str]]] = {
    "django_alive.checks.check_migrations": {},
}

#### END ALIVE CONFIGURATION


#### DATADOG APM CONFIGURATION

ddtrace.tracer.set_tags({"build": BUILD})

#### END DATADOG APM CONFIGURATION


#### STATSD CONFIGURATION

STATSD_TAGS: list[str] = [
    f"env:{ENV}",
    f"image_tag:{TAG}",
    f"build:{BUILD}",
]

#### END STATSD CONFIGURATION


#### SENTRY CONFIGURATION

SENTRY_DSN = env.str("SENTRY_DSN", default="")
if TAG and SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN, # type: ignore
        integrations=[DjangoIntegration(), RedisIntegration(), CeleryIntegration()],
        send_default_pii=True,
        release=f"django@{TAG}",
        environment=ENV, # type: ignore
    )

    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("build", BUILD)
        scope.set_tag("tag", TAG)

#### END SENTRY CONFIGURATION
