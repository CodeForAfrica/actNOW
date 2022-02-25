"""
Django settings for actnow project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""


from pathlib import Path
from typing import List

import sentry_sdk
from environs import Env
from sentry_sdk.integrations.django import DjangoIntegration

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("ACTNOW_SECRET_KEY")

DEBUG = env.bool("ACTNOW_DEBUG", False)

ENVIRONMENT = env.str("DJANGO_ENV", "development")

ALLOWED_HOSTS: List[str] = env.str("ACTNOW_ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "oauth2_provider",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "phonenumber_field",
    "storages",
    "django_filters",
    # Local apps
    "actnow.db",
    "actnow.accounts",
    "actnow.profiles",
    "actnow.petitions",
    "actnow.site",
]

LOGIN_URL = "/admin/login/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "actnow.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path.joinpath(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "actnow.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {"default": env.dj_db_url("ACTNOW_DATABASE_URL")}


# Password hashing
# https://docs.djangoproject.com/en/3.2/ref/settings/#password-hashers

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "accounts.backends.ActNowBackend",
]

AUTH_USER_MODEL = "accounts.ActNowUser"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DRF
# https://www.django-rest-framework.org/#installation

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

SITE_ID = 1
REST_USE_JWT = True

# Django Oauth Toolkit settings
# https://django-oauth-toolkit.readthedocs.io/en/latest/settings.html#settings

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_GENERATOR": "actnow.accounts.tokens.signed_token_generator",
    "OAUTH2_VALIDATOR_CLASS": "actnow.accounts.oauth_validators.OAuth2Validator",
    "OIDC_ENABLED": False,
    "OIDC_RSA_PRIVATE_KEY": env.str("ACTNOW_OIDC_RSA_PRIVATE_KEY"),
    "SCOPES": {
        "openid": "Returns the sub claim, which uniquely identifies the user",
        "profile": "Returns claims that represent basic profile information",
        "email": "Returns the email claim",
    },
}


# Django Oauth Toolkit Application model
# https://django-oauth-toolkit.readthedocs.io/en/latest/settings.html#application-model

OAUTH2_PROVIDER_APPLICATION_MODEL = "accounts.ActNowApplication"
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = "accounts.AccessToken"
OAUTH2_PROVIDER_GRANT_MODEL = "accounts.Grant"
OAUTH2_PROVIDER_GRANT_MODEL = "accounts.Grant"
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = "accounts.RefreshToken"
OAUTH2_PROVIDER_ID_TOKEN_MODEL = "accounts.IDToken"

# AWS S3 Storage
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

ACTNOW_USE_S3 = env.bool("ACTNOW_USE_S3", False)
if ACTNOW_USE_S3:
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_SIGNATURE_VERSION = env.str("AWS_S3_SIGNATURE_VERSION", "s3v4")
    AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME")
    AWS_S3_FILE_OVERWRITE = env.bool("AWS_S3_FILE_OVERWRITE", False)
    AWS_LOCATION = env.str("AWS_LOCATION", "static")
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL", None)
    AWS_S3_VERIFY = env.bool("AWS_S3_VERIFY", True)
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

    DEFAULT_FILE_STORAGE = "actnow.storages_backends.MediaS3Boto3Storage"


# Sentry
# https://docs.sentry.io/platforms/python/guides/django/

SENTRY_DSN = env.str("ACTNOW_SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        send_default_pii=True,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        debug=DEBUG,
    )
