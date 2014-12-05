# coding=utf-8
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views.event',
    url(r'^$', 'home', name='web_event_home'),
    url(r'^(?P<slug>\d+)/$', 'event', name='web_event'),
    url(r'^hongbao/$', 'hongbao', name='web_hongbao'),
    url(r'^hongbao/finished/(?P<hid>\d+)/$', 'hongbao_finished', name='web_hongbao_finished'),
    url(r'^hongbao/error/$', 'hongbao_error', name='web_hongbao_error'),
    url(r'^hongbao/error/(?P<hid>\d+)/$', 'hongbao_error', name='web_hongbao_already'),
)

__author__ = 'edison'
