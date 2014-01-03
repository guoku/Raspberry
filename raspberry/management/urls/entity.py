from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.entity',
    url(r'^$', 'entity_list', name='entity_list'),
    url(r'^search/$', 'search_entity', name='entity_search'),
    url(r'^new/$', 'new_entity', name='entity_new'),
    url(r'^create/taobao/$', 'create_entity_by_taobao_item', name='create_entity_from_taobao'),
    #url(r'^create/offline/$', 'create_entity_from_offline', name='create_entity_from_offline'),

    url(r'^(?P<entity_id>\w+)/edit/$', 'edit_entity', name='entity_edited'),
    url(r'^(?P<entity_id>\w+)/merge/$', 'merge_entity', name='entity_merged'),
    url(r'^(?P<entity_id>\w+)/recycle/$', 'recycle_entity', name='entity_recycled'),
    url(r'^(?P<entity_id>\w+)/edit/image/$', 'edit_entity_image', name='entity_image_edited'),
    url(r'^(?P<entity_id>\w+)/image/add/$', 'add_image_for_entity'),
    url(r'^(?P<entity_id>\w+)/image/del/(?P<image_id>\w+)/$', 'del_image_from_entity'),
    url(r'^(?P<entity_id>\w+)/taobao/item/load/$', 'load_taobao_item_for_entity', name='load_taobao_item_for_entity'),
    url(r'^(?P<entity_id>\w+)/taobao/item/add/$', 'add_taobao_item_for_entity'),

    url(r'^(?P<entity_id>\w+)/taobao/item/(?P<item_id>\w+)/bind/$', 'bind_taobao_item_to_entity', name='taobao_item_bind_to_entity'),
    url(r'^(?P<entity_id>\w+)/taobao/item/(?P<item_id>\w+)/unbind/$', 'unbind_taobao_item_from_entity', name='taobao_item_unbind_from_entity'),
)



__author__ = 'edison7500'

