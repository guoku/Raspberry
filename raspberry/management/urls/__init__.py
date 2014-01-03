from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    'management.views',
    url(r'^category/sync/$', 'sync.sync_category', name='sync_category'),
    url(r'^entity/create/offline/$', 'sync.create_entity_from_offline', name='create_entity_from_offline'),

    url(r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/post/selection/instant/$', 'note.post_selection_instant', name='post_selection_instant'),
    url(r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/post/selection/delay/$', 'note.post_selection_delay', name='post_selection_delay'),
    url(r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/update/selection/info/$', 'note.update_note_selection_info', name='update_note_selection_info'),

    url(r'^category/', include('management.urls.category')),
    url(r'^entity/', include('management.urls.entity')),
    url(r'^note/', include('management.urls.note')),
    url(r'^banner/', include('management.urls.banner')),
    url(r'^user/', include('management.urls.user')),
    url(r'report/', include('management.urls.report')),
)

__author__ = 'edison7500'
