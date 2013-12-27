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
    (r'^entity/(?P<entity_id>\w+)/add_note/$', 'add_note'),
    (r'^entity/(?P<note_id>\w+)/update_note/$', 'update_note'),
    (r'^entity/(?P<note_id>\w+)/delete_note/$', 'delete_note')
)


# urlpatterns += patterns(
#     'web.views.note',
#     (r'', '')
# )
#
#
# urlpatterns += patterns(
#     'web.views.user',
#     (r'', '')
# )