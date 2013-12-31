from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.entity',
    url(r'^$', 'entity_list', name='entity_list'),
    url(r'^search/$', 'search_entity', name='entity_search'),
    url(r'^new/$', 'new_entity', name='entity_new'),
    url(r'^create/taobao/$', 'create_entity_by_taobao_item', name='create_entity_from_taobao'),
    #url(r'^create/offline/$', 'create_entity_from_offline', name='create_entity_from_offline'),

)



__author__ = 'edison7500'

