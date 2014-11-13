import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/2c85349224dc1755943a78ffad3ac9c1bb12d2d0/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/2c85349224dc1755943a78ffad3ac9c1bb12d2d0/'
# STATIC_URL = '/static/v3/2c85349224dc1755943a78ffad3ac9c1bb12d2d0/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
