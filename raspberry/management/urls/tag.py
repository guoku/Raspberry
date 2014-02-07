from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.tag',
    url(r'^$', 'user_tag_list', name = 'management_tag_list'),
    url(r'^(?P<tag>\w+)/user/(?P<user_id>\d+)/transcend/$', 'transcend_user_tag', name = 'management_transcend_user_tag'),
    url(r'^(?P<tag>\w+)/user/(?P<user_id>\d+)/freeze/$', 'freeze_user_tag', name = 'management_freeze_user_tag'),
)
