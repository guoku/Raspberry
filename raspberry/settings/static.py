import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/c6aa8a79d4b5fb77af662da4e8ca5d026f31c729/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/c6aa8a79d4b5fb77af662da4e8ca5d026f31c729/'
# STATIC_URL = '/static/v3/c6aa8a79d4b5fb77af662da4e8ca5d026f31c729/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
