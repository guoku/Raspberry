# coding=utf-8
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views.event',
    url(r'^$', 'home', name='web_event_home'),
    url(r'^(?P<slug>\d+)/$', 'event', name='web_event'),
    url(r'^hongbao/$', 'hongbao', name='web_hongbao'),
    url(r'^hongbao/finished/$', 'hongbao_finished', name='web_hongbao_finished')
)

__author__ = 'edison'
