from .settings_common import *

import os

# ------------------------------------------------------------------------------
# CORE
# ------------------------------------------------------------------------------

DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "changeme-super-secret-key"
)

HOSTNAME = os.environ.get(
    "HOSTNAME",
    "localhost"
)

ALLOWED_HOSTS = ["*"]

# ------------------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "rapidpro"),
        "USER": os.environ.get("POSTGRES_USER", "rapidpro"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "rapidpro"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

DATABASES["readonly"] = DATABASES["default"].copy()

# ------------------------------------------------------------------------------
# REDIS
# ------------------------------------------------------------------------------

# REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
# REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))

REDIS_URL = os.environ.get("VALKEY_URL", "")

# ------------------------------------------------------------------------------
# CELERY
# ------------------------------------------------------------------------------

#CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "")
CELERY_TASK_ALWAYS_EAGER = False #Alberto False para Producción, True para desarrollo
CELERY_TASK_EAGER_PROPAGATES = False #Alberto False para Producción, True para desarrollo

# ------------------------------------------------------------------------------
# MAILROOM
# ------------------------------------------------------------------------------

MAILROOM_URL = os.environ.get(
    "MAILROOM_URL",
    "http://mailroom:8090"
)

MAILROOM_AUTH_TOKEN = os.environ.get(
    "MAILROOM_AUTH_TOKEN",
    ""
)


# ------------------------------------------------------------------------------
# STORAGE
# ------------------------------------------------------------------------------

# Local storage (dev)
STORAGE_ROOT = "/rapidpro/storage"

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

USE_X_FORWARDED_HOST = True

# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# ------------------------------------------------------------------------------
# BRANDING
# ------------------------------------------------------------------------------

BRAND = {
    "name": "RapidPro",
    "description": "Visually build nationally scalable mobile applications anywhere in the world.",
    "hosts": ["nncd.mx"],
    "domain": "rapidpro.nncd.mx",
    "emails": {"notifications": "nono.desarrollo@broxel.com"},
    "logos": {
        "primary": "images/logo-dark.svg",
        "favico": "https://nonocard.com/wp-content/uploads/2024/11/cropped-iconnono-32x32.png",
        "avatar": "brands/rapidpro/rapidpro-avatar.webp",
    },
    "landing": {
        "hero": "brands/rapidpro/splash.jpg",
    },
    "features": ["sso"],
    "features": ["signups", "sso"],
}

# ------------------------------------------------------------------------------
# TIMEZONE
# ------------------------------------------------------------------------------

TIME_ZONE = "America/Mexico_City"

# ------------------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------------------
STATIC_URL = "/sitestatic/"
# print(f"PROJECT_DIR: {PROJECT_DIR}")
# print(f"STATIC_ROOT: {STATIC_ROOT}")
# print(f"STATIC_URL: {STATIC_URL}")

# ------------------------------------------------------------------------------
# INTERNAL ADDRESSES
# ------------------------------------------------------------------------------

INTERNAL_IPS = ["127.0.0.1"]

##ALBERTO NONO DEV
MIDDLEWARE = (
    MIDDLEWARE[:1]
    + ("whitenoise.middleware.WhiteNoiseMiddleware",)
    + MIDDLEWARE[1:]
)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

DYNAMO_ENDPOINT_URL = os.environ.get("DYNAMO_ENDPOINT_URL", "")
DYNAMO_TABLE_PREFIX = os.environ.get("DYNAMO_TABLE_PREFIX", "")

ELASTIC_ENDPOINT_URL = os.environ.get("ELASTIC_ENDPOINT_URL", "http://elastic:9200")

S3_SESSIONS_BUCKET = os.environ.get("S3_SESSIONS_BUCKET", "rapidpro-sessions")
S3_ATTACHMENTS_BUCKET = os.environ.get("S3_ATTACHMENTS_BUCKET", "rapidpro-attachments")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": S3_ATTACHMENTS_BUCKET  # o S3_SESSIONS_BUCKET según tu lógica
        },
    },
    "archives": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": S3_ATTACHMENTS_BUCKET  # usa el que requieras
        },
    },
    "public": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": S3_ATTACHMENTS_BUCKET,
            "signature_version": "s3v4",
            #"default_acl": "public-read",
            "querystring_auth": False,
            # Aquí pon el custom_domain SOLO si tienes un CDN/bucket website configurado,
            # si no, puedes omitirlo (Django devolverá enlaces de S3 firmados/reales)
            # "custom_domain": "rapidpro.nono-labs.com/media",
        },
    },
    "staticfiles": {
        # "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

AWS_S3_REGION_NAME = os.environ.get("AWS_REGION", "us-east-1")
AWS_S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT", "https://storage.googleapis.com")
AWS_S3_ADDRESSING_STYLE = "path" if os.environ.get("S3_PATH_STYLE", "true").lower() in ("1", "true", "yes", "on") else "virtual"
AWS_S3_FILE_OVERWRITE = False

STORAGE_URL = f"{AWS_S3_ENDPOINT_URL}/{S3_ATTACHMENTS_BUCKET}"


# -----------------------------------------------------------------------------------
# Cache
# -----------------------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django_valkey.cache.ValkeyCache",
        "LOCATION": REDIS_URL,
    }
}

# STATIC_URL = "/static/"

##EMAIL
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "false").lower() == "true"
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", 10))

###Permissions

permissions_str = os.environ.get('VIEWER_PERMISSIONS', '')

# Convertir a lista, ignorando líneas vacías
GROUP_PERMISSIONS["Viewers"] = [
    line.strip() 
    for line in permissions_str.splitlines() 
    if line.strip()  # solo líneas no vacías
]

print(f"VIEWER_PERMISSIONS: {GROUP_PERMISSIONS['Viewers']}")