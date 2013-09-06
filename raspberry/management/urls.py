__author__ = 'stxiong'
from django.conf.urls.defaults import *

urlpatterns = patterns('management.views',
    (r'^entity/$', 'entity_list'),
    (r'^entity/new/$', 'new_entity'),
    (r'^entity/create/taobao/$', 'create_entity_by_taobao_item'),
    (r'^entity/(?P<entity_id>\d+)/edit/$', 'edit_entity'),
)


