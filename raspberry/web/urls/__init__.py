# coding=utf-8
from django.conf.urls import url, patterns, include

from web.views.account import RegisterWizard, ThirdPartyRegisterWizard
from web.forms.account import SignUpAccountFrom, SignUpAccountBioFrom

FORMS = [
    ('register', SignUpAccountFrom),
    ('register-bio', SignUpAccountBioFrom)
]

urlpatterns = patterns(
    'web.views.main',
    url(r'^$', 'index', name='web_index'),
    url('^selected/$', 'selection', name='web_selection'),
    url('^m/selection/$', 'wap_selection', name='wap_selection'),
    url('^popular/$', 'popular', name='web_popular'),
    url(r'^c/', include('web.urls.category')),
    url(r'^t/', include('web.urls.tag')),
)

urlpatterns += patterns(
    'web.views.tag',
    url(r'^tag/suggest/$', 'tag_suggest', name='web_tag_suggest'),
)

urlpatterns += patterns(
    'web.views.entity',
    url(r'^detail/(?P<entity_hash>\w+)/$', 'entity_detail', name='web_detail'),
    url(r'^m/detail/(?P<entity_hash>\w+)/$', 'wap_entity_detail', name='wap_detail'),
    url(r'^entity/', include('web.urls.entity')),
    url(r'^note/', include('web.urls.note')),
)

urlpatterns += patterns(
    'web.views.account',
    url(r'^login/$', 'login', name="web_login"),
    url(r'^register/$', RegisterWizard.as_view(FORMS), name='web_register'),
    url(r'^logout/$', 'logout', name="web_logout"),
    url(r'^sina/login$', 'login_by_sina', name="web_login_by_sina"),
    url(r'^sina/auth/$', 'auth_by_sina', name="web_auth_by_sina"),
    url(r'^sina/bind/$', 'bind_sina', name="web_bind_sina"),
    url(r'^sina/unbind/$', 'unbind_sina', name="web_unbind_sina"),
    url(r'^taobao/login/$', 'login_by_taobao', name='web_login_by_taobao'),
    url(r'^taobao/bind/$', 'bind_taobao', name="web_bind_taobao"),
    url(r'^taobao/unbind/$', 'unbind_taobao', name="web_unbind_taobao"),
    url(r'^taobao/auth/$', 'auth_by_taobao', name="web_auth_by_taobao"),

    url(r'^account/', include('web.urls.account')),
    url(r'^u/', include('web.urls.user')),
)

urlpatterns += patterns(
    'web.views.search',
    url('^search/$', 'search', name='web_search')
)
