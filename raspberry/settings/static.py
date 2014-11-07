import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/7131b7bbf49ffba83aba563cbbdd2f6544804bdb/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/7131b7bbf49ffba83aba563cbbdd2f6544804bdb/'
# STATIC_URL = '/static/v3/7131b7bbf49ffba83aba563cbbdd2f6544804bdb/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
