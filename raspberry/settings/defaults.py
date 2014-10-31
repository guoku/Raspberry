import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('guoku', 'hi@guoku.com'),
)

MANAGERS = ADMINS

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '../conf/locale'),
)

# List of finder classes that know how to find static files in
# various locations.
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
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.request',
  'django.core.context_processors.media',
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.static',
)


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = '10.0.2.48'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 2
SESSION_COOKIE_AGE = 1209600
MAX_SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 14

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
          'level': 'ERROR',
          'class': 'logging.FileHandler',
          'formatter': 'verbose',
          'filename': '/tmp/djanog.log',
          'mode': 'a',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.formtools',
    'django.contrib.sitemaps',
    'djcelery',
    'base',
    'management',
    'mobile',
    'seller',
    'stats',
    'web',
    'share',
    # 'edm',
    # 'lotto',
    'gunicorn',
)



INTERNAL_IPS = ('127.0.0.1',)

# taobao api key and sercet
APP_HOST = "http://www.guoku.com"
TAOBAO_APP_KEY = '12313170'
TAOBAO_APP_SECRET = '90797bd8d5859aac971f8cc9d4e51105'
TAOBAO_OAUTH_URL = 'https://oauth.taobao.com/authorize'
TAOBAO_OAUTH_LOGOFF = 'https://oauth.taobao.com/logoff'
TAOBAO_BACK_URL = APP_HOST + "/taobao/auth"
TAOBAO_APP_INFO = {
    "default_app_key" : "12313170",
    "default_app_secret" : "90797bd8d5859aac971f8cc9d4e51105",
    "web_app_key" : "21419640",
    "web_app_secret" : "df91464ae934bacca326450f8ade67f7"
}

SINA_APP_KEY = '1459383851'
SINA_APP_SECRET = 'bfb2e43c3fa636f102b304c485fa2110'
SINA_BACK_URL = APP_HOST + '/sina/auth'


EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-7n8gut3y8rpk1u-0edgmgaj7vs50gig8'
MAILGUN_SERVER_NAME = 'post.guoku.com'
EMAIL_SUBJECT_PREFIX = '[guoku]'


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





MOGILEFS_DOMAIN = 'prod'
MOGILEFS_TRACKERS = ['10.0.2.50:7001']
IMAGE_LOCAL = DEBUG
IMAGE_SERVER  = 'http://imgcdn.guoku.com/'
IMAGES_SIZE = [64, 128, 240, 310, 480, 640]


# MOGILEFS_DOMAIN = 'prod'
# MOGILEFS_TRACKERS = ['10.0.2.50:7001']
MOGILEFS_MEDIA_URL = 'images/'
DEFAULT_FILE_STORAGE = 'storages.backends.mogile.MogileFSStorage'
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# IMAGE_SIZE = [128, 310, 640]

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/')
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/'
# STATIC_URL = '/static/v3/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


# scp

SCP_HOST = '10.0.2.46'
SCP_USER = 'jiaxin'
SCP_KEY = os.path.join(os.path.dirname(__file__), 'scp_key/')
SCP_REMOTE_FILE = '/data/www/core/download/android/guoku-release.apk'
