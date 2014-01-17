from django.conf.urls import url, patterns
urlpatterns = patterns(
    'web.views',
    url(r'^selected/$', 'selected', name = "selection"),
    url(r'^login/$', 'login', name = "login"),
    url(r'^taobao/bind/$', 'bind_taobao', name = "bind_taobao"),
    url(r'^taobao/auth/$', 'taobao_auth', name = "taobao_auth"),
    url(r'^taobao/binding/check/$', 'bind_taobao_check', name = "check_taobao_binding"),
    url(r'^taobao/shop/bind/$', 'bind_taobao_shop', name = "bind_taobao_shop"),
)


