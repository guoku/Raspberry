import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/b515dc8212364abafe3e64d0bb267b53a1822974/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/b515dc8212364abafe3e64d0bb267b53a1822974/'
# STATIC_URL = '/static/v3/b515dc8212364abafe3e64d0bb267b53a1822974/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
