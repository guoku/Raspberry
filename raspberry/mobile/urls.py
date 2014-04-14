__author__ = 'stxiong'
from django.conf.urls import patterns, url, include

urlpatterns = patterns('mobile.views',
    (r'^login/$', 'login'),
    (r'^sina/login/$', 'login_by_sina'),
    (r'^taobao/login/$', 'login_by_taobao'),
    (r'^logout/$', 'logout'),
    (r'^register/$', 'register'),
    (r'^forget/password/$', 'forget_password'),
    (r'^sina/register/$', 'register_by_sina'),
    (r'^taobao/register/$', 'register_by_taobao'),
    (r'^apns/token/$', 'apns_token'),
    (r'^homepage/$', 'homepage'),
    (r'^popular/$', 'popular'),
    (r'^feed/$', 'feed'),
    (r'^selection/$', 'selection'),
    (r'^message/$', 'message'),
    (r'^unread/$', 'unread_count'),
    (r'^category/$', 'all_category'),
    (r'^category/(?P<category_id>\d+)/entity/$', 'category_entity'),
    (r'^category/(?P<category_id>\d+)/entity/note/$', 'category_entity_note'),
    (r'^category/(?P<category_id>\d+)/stat/$', 'category_stat'),
    (r'^category/(?P<category_id>\d+)/user/(?P<user_id>\d+)/like/$', 'category_user_like'),
    (r'^entity/$', 'entity_list'),
    (r'^entity/guess/$', 'guess_entity'),
    (r'^entity/search/$', 'search_entity'),
    (r'^entity/(?P<entity_id>\w+)/$', 'entity_detail'),
    (r'^entity/(?P<entity_id>\w+)/like/(?P<target_status>\d+)/$', 'like_entity'),
    (r'^entity/(?P<entity_id>\w+)/add/note/$', 'add_note_for_entity'),
    (r'^entity/(?P<entity_id>\w+)/report/$', 'report_entity'),
    (r'^entity/note/(?P<note_id>\d+)/$', 'entity_note_detail'),
    (r'^entity/note/(?P<note_id>\d+)/update/$', 'update_entity_note'),
    (r'^entity/note/(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke_entity_note'),
    (r'^entity/note/(?P<note_id>\d+)/add/comment/$', 'comment_entity_note'),
    (r'^entity/note/(?P<note_id>\d+)/del/$', 'delete_entity_note'),
    (r'^entity/note/(?P<note_id>\d+)/comment/(?P<comment_id>\d+)/del/$', 'delete_entity_note_comment'),
    (r'^entity/note/(?P<note_id>\d+)/report/$', 'report_entity_note'),
    (r'^entity/note/search/$', 'search_entity_note'),
    (r'^user/info/$', 'user_info'),
    (r'^user/(?P<user_id>\d+)/$', 'user_detail'),
    (r'^user/(?P<user_id>\d+)/follow/(?P<target_status>\d+)/$', 'follow_user'),
    (r'^user/(?P<user_id>\d+)/like/$', 'user_like'),
    (r'^user/(?P<user_id>\d+)/entity/note/$', 'user_entity_note'),
    (r'^user/(?P<user_id>\d+)/fan/$', 'user_fan'),
    (r'^user/(?P<user_id>\d+)/following/$', 'user_following'),
    (r'^user/(?P<user_id>\d+)/tag/$', 'user_tag_list'),
    (r'^user/tag/random/$', 'random_user_tag'),
    (r'^tag/recommend/$', 'recommend_user_tag'),
    (r'^user/(?P<user_id>\d+)/tag/(?P<tag>\w+)/$', 'user_tag_entity'),
    (r'^user/update/$', 'update_user'),
    (r'^user/search/$', 'search_user'),
    (r'^sina/user/check/$', 'check_sina_user'),
    (r'^item/(?P<item_id>\w+)/visit/$', 'visit_item'),
)

