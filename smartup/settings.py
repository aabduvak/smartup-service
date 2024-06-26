"""
Django settings for smartup project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_file = os.path.join(BASE_DIR, ".env")

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)
IS_LOCAL = env("IS_LOCAL", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# SmartUp credentials
SMARTUP_LOGIN = env("SMARTUP_LOGIN")
SMARTUP_PASSWORD = env("SMARTUP_PASSWORD")
SMARTUP_URL = env("SMARTUP_URL")
BRANCHES_ID = env.list("BRANCHES_ID", default=[])

# Eskiz.uz credentials (SMS Provider)
ESKIZ_EMAIL = env("ESKIZ_EMAIL")
ESKIZ_PASSWORD = env("ESKIZ_PASSWORD")
ESKIZ_URL = env("ESKIZ_URL")
ESKIZ_DEFAULT_NICK = env("ESKIZ_DEFAULT_NICK")

# Database credentials
DB_HOST = env("DB_HOST")
DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
DB_NAME = env("DB_NAME")
DB_PORT = env("DB_PORT")

TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")
CHAT_ID = env("CHAT_ID")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "rest_framework",
    "drf_yasg",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smartup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "smartup.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if not IS_LOCAL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR + "/" + "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "smartup.urls.api_info",  # Reference to your API info dictionary
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",  # Token <value>
            "in": "header",
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "USER_DETAILS_SERIALIZER": "api.serializer.user.UserSerializer",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
