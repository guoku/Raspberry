from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    'web.views.main',
    url('^selected/$', 'selection', name='web_selection'),
    url('^popular/$', 'popular', name='web_popular'),
    url('^discover/$', 'discover', name='web_discover'),
    url('^discover/product/$', 'discover_more', name='web_discover_more'),
    url('^detail/(?P<entity_hash>\w+)/$', 'detail', name='web_detail'),

    url('^shop/(?P<shop_id>\w+)/$', 'shop', name='web_shop'),
    url('^message/$', 'message', name='web_message'),
    url('^activity/$', 'activity', name='web_activity')
)


urlpatterns += patterns(
    'web.views.account',
    url('^login/$', 'login', name='web_login'),
    url('^login/sina/$', 'login_by_sina', name='web_login_by_sina'),
    url('^login/taobao/$', 'login_by_taobao', name='web_login_by_taobao'),

    url('^logout/$', 'logout', name='web_logout'),

    url('^register/$', 'register', name='web_register'),
    url('^register/bio/$', 'register_bio', name='web_register_bio'),
    url('^register/check_nickname_available/$', 'check_nickname_available', name='web_check_nickname_available'),
    url('^register/check_email_available/$', 'check_email_available', name='web_check_email_available'),

    url('^setting/$', 'setting', name='web_setting'),
    url('^setting/check_nickname_available/$', 's_check_nickname_available', name='web_s_check_nickname_available'),
    url('^setting/check_email_available/$', 's_check_email_available', name='web_s_check_email_available'),
    url('^setting/upload_avatar/$', 'upload_avatar', name='web_upload_avatar'),
    url('^setting/update_avatar$', 'update_avatar', name='web_update_avatar')
)


urlpatterns += patterns(
    'web.views.entity',
    url('^entity/new/$', 'load_entity', name='web_load_entity'),
    url('^entity/create/$', 'create_entity', name='web_create_entity'),
    url('^entity/(?P<entity_id>\w+)/like/$', 'like_entity', name='web_like_entity'),
    url('^entity/(?P<entity_id>\w+)/note/create/$', 'add_note', name='web_add_note'),
    url('^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/update/$', 'update_note', name='web_update_note'),
    url('^entity/(?P<entity_id>\w+)/note/(?P<note_id>\w+)/delete/$', 'delete_note', name='web_delete_note')
)


urlpatterns += patterns(
    'web.views.note',
    url('^note/(?P<note_id>\w+)/poke/$', 'poke_note', name='web_poke_note'),
    url('^note/(?P<note_id>\w+)/comment/create/$', 'add_comment', name='web_add_comment'),
    url('^note/(?P<note_id>\w+)/comment/(?P<comment_id>\w+)/delete/$', 'delete_comment', name='web_delete_comment')
)


urlpatterns += patterns(
    'web.views.user',
    url('^u/(?P<user_id>\w+)/$', 'user_index', name='web_user_index'),
    url('^u/(?P<user_id>\w+)/likes/$', 'user_likes', name='web_user_likes'),
    url('^u/(?P<user_id>\w+)/posts/$', 'user_posts', name='web_user_posts'),
    url('^u/(?P<user_id>\w+)/notes/$', 'user_notes', name='web_user_notes'),
    url('^u/(?P<user_id>\w+)/tags/$', 'user_tags', name='web_user_tags'),
    url('^u/(?P<user_id>\w+)/followings/$', 'user_followings', name='web_user_followings'),
    url('^u/(?P<user_id>\w+)/fans/$', 'user_fans', name='web_user_fans'),

    url('^u/(?P<user_id>\w+)/follow/$', 'follow', name='web_follow'),
)