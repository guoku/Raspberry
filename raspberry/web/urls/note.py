from django.conf.urls import url, patterns


urlpatterns = patterns(
    'web.views.note',
    url('^(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke_note', name='web_poke_note'),
    url('^(?P<note_id>\d+)/comment/$', 'get_comments', name='web_get_comments'),
    url('^(?P<note_id>\d+)/comment/create/$', 'add_comment', name='web_add_comment'),
    url('^(?P<note_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', 'delete_comment', name='web_delete_comment')
)
