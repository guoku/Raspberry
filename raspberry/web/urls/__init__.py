from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    'web.views.main',
    ('^selection/$', 'selection'),
    (r'^popular/$', 'popular'),
    (r'^discover/$', 'discover'),
    (r'^detail/(?P<entity_hash>\w+)/$', 'detail')
)


urlpatterns += patterns(
    'web.views.accounts',
    (r'^accounts/login/$', 'login'),
    (r'^accounts/login/sina/$', 'login_by_sina'),
    (r'^accounts/login/taobao/$', 'login_by_taobao'),
    (r'^accounts/logout/$', 'logout'),
    (r'^accounts/register/$', 'register'),
    (r'^accounts/register/validate_nickname/$', 'is_nickname_used'),
    (r'^accounts/register/validate_email/$', 'is_email_used')
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


# urlpatterns += patterns(
#     'web.views.user',
#     (r'', '')
# )