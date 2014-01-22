# coding=utf-8
from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    'web.views.note',
    url('^(?P<note_id>\w+)/poke/$', 'poke_note', name='web_poke_note'),
    url('^(?P<note_id>\w+)/comment/$', 'get_comments', name='web_get_comments'),  # Ajax 方式获取评论
    url('^(?P<note_id>\w+)/comment/create/$', 'add_comment', name='web_add_comment'),
    url('^(?P<note_id>\w+)/comment/(?P<comment_id>\w+)/delete/$', 'delete_comment', name='web_delete_comment')
)