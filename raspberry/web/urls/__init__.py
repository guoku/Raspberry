from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    'web.views.main',
    ('^selected/$', 'selection'),
    (r'^popular/$', 'popular'),
    (r'^discover/$', 'discover'),
    (r'^discover/product/$', 'discover'),
    (r'^detail/(?P<entity_hash>\w+)/$', 'detail'),
    (r'^shop/(?P<shop_id>\w+)/$', 'shop')
)


urlpatterns += patterns(
    'web.views.accounts',
    (r'^accounts/login/$', 'login'),
    (r'^accounts/login/sina/$', 'login_by_sina'),
    (r'^accounts/login/taobao/$', 'login_by_taobao'),
    (r'^accounts/logout/$', 'logout'),
    (r'^accounts/register/$', 'register'),
    (r'^accounts/register/check_nickname_available/$', 'check_nickname_available'),
    (r'^accounts/register/check_email_available/$', 'check_email_available'),
    (r'^accounts/setting/$', 'setting'),
    (r'^accounts/setting/base/$', 'set_base'),
    (r'^accounts/setting/psw/$', 'set_psw'),
    (r'^accounts/setting/upload_avatar/$', 'upload_avatar'),
    (r'^accounts/setting/update_avatar$', 'update_avatar'),
)


urlpatterns += patterns(
    'web.views.entity',
    (r'^entity/(?P<entity_id>\w+)/like/$', 'like_entity'),
    (r'^entity/(?P<entity_id>\w+)/note/create/$', 'add_note'),
    (r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/update/$', 'update_note'),
    (r'^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/delete/$', 'delete_note')
)


urlpatterns += patterns(
    'web.views.note',
    (r'^note/(?P<note_id>\w+)/comment/create/$', 'add_comment'),
    (r'^note/(?P<note_id>\w+)/comment/(?P<comment_id>\w+)/delete/$', 'delete_comment')
)


urlpatterns += patterns(
    'web.views.user',
    (r'^u/(?P<user_id>\w+)/$', 'user_index'),
    (r'^u/(?P<user_id>\w+)/likes/$', 'user_likes'),
    (r'^u/(?P<user_id>\w+)/posts/$', 'user_posts'),
    (r'^u/(?P<user_id>\w+)/notes/$', 'user_notes'),
    (r'^u/(?P<user_id>\w+)/tags/$', 'user_tags'),
    (r'^u/(?P<user_id>\w+)/followings/$', 'user_followings'),
    (r'^u/(?P<user_id>\w+)/fans/$', 'user_fans')
)