# coding=utf-8
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'web.views.tag',
    url('suggest/$', 'tag_suggest', name='web_tag_suggest'),
)
