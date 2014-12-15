import os



# static file

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../uploads')
MEDIA_URL = '/uploads/'
# STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/v3/6c1eefe379a3c2f67f13d1c3608138f3b213a0ac/'
STATIC_ROOT = '/tmp/static/'
STATIC_URL = 'http://static.guoku.com/static/v3/6c1eefe379a3c2f67f13d1c3608138f3b213a0ac/'
# STATIC_URL = '/static/v3/6c1eefe379a3c2f67f13d1c3608138f3b213a0ac/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (

)


__author__ = 'edison'
