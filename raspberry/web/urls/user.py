# coding=utf-8
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views.user',
    url('^(?P<user_id>\w+)/$', 'user_index', name='web_user_index'),
    url('^(?P<user_id>\w+)/likes/$', 'user_likes', name='web_user_likes'),
    url('^(?P<user_id>\w+)/notes/$', 'user_notes', name='web_user_notes'),
    url('^(?P<user_id>\w+)/tags/$', 'user_tags', name='web_user_tags'),
    url('^(?P<user_id>\w+)/followings/$', 'user_followings', name='web_user_followings'),
    url('^(?P<user_id>\w+)/fans/$', 'user_fans', name='web_user_fans'),

    url('^(?P<user_id>\w+)/follow/(?P<target_status>\d+)/$', 'follow', name='web_follow'),
    url('^(?P<user_id>\w+)/tag/(?P<tag_hash>\w+)/$', 'user_tag_entity', name='web_user_tag_entity'),
)
