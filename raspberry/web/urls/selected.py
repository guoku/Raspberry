from django.conf.urls.defaults import url, patterns

#from web.views.selection import selection

urlpatterns = patterns(
    'web.views.selection',
    url(r'^$', 'selection'),
)

__author__ = 'edison7500'
