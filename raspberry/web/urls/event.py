# coding=utf-8
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views.event',
    url(r'^$', 'home', name='web_event_home'),
    url(r'^(?P<slug>\d+)/$', 'event', name='web_event'),
)

__author__ = 'edison'
