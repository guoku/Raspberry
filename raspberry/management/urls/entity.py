from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.entity',
    url(r'^$', 'entity_list', name = 'management_entity_list'),
    url(r'^search/$', 'search_entity', name = 'management_entity_search'),
    url(r'^new/$', 'new_entity', name = 'management_new_entity'),
    url(r'^create/taobao/$', 'create_entity_by_taobao_item', name = 'management_create_entity_by_taobao_item'),
    #url(r'^create/offline/$', 'create_entity_from_offline', name='create_entity_from_offline'),

    url(r'^(?P<entity_id>\w+)/edit/$', 'edit_entity', name = 'management_edit_entity'),
    url(r'^(?P<entity_id>\w+)/merge/$', 'merge_entity', name = 'management_merge_entity'),
    url(r'^(?P<entity_id>\w+)/recycle/$', 'recycle_entity', name = 'management_recycle_entity'),
    url(r'^(?P<entity_id>\w+)/edit/image/$', 'edit_entity_image', name = 'management_edit_entity_image'),
    url(r'^(?P<entity_id>\w+)/image/add/$', 'add_image_for_entity', name = 'management_add_image_for_entity'),
    url(r'^(?P<entity_id>\w+)/image/del/(?P<image_id>\w+)/$', 'del_image_from_entity', name = 'management_del_image_from_entity'),
    url(r'^(?P<entity_id>\w+)/taobao/item/load/$', 'load_taobao_item_for_entity', name = 'management_load_taobao_item_for_entity'),
    url(r'^(?P<entity_id>\w+)/taobao/item/add/$', 'add_taobao_item_for_entity', name = 'management_add_taobao_item_for_entity'),

    url(r'^(?P<entity_id>\w+)/taobao/item/(?P<item_id>\w+)/bind/$', 'bind_taobao_item_to_entity', name = 'management_bind_taobao_item_to_entity'),
    url(r'^(?P<entity_id>\w+)/taobao/item/(?P<item_id>\w+)/unbind/$', 'unbind_taobao_item_from_entity', name = 'management_unbind_taobao_item_from_entity'),
    url(r'^categories$', 'get_all_categories'),
    url(r'^item/taobao/state$', 'read_taobao_item_state')  # for chrome extension

)

__author__ = 'edison7500'

