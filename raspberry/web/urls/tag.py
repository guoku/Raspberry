# coding=utf-8
from django.conf.urls import url, patterns

urlpatterns = patterns(
    'web.views.tag',
    url(r'^(?P<tag_hash>\w+)/$', 'tag_detail', name='web_tag_detail'),
)
