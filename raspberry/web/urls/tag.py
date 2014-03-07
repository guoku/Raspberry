# coding=utf-8
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'web.views.tag',
    url(r'^(?P<tag_hash>\w+)/$', 'tags', name='web_tags'),
)
