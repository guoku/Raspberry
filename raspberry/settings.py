import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

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
#DATABASE_ROUTERS = ['router.AuthRouter'] 

from mongoengine import connect 
connect('guoku', host='10.0.2.200')

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

MOGILEFS_DOMAIN = 'staging'
MOGILEFS_TRACKERS = ['10.0.1.23:7001']

SPHINX_API_VERSION = 0x116
SPHINX_SERVER = 'localhost' 
SPHINX_port = 3312 


#mongo db
MANGO_HOST = '10.0.2.200'
MANGO_PORT = 27017


JUMP_TO_TAOBAO = True 

IMAGE_LOCAL = True 
IMAGE_SERVER  = 'http://10.0.1.109:8000/image/local/'
APP_HOST = "http://10.0.1.109:8001"
#IMAGE_LOCAL = False 
#IMAGE_SERVER  = 'http://imgcdn.guoku.com/'

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = False

#CELERY_RESULT_BACKEND = "redis"
#CELERY_REDIS_HOST = "localhost"
#CELERY_REDIS_PORT = 6379

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
BROKER_POOL_LIMIT = 10

GUOKU_APNS_KEY = os.path.join(os.path.dirname(__file__), 'apns_key/')
APNS_SERVER = {'HOST':'http://10.0.2.218:7077/'}

MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'static')
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3psdgd-e9ggs-0bjm9ghuu)mqlpj0xo87k4xmq3w@xg8kuk69r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  #'django.core.context_processors.static',
  'django.core.context_processors.i18n',
  'django.core.context_processors.request',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'zinnia.context_processors.version',
) # Optional

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
    'djcelery',
    'base',
    'management',
    'mobile',
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

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# taobao api key and sercet
TAOBAO_APP_KEY = '12313170'
TAOBAO_APP_SECRET = '90797bd8d5859aac971f8cc9d4e51105'
TAOBAO_OAUTH_URL = 'https://oauth.taobao.com/authorize'
TAOBAO_OAUTH_LOGOFF = 'https://oauth.taobao.com/logoff'

TAOBAO_APP_INFO = { 
    "default_app_key" : "12313170",
    "default_app_secret" : "90797bd8d5859aac971f8cc9d4e51105",
    "web_app_key" : "21419640",
    "web_app_secret" : "df91464ae934bacca326450f8ade67f7" 
}

