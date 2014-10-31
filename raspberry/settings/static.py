import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/349ec170063b393127d62f7e6bd04cf701fb9d6a/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/349ec170063b393127d62f7e6bd04cf701fb9d6a/'
# STATIC_URL = '/static/v3/349ec170063b393127d62f7e6bd04cf701fb9d6a/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
