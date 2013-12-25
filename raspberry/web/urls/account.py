from django.conf.urls.defaults import url, patterns


urlpatterns = patterns(
    'web.views.account',
    (r'^login/$', 'login'),
    (r'^login/sina/$', 'login_by_sina'),
    (r'^login/taobao/$', 'login_by_taobao'),
    (r'^logout/$', 'logout'),
    (r'^register/$', 'register'),
    (r'^register/validate_nickname/$', 'is_nickname_used'),
    (r'^register/validate_email/$', 'is_email_used')
)