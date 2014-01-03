from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.category',
    url(r'^$', 'category_list', name = 'management_category_list'),
    url(r'^create/$', 'create_category', name = 'management_create_category'),
    # url(r'^sync/$', 'sync_category', name='category_sync'),
    url(r'(?P<category_id>\d+)/edit/$', 'edit_category', name = 'management_edit_category'),
    url(r'^group/create/$', 'create_category_group', name = 'management_create_category_group'),
    url(r'^group/(?P<category_group_id>\d+)/edit/$', 'edit_category_group', name = 'management_edit_category_group'),
)

__author__ = 'edison7500'
