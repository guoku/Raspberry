import os.path
from defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#mongodb setting
from mongoengine import register_connection
register_connection('guoku-db', 'guoku', username='qinzhoukan', password='qinzhoukan1@#',host='10.0.2.200',
        max_pool_size=200, auto_start_request=False, safe=True)
register_connection('log-db', 'guoku_log', host='10.0.2.200',
        max_pool_size=200, auto_start_request=False, safe=True)

MANGO_HOST = '10.0.2.200'
MANGO_PORT = 27017

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guoku',
        'USER': 'qinzhoukan',
        'PASSWORD': 'qinzhoukan1@#',
        'HOST': '10.0.2.90',
        'PORT': '',
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '10.0.2.49:6379',
        'TIMEOUT:': 864000,
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

# session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = '10.0.2.49'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 2
SESSION_COOKIE_AGE = 1209600
MAX_SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 14

MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']

SPHINX_API_VERSION = 0x116
SPHINX_SERVER = '10.0.2.50'
SPHINX_PORT = 9312

JUMP_TO_TAOBAO = True

IMAGE_LOCAL = DEBUG
IMAGE_SERVER  = 'http://imgcdn.guoku.com/'
APP_HOST = 'http://www.guoku.com'

CELERY_RESULT_BACKEND = "redis://10.0.2.100:6379/0"
BROKER_TRANSPORT = "librabbitmq"
BROKER_HOST = "10.0.2.100"
BROKER_USER = "raspberry"
BROKER_PASSWORD = "raspberry1@#"
BROKER_VHOST = "raspberry"
BROKER_POOL_LIMIT = 10
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_DISABLE_RATE_LIMITS = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
#    ('common', os.path.join(os.path.dirname(__file__), 'static')),
)



# List of callables that know how to import templates from various sources.

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'raspberry.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'djcelery',
    'base',
    'management',
    'mobile',
    'seller',
    'web',
    'gunicorn',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#GUOKU_APNS_KEY = os.path.join(os.path.dirname(__file__), 'apns_key/')
GUOKU_APNS_KEY = '/data/www/raspberry/apns_key/'
APNS_SERVER = {'HOST':'http://10.0.2.46:7077/'}


SCP_HOST = '10.0.2.46'
SCP_USER = 'jiaxin'
SCP_KEY = os.path.join(os.path.dirname(__file__), 'scp_key/')
SCP_REMOTE_FILE = '/data/www/core/download/android/guoku-release.apk'

ALLOWED_HOSTS = ['*']

