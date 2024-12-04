from .base import *

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="your-production-domain.com").split(",")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("POSTGRES_DB"),
        'USER': config("POSTGRES_USER"),
        'PASSWORD': config("POSTGRES_PASSWORD"),
        'HOST': config("POSTGRES_HOST", default="localhost"),
        'PORT': config("POSTGRES_PORT", default="5432"),
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
