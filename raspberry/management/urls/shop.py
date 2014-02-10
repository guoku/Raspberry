from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.shop',
    url(r'^$', 'index', name = 'management_shop_index'),
    url(r'^list/$', 'shop_list', name = 'management_shop_list'),
    url(r'^add/$', 'add_shop', name = 'management_add_shop'),
    url(r'^detail/$', 'shop_detail', name = 'management_shop_detail'),
    url(r'^edit/$', 'edit_shop', name = 'management_edit_shop'),
)