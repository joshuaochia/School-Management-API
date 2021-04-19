from .base import *

# Override the base settings here


DEBUG = False
ALLOWED_HOSTS = ['Server-ip', 'your-domain-name'] # Config this one
CSRF_COOKIE_SECURE = True

#Config for production data base
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your-db-name',
        'USER': 'your-db-user-name',
        'PASSWORD': 'your-db-password',
        'HOST': 'localhost',
        'PORT': '',
    }
}