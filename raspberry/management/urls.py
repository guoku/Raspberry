__author__ = 'stxiong'
from django.conf.urls.defaults import *

urlpatterns = patterns('management.views',
    (r'^candidate/$', 'candidate_list'),
    (r'^candidate/(?P<candidate_id>\w+)/edit/$', 'edit_candidate'),
    (r'^candidate/(?P<candidate_id>\w+)/shift/entity/$', 'shift_candidate_to_entity'),
    (r'^category/$', 'category_list'),
    (r'^category/create/$', 'create_category'),
    (r'^category/sync/$', 'sync_category'),
    (r'^category/(?P<category_id>\d+)/edit/$', 'edit_category'),
    (r'^category/group/create/$', 'create_category_group'),
    (r'^entity/$', 'entity_list'),
    (r'^entity/search/$', 'search_entity'),
    (r'^entity/new/$', 'new_entity'),
    (r'^entity/create/taobao/$', 'create_entity_by_taobao_item'),
    (r'^entity/create/offline/$', 'create_entity_from_offline'),
    (r'^entity/(?P<entity_id>\w+)/edit/$', 'edit_entity'),
    (r'^entity/(?P<entity_id>\w+)/image/add/$', 'add_image_for_entity'),
    (r'^entity/(?P<entity_id>\w+)/taobao/item/load/$', 'load_taobao_item_for_entity'),
    (r'^entity/(?P<entity_id>\w+)/taobao/item/add/$', 'add_taobao_item_for_entity'),
    (r'^entity/(?P<entity_id>\w+)/taobao/item/(?P<item_id>\w+)/bind/$', 'bind_taobao_item_to_entity'),
    (r'^entity/(?P<entity_id>\w+)/taobao/item/(?P<item_id>\w+)/unbind/$', 'unbind_taobao_item_from_entity'),
    (r'^taobao/item/sync/$', 'sync_taobao_item'),
)


