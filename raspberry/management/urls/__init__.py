from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    'management.views',
    url(r'^category/sync/$', 'sync.sync_category', name = 'management_sync_category'),
    url(r'^entity/create/offline/$', 'sync.create_entity_from_offline', name = 'management_create_entity_from_offline'),
    url(r'^taobao/item/sync/$', 'sync.sync_taobao_item', name = 'management_sync_taobao_item'),
    url(r'^selection/sync/$', 'sync.sync_selection', name = 'management_sync_selection'),
    url(r'^entity/without/title/sync/$', 'sync.sync_entity_without_title', name = 'management_sync_entity_without_title'),
    url(r'^update/entity/(?P<entity_id>\w+)/title/sync/$', 'sync.sync_update_entity_title', name = 'management_sync_update_entity_title'),

    url(r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/post/selection/instant/$', 'note.post_selection_instant', name = 'management_post_selection_instant'),
    url(r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/post/selection/delay/$', 'note.post_selection_delay', name = 'management_post_selection_delay'),
    url(r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/update/selection/info/$', 'note.update_note_selection_info', name = 'management_update_note_selection_info'),
    
    url(r'^item(?P<item_id>\w+)/update/$', 'entity.update_item', name = 'management_update_item'),

    url(r'^banner/', include('management.urls.banner')),
    url(r'^category/', include('management.urls.category')),
    url(r'^entity/', include('management.urls.entity')),
    url(r'^note/', include('management.urls.note')),
    url(r'^mobile/', include('management.urls.mobile_app')),
    url(r'^report/', include('management.urls.report')),
    url(r'^user/', include('management.urls.user')),
    url(r'^ustation/', include('management.urls.ustation')),
    url(r'^shop/', include('management.urls.shop')),
    url(r'^tag/', include('management.urls.tag')),

    url(r'^event/', include('management.urls.event')),
    url(r'^event-banner/', include('management.urls.event_banner')),
    url(r'^recommend/', include('management.urls.recommendation')),
)

__author__ = 'edison7500'
