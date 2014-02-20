# coding=utf-8
from django.conf.urls import url, patterns, include

urlpatterns = patterns(
    'web.views.main',
    url(r'^$', 'index', name='web_index'),
    url('^selected/$', 'selection', name='web_selection'),
    url('^popular/$', 'popular', name='web_popular'),
    url('^discover/$', 'discover', name='web_discover'),
    url('^discover/product/$', 'discover_more', name='web_discover_more'),

    url(r'^shop/(?P<shop_id>\w+)/$', 'shop', name='web_shop'),
    url(r'^message/$', 'message', name='web_message'),
    url(r'^activity/$', 'activity', name='web_activity'),
)

urlpatterns += patterns(
    'web.views.entity',
    url(r'^detail/(?P<entity_hash>\w+)/$', 'entity_detail', name='web_detail'),
    url(r'^entity/', include('web.urls.entity')),
    url(r'^note/', include('web.urls.note')),
)


urlpatterns += patterns(
    'web.views.account',
    url(r'^login/$', 'login', name="web_login"),
    url(r'^logout/$', 'logout', name="web_logout"),
    url(r'^sina/login$', 'login_by_sina', name="web_login_by_sina"),
    url(r'^sina/auth/$', 'auth_by_sina', name="web_auth_by_sina"),
    url(r'^sina/bind/$', 'bind_sina', name="web_bind_sina"),
    url(r'^sina/unbind/$', 'unbind_sina', name="web_unbind_sina"),
    url(r'^taobao/login/$', 'login_by_taobao', name='web_login_by_taobao'),
    url(r'^taobao/bind/$', 'bind_taobao', name="web_bind_taobao"),
    url(r'^taobao/unbind/$', 'unbind_taobao', name="web_unbind_taobao"),
    url(r'^taobao/auth/$', 'auth_by_taobao', name="web_auth_by_taobao"),
    url(r'^taobao/shop/bind/$', 'bind_taobao_shop', name="web_bind_taobao_shop"),

    url(r'^account/', include('web.urls.account')),
    url(r'^u/', include('web.urls.user')),
)

urlpatterns += patterns(
    'web.views.search',
    url('^search/$', 'search', name='web_search')
)
