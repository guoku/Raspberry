from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.tag',
    url(r'^$', 'user_tag_list', name = 'management_user_tag_list'),
)
