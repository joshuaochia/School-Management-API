from .base import *

# Override the base settings here

DEBUG = False

ALLOWED_HOSTS = ['Server-ip', 'your-domain-name']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Config for production data base
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


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,

    # Filters here
    'filters': {
        'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },

    # Formatter here
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{'
        }
    },

    # Handlers here
	'handlers': {
		'file': {
			'level': 'WARNING',
			'class': 'logging.FileHandler',
            'filename': LOG_DIR + 'debug.log',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
		},
	},
    
    # Logger here
    'loggers': {
        'django': {
            'handlers': ['file',],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            },
    },
}