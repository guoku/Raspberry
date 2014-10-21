from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.event',
    url(r'^$', '', name='management_event_banner'),
)

__author__ = 'edison'
