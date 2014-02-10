# coding=utf-8
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views',
    url('new/$', 'load_entity', name='web_load_entity'),
    url('^create/$', 'create_entity', name='web_create_entity'),
    url('^(?P<entity_id>\w+)/like/$', 'like_entity', name='web_like_entity'),
    url('^(?P<entity_id>\w+)/note/$', 'get_notes', name='web_get_notes'),  # Ajax 方式获取点评
    url('^(?P<entity_id>\w+)/note/create/$', 'add_note', name='web_add_note'),
    url('^(?P<entity_id>\w+)/note/(?P<note_id>\w+)/update/$', 'update_note', name='web_update_note'),
    url('^(?P<entity_id>\w+)/note/(?P<note_id>\w+)/delete/$', 'delete_note', name='web_delete_note')
)