from mubasir.settings.base import *  # noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = secrets.SECRET_KEY

DEBUG = False

SERVER_URL = "http://mubasir.hack.hipolabs.com"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'mubasir.hack.hipolabs.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "mubasir",
        'USER': "mubasir",
        'PASSWORD': secrets.POSTGRES_PASSWORD,
        'HOST': "postgres",
        'PORT': '5433',
    }
}

sentry_sdk.init(
    dsn=secrets.SENTRY_DSN,
    integrations=[DjangoIntegration()]
)

# django-storages
#
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_FILE_OVERWRITE = False
AWS_STORAGE_BUCKET_NAME = "mubasir"
ROOT_MEDIA_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = ROOT_MEDIA_URL + 'media/'
STATIC_URL = ROOT_MEDIA_URL + 'static/'
AWS_ACCESS_KEY_ID = secrets.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = secrets.AWS_SECRET_ACCESS_KEY