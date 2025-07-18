import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-6fgii6nn+_+--wgl^*fpp0+mfpi0ifkvc038urb&f5yr6b(!^y"
)


DEBUG = True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", "http://localhost:4000,http://localhost:3000"
).split(",")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "drf_spectacular_sidecar",
    "drf_spectacular",
    "clients",
    "ckeditor",
    "accounts",
    "projects",
    "jobs",
    "blog",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            # "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            # "querystring_auth": False,
            "location": "static",
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PG_DB_NAME"),
        "USER": os.getenv("PG_USER"),
        "PASSWORD": os.getenv("PG_PASSWORD"),
        "HOST": os.getenv("PG_HOST"),
        "PORT": os.getenv("PG_PORT", "5432"),
        "CONN_MAX_AGE": None,
        "OPTIONS": {"sslmode": os.getenv("PG_SSL_MODE")},
    }
}
AUTH_USER_MODEL = "accounts.User"

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


LANGUAGE_CODE = "en-us"


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = os.getenv("STATIC_URL", "static/")
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AWS_QUERYSTRING_AUTH = False

AWS_CLOUD_ACCESS_KEY_ID = os.getenv("AWS_CLOUD_ACCESS_KEY_ID")
AWS_CLOUD_SECRET_ACCESS_KEY = os.getenv("AWS_CLOUD_SECRET_ACCESS_KEY")
AWS_CLOUD_STORAGE_BUCKET_NAME = os.getenv("AWS_CLOUD_STORAGE_BUCKET_NAME")
AWS_CLOUD_S3_REGION_NAME = os.getenv("AWS_CLOUD_S3_REGION_NAME", "eu-north-1")
AWS_CLOUD_REGION = AWS_CLOUD_S3_REGION_NAME
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_CLOUD_STORAGE_BUCKET_NAME")

if DEBUG:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_CLOUD_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_CLOUD_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_CLOUD_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_CLOUD_S3_REGION_NAME", "eu-north-1")
    AWS_REGION = AWS_CLOUD_S3_REGION_NAME
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_CLOUD_STORAGE_BUCKET_NAME")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=90),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")


ADMINS = [
    ("Murad", "murad.dev@gumisofts.com"),
]
MANAGERS = []


# CKEditor Configuration
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
        "extraPlugins": ",".join(
            [
                "uploadimage",
                "div",
                "autolink",
                "autogrow",
                "widget",
                "lineutils",
            ]
        ),
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
