from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.banner',
    url(r'^$', 'banner_list', name='banner_list'),
    url(r'^new/$', 'new_banner', name='new_banner'),
    url(r'^create/$', 'create_banner', name='create_banner'),
    url(r'^(?P<banner_id>\w+)/delete/$', 'delete_banner', name='delete_banner'),
)

__author__ = 'edison7500'
