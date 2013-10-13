__author__ = 'stxiong'
from django.conf.urls.defaults import *

urlpatterns = patterns('mobile.views',
    (r'^login/$', 'login'),
#    url(r'^logout/$', 'logout'),
    (r'^register/$', 'register'),
    (r'^homepage/$', 'homepage'),
    (r'^search/$', 'search'),
    (r'^category/$', 'all_category'),
    (r'^category/(?P<category_id>\d+)/entity/$', 'category_entity'),
    (r'^entity/(?P<entity_id>\w+)/$', 'entity_detail'),
    (r'^entity/(?P<entity_id>\w+)/like/(?P<target_status>\d+)/$', 'like_entity'),
    (r'^entity/(?P<entity_id>\w+)/add/note/$', 'add_note_for_entity'),
    (r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\d+)/$', 'entity_note_detail'),
    (r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke_entity_note'),
    (r'^follow/user/(?P<followee_id>\d+)/(?P<target_status>\d+)/$', 'follow_user'),
    (r'^user/(?P<user_id>\d+)/like/$', 'user_like'),
    (r'^user/(?P<user_id>\d+)/note/$', 'user_note'),
)

