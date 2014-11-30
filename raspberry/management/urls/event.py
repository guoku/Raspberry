from django.conf.urls import url, patterns


urlpatterns = patterns(
    'management.views.event',
    url(r'^$', 'list', name='management_event'),
    url(r'^create/$', 'create', name='management_event_create'),
)

__author__ = 'edison'
