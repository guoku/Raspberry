from django.conf.urls.defaults import *

urlpatterns = patterns(
    'web.views',

    #(r'^selection/$', 'selection'),
    (r'^popular/$', 'popular'),
    (r'^discover/$', 'discover'),
    (r'^detail/(?P<entity_hash>\w+)/$', 'detail'),

    (r'^login/$', 'login'),
    (r'^login/sina/$', 'login_by_sina'),
    (r'^login/taobao/$', 'login_by_taobao'),
    (r'^register/$', 'register'),
    (r'^register/validate_nickname/$', 'is_nickname_used'),
    (r'^register/validate_email/$', 'is_email_used')
)


