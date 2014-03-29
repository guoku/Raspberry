from django.conf.urls import patterns, url


urlpatterns = patterns(
    'management.views.user',
    url(r'^$', 'user_list', name='management_user_list'),
    url(r'^(?P<user_id>\w+)/edit/$', 'edit_user', name='management_edit_user'),
    url(r'^(?P<user_id>\w+)/set/censor/$', 'set_censor', name='management_set_user_censor'),
    url(r'^(?P<user_id>\w+)/cancel/censor/$', 'cancel_censor', name='management_cancel_user_censor'),
    url(r'^(?P<user_id>\w+)/pust/message/$', 'push_message_to_user', name='management_push_message_to_user'),
    url(r'^(?P<user_id>\w+)/note/freeze/all/$', 'freeze_user_note_all', name='management_freeze_user_note_all'),
)



__author__ = 'edison7500'
