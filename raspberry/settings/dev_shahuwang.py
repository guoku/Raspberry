import os.path
from defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
from mongoengine import register_connection 
register_connection('guoku-db', 'guoku')
register_connection('log-db', 'guoku_log')

ENABLE_GUOKU_PLUS = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'guoku_11_21',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '',                      
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'guoku_11_21',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '',                      
        'OPTIONS': {
            'use_unicode':'utf-8',
            'init_command':'SET storage_engine=INNODB',
        }
    },
}
#DATABASE_ROUTERS = ['router.AuthRouter']
'''
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": [
            "localhost:6379:1",
        ],
        "OPTIONS": {
            "PARSER_CLASS": "redis.connection.HiredisParser",
            "CLIENT_CLASS": "redis_cache.client.ShardClient",
        }
    }
}
'''
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'TIMEOUT:': 864000,
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

# session
#SESSION_ENGINE = 'redis_sessions.session'
#SESSION_REDIS_HOST = 'localhost'
#SESSION_REDIS_PORT = 6379
#SESSION_REDIS_DB = 2
#SESSION_COOKIE_AGE = 1209600

MOGILEFS_DOMAIN = 'staging'
MOGILEFS_TRACKERS = ['10.0.1.23:7001']

SPHINX_API_VERSION = 0x116
SPHINX_SERVER = '10.0.1.109' 
SPHINX_port = 3312 


#mongo db
MANGO_HOST = 'localhost'
MANGO_PORT = 27017


JUMP_TO_TAOBAO = True 

IMAGE_LOCAL = True 
IMAGE_SERVER  = 'http://10.0.1.109/image/local/'
APP_HOST = "http://10.0.1.133:80"
ALLOWED_HOSTS = ['*']
#IMAGE_LOCAL = False 
#IMAGE_SERVER  = 'http://imgcdn.guoku.com/'

#CELERY_RESULT_BACKEND = "redis"
#CELERY_REDIS_HOST = "localhost"
#CELERY_REDIS_PORT = 6379

BROKER_HOST = "10.0.1.109"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
BROKER_POOL_LIMIT = 10

GUOKU_APNS_KEY = os.path.join(os.path.dirname(__file__), 'apns_key/')
APNS_SERVER = {'HOST':'http://10.0.2.218:7077/'}

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/v3/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
BASE_DIR = os.getcwd()

# Additional locations of static files
STATICFILES_DIRS = (
    # ('common', os.path.join(BASE_DIR, 'static')),
    #('common', os.path.join(os.path.dirname(__file__), '../static')),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'raspberry.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'debug_toolbar',
    'djcelery',
    'base',
    'management',
    'mobile',
    'seller',
    'web',
    # 'redis_admin',
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
        }, }
}

