import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/bfac09d6e4aca982a85dc2aeb4c57aea1f0e766d/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/bfac09d6e4aca982a85dc2aeb4c57aea1f0e766d/'
# STATIC_URL = '/static/v3/bfac09d6e4aca982a85dc2aeb4c57aea1f0e766d/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
