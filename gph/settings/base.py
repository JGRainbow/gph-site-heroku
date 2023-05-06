'''
Django settings for gph project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
'''

import os, sys
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure logs directory exists.
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY', 'FIXME_SECRET_KEY_HERE')

# S3 Bucketeer
# AWS_ACCESS_KEY_ID = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID','')
# AWS_SECRET_ACCESS_KEY = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY', '')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKETEER_BUCKET_NAME','')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'public/static'

# Admin (running team) Discord integration
# ALERT_WEBHOOK_URL = os.environ.get('ALERT_WEBHOOK_URL','')
# SUBMISSION_WEBHOOK_URL = os.environ.get('SUBMISSION_WEBHOOK_URL','')
# FREE_ANSWER_WEBHOOK_URL = os.environ.get('FREE_ANSWER_WEBHOOK_URL','')
# VICTORY_WEBHOOK_URL = os.environ.get('VICTORY_WEBHOOK_URL','')
# FAILURE_WEBHOOK_URL = os.environ.get('FAILURE_WEBHOOK_URL','')
# DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN','')

RECAPTCHA_SITEKEY = None
RECAPTCHA_SECRETKEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'impersonate',
    'mathfilters',
    'channels',
    'puzzles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'puzzles.messaging.log_request_middleware',
    'puzzles.context.context_middleware',
    'puzzles.puzzlehandlers.reverse_proxy_middleware',
    'puzzles.views.accept_ranges_middleware',
]

redis_url = os.environ.get('REDIS_URL')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_url,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'CONNECTION_POOL_KWARGS': {
                'ssl_cert_reqs': None
            },
        },
    }
}

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
heroku_redis_ssl_host = {
    'address':redis_url,
    'ssl': ssl_context
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": (heroku_redis_ssl_host,)
        },
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'

ROOT_URLCONF = 'gph.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'puzzles.context.context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'gph.wsgi.application'
ASGI_APPLICATION = 'gph.asgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Apparently conn_max_age=0 is better for Heroku:
# https://stackoverflow.com/questions/48644208/django-postgresql-heroku-operational-error-fatal-too-many-connections-for-r
DATABASES = {
    'default': dj_database_url.config(conn_max_age=0, ssl_require=True),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us' #FIXME

TIME_ZONE = 'America/New_York' #FIXME

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.normpath(os.path.join(BASE_DIR, 'locale'))]
FORMAT_MODULE_PATH = ['gph.formats']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'static'))
SOLUTION_STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'puzzles/templates/solution_bodies'))
STATICFILES_STORAGE = 'gph.storage.CustomStorage'

# Email SMTP information

EMAIL_USE_TLS = True
EMAIL_HOST = 'FIXME'
EMAIL_HOST_USER = 'FIXME'
EMAIL_HOST_PASSWORD = 'FIXME'
EMAIL_PORT = 'FIXME'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[FIXME Puzzle Hunt] '

# https://docs.djangoproject.com/en/3.1/topics/logging/

# Loggers and handlers both have a log level; handlers ignore messages at lower
# levels. This is useful because a logger can have multiple handlers with
# different log levels.

# The levels are DEBUG < INFO < WARNING < ERROR < CRITICAL. DEBUG logs a *lot*,
# like exceptions every time a template variable is looked up and missing,
# which happens literally all the time, so that might be a bit too much.

# If you want to log to stdout (e.g. on Heroku), the handler looks as follows:
# {
#     'level': 'INFO',
#     'class': 'logging.StreamHandler',
#     'stream': sys.stdout,
#     'formatter': 'django',
# },

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django': {
            'format': '%(asctime)s (PID %(process)d) [%(levelname)s] %(module)s\n%(message)s'
        },
        'puzzles': {
            'format': '%(asctime)s (PID %(process)d) [%(levelname)s] %(name)s %(message)s'
        },
    },
    # FIXME you may want to change the filenames to something like
    # /srv/logs/django.log or similar
    handlers': {
        'django': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'django',
        },
        'general': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'puzzles',
        },
        'puzzle': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'puzzles',
        },
        'request': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'puzzles',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': 'INFO',
            'propagate': True,
        },
        'puzzles': {
            'handlers': ['general'],
            'level': 'INFO',
            'propagate': True,
        },
        'puzzles.puzzle': {
            'handlers': ['puzzle'],
            'level': 'INFO',
            'propagate': False,
        },
        'puzzles.request': {
            'handlers': ['request'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Google Analytics
GA_CODE = ''

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
