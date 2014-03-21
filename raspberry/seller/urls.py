from django.conf.urls import url, patterns


urlpatterns = patterns(
    "seller.views",
    url(r'^$', 'index', name = 'seller_index'),
    url(r'^commodities/$', 'commodities', name = 'seller_commodities'),
    url(r'^shop/bind/$', 'bind_taobao_shop', name = 'seller_bind_taobao_shop'),
    url(r'^shop/confirm/$', 'confirm_current_taobao_shop', name = 'seller_confirm_current_taobao_shop'),
    url(r'^guokuplus/list/$', 'guokuplus_list', name = 'seller_guoku_plus_list'),
    url(r'^verify/$', 'verify', name = 'seller_verify'),
    url(r'^guokuplus/apply/$', 'apply_guoku_plus', name = 'seller_apply_guoku_plus'),
    url(r'^guokuplus/detail/$', 'guoku_plus_detail', name = 'seller_guoku_plus_detail'),
    url(r'^guokuplus/token/verify/$', 'verify_token', name = 'seller_verify_token'),
    url(r'^faq$', 'faq', name = 'seller_faq'),
)
