from django.conf.urls.defaults import url, patterns, include

urlpatterns = patterns(
    '',
    url('^selected/$', include('web.urls.selected')),
)

__author__ = 'edison7500'
