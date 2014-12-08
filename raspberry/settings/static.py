import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/1fadbb09398bc4b629b8fbb4d3c3627a63da58ed/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/1fadbb09398bc4b629b8fbb4d3c3627a63da58ed/'
# STATIC_URL = '/static/v3/1fadbb09398bc4b629b8fbb4d3c3627a63da58ed/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
