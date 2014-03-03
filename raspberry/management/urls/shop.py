from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.shop',
    url(r'^$', 'index', name = 'management_shop_index'),
    url(r'^list/$', 'shop_list', name = 'management_shop_list'),
    url(r'^add/$', 'add_shop', name = 'management_add_shop'),
    url(r'^detail/$', 'shop_detail', name = 'management_shop_detail'),
    url(r'^edit/$', 'edit_shop', name = 'management_edit_shop'),
    url(r'^guokuplus/application/list/$', 'guokuplus_application_list', name = 'management_guokuplus_application_list'),
    url(r'^guokuplus/application/detail/$', 'guokuplus_application_detail', name = 'management_guokuplus_application_detail'),
    url(r'^guokuplus/application/approve/$', 'approve_guokuplus_application', name = 'management_approve_guokuplus_application'),
    url(r'^guokuplus/application/editor_comment/add/$', 'add_guokuplus_application_editor_comment', name = 'management_add_guokuplus_app_editor_comment'),
)
