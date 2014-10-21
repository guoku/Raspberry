# coding=utf-8
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views.event',
    url(r'^$', 'home', name='web_event_home'),
)

__author__ = 'edison'
