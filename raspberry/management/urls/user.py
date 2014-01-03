from django.conf.urls import patterns, url


urlpatterns = patterns(
    'management.views.user',
    url(r'^$', 'user_list', name = 'management_user_list'),
    url(r'^(?P<user_id>\w+)/edit/$', 'edit_user', name = 'management_edit_user'),
    url(r'^(?P<user_id>\w+)/pust/message/$', 'push_message_to_user', name = 'management_push_message_to_user'),
)



__author__ = 'edison7500'
