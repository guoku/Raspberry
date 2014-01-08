from django.conf.urls.defaults import *

urlpatterns = patterns(
    'web.views',
    (r'^selected/$', 'selected', name = "selection"),
    (r'^taobao/bind$', 'bind_taobao', name = "bind_taobao")
    (r'^taobao/auth$', 'taobao_auth', name = "taobao_auth")
    (r'^taobao/binding/check$', 'bind_taobao_check', name = "check_taobao_binding")
)


