from django.conf.urls.defaults import url, patterns

urlpatterns = patterns(
    'management.views.category',
    url(r'^$', 'category_list', name='category_list'),
    url(r'^create/$', 'create_category', name='category_created'),
    url(r'^sync/$', 'sync_category', name='category_sync'),
    url(r'(?P<category_id>\d+)/edit/$', 'edit_category', name='category_edit'),
    url(r'^group/create/$', 'create_category_group', name='category_group_created'),
    url(r'^group/(?P<category_group_id>\d+)/edit/$', 'edit_category_group', name='category_group_edit'),
)

__author__ = 'edison7500'
