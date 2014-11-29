from django.conf.urls import url, patterns


urlpatterns = patterns(
    'management.views.event',
    url(r'^$', 'list', name=''),
)

__author__ = 'edison'
