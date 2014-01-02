from django.conf.urls import patterns, url


urlpatterns = patterns(
    'management.views.user',
    url(r'^$', 'user_list', name='user_list'),
    url(r'^(?P<user_id>\w+)/edit/$', 'edit_user', name='user_edited'),
    url(r'^(?P<user_id>\w+)/pust/message/$', 'push_message_to_user', name='push_message_to_user'),
)



__author__ = 'edison7500'
