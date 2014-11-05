# import os.path
from defaults import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG


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
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'guoku',
        'USER': 'qinzhoukan',
        'PASSWORD': 'qinzhoukan1@#',
        'HOST': '10.0.2.95',
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
        'LOCATION': '10.0.2.48:6379',
        'TIMEOUT:': 864000,
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}



# MOGILEFS_TRACKERS = ['10.0.2.50:7001']

SPHINX_API_VERSION = 0x116
SPHINX_SERVER = '10.0.2.50'
SPHINX_PORT = 9312

JUMP_TO_TAOBAO = True

IMAGE_LOCAL = DEBUG
IMAGE_SERVER  = 'http://imgcdn.guoku.com/'
APP_HOST = 'http://www.guoku.com'


# MOGILEFS_DOMAIN = 'prod'
# MOGILEFS_TRACKERS = ['10.0.2.50:7001']
# MOGILEFS_MEDIA_URL = 'images/'
# DEFAULT_FILE_STORAGE = 'storages.backends.mogile.MogileFSStorage'
# IMAGE_SIZE = [128, 310, 640]



# MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
# MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/')


# Additional locations of static files
# STATICFILES_DIRS = (
#
# )



# List of callables that know how to import templates from various sources.

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'raspberry.urls'



#GUOKU_APNS_KEY = os.path.join(os.path.dirname(__file__), 'apns_key/')
GUOKU_APNS_KEY = '/data/www/raspberry/apns_key/'
APNS_SERVER = {'HOST': 'http://10.0.2.46:7077/'}




# APP_HOST = "http://test.guoku.com"
SINA_BACK_URL = APP_HOST + '/sina/auth'
TAOBAO_BACK_URL = APP_HOST + "/taobao/auth"

ENABLE_GUOKU_PLUS = True

ALLOWED_HOSTS = ['guoku.com', 'www.guoku.com', 'admin.guoku.com', 'api.guoku.com']