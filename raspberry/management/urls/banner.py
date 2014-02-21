from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.banner',
    url(r'^$', 'banner_list', name = 'management_banner_list'),
    url(r'^new/$', 'new_banner', name = 'management_new_banner'),
    url(r'^create/$', 'create_banner', name = 'management_create_banner'),
    url(r'^(?P<banner_id>\w+)/edit/$', 'edit_banner', name = 'management_edit_banner'),
    url(r'^(?P<banner_id>\w+)/delete/$', 'delete_banner', name = 'management_delete_banner'),
)

__author__ = 'edison7500'
