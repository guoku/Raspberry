__author__ = 'stxiong'
from django.conf.urls.defaults import *

urlpatterns = patterns('mobile.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^register/$', 'register'),
    (r'^homepage/$', 'homepage'),
    (r'^search/$', 'search'),
    (r'^feed/$', 'feed'),
    (r'^message/$', 'message'),
    (r'^category/$', 'all_category'),
    (r'^category/(?P<category_id>\d+)/entity/$', 'category_entity'),
    (r'^entity/$', 'entity_list'),
    (r'^entity/guess/$', 'guess_entity'),
    (r'^entity/(?P<entity_id>\w+)/$', 'entity_detail'),
    (r'^entity/(?P<entity_id>\w+)/like/(?P<target_status>\d+)/$', 'like_entity'),
    (r'^entity/(?P<entity_id>\w+)/add/note/$', 'add_note_for_entity'),
    (r'^entity/note/(?P<note_id>\d+)/update/$', 'update_note'),
    (r'^entity/note/(?P<note_id>\d+)/$', 'note_detail'),
    (r'^entity/note/(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke_note'),
    (r'^entity/note/(?P<note_id>\d+)/add/comment/$', 'comment_note'),
    (r'^user/(?P<user_id>\d+)/$', 'user_detail'),
    (r'^user/(?P<user_id>\d+)/follow/(?P<target_status>\d+)/$', 'follow_user'),
    (r'^user/(?P<user_id>\d+)/like/$', 'user_like'),
    (r'^user/(?P<user_id>\d+)/entity/note/$', 'user_entity_note'),
    (r'^user/(?P<user_id>\d+)/fan/$', 'user_fan'),
    (r'^user/(?P<user_id>\d+)/following/$', 'user_following'),
    (r'^user/update/$', 'update_user'),
)

