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
        'HOST': "hackdb.cmq91upkqjfq.us-east-1.rds.amazonaws.com",
        'PORT': '5433',
    }
}

sentry_sdk.init(
    dsn=secrets.SENTRY_DSN,
    integrations=[DjangoIntegration()]
)
