import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/c07e56764d6a27ea527a61d4958a17a9e0649f8c/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/c07e56764d6a27ea527a61d4958a17a9e0649f8c/'
# STATIC_URL = '/static/v3/c07e56764d6a27ea527a61d4958a17a9e0649f8c/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
