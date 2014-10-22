from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.recommendation',
    url(r'^$', 'list', name='management_event_banner'),
    url(r'^create/$', 'create', name='management_event_banner_create'),
    url(r'^(?P<event_banner_id>\d+)/edit/$', 'edit', name='management_event_banner_edit'),
)

__author__ = 'edison'
