import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/0f5c3805942d25cad8d55d1bc1281300f97f3fc7/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/0f5c3805942d25cad8d55d1bc1281300f97f3fc7/'
# STATIC_URL = '/static/v3/0f5c3805942d25cad8d55d1bc1281300f97f3fc7/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
