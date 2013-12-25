from django.conf.urls.defaults import url, patterns, include


urlpatterns = patterns(
    '',
    ('^selection/$', 'web.views.main.selection'),
    (r'^popular/$', 'web.views.main.popular'),
    (r'^discover/$', 'web.views.main.discover'),
    (r'^detail/(?P<entity_hash>\w+)/$', 'web.views.main.detail')
)


urlpatterns += patterns(
    'web.views.account',
    (r'^account/login/$', 'login'),
    (r'^account/login/sina/$', 'login_by_sina'),
    (r'^account/login/taobao/$', 'login_by_taobao'),
    (r'^account/logout/$', 'logout'),
    (r'^account/register/$', 'register'),
    (r'^account/register/validate_nickname/$', 'is_nickname_used'),
    (r'^account/register/validate_email/$', 'is_email_used')
)


# urlpatterns += patterns(
#     'web.views.entity',
#     (r'', '')
# )
#
#
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