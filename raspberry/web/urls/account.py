# coding=utf-8
from django.conf.urls import url, patterns
from web.views.account import RegisterWizard
from web.forms.account import SignUpAccountFrom, SignUpAccountBioFrom

urlpatterns = patterns(
    'web.views.account',
    # url('^login/$', 'login', name='web_login'),
    url('^login/sina/$', 'login_by_sina', name='web_login_by_sina'),
    url('^login/taobao/$', 'login_by_taobao', name='web_login_by_taobao'),

    # url('^logout/$', 'logout', name='web_logout'),
    url('register/$', RegisterWizard.as_view([SignUpAccountFrom, SignUpAccountBioFrom]), name='web_register'),

    # url('^register/$', 'register', name='web_register'),
    # url('^register/bio/$', 'register_bio', name='web_register_bio'),
    # url('^register/check_nickname_available/$', 'check_nickname_available', name='web_check_nickname_available'),
    # url('^register/check_email_available/$', 'check_email_available', name='web_check_email_available'),

    url('^setting/$', 'setting', name='web_setting'),
    # url('^setting/check_nickname_available/$', 's_check_nickname_available', name='web_s_check_nickname_available'),
    # url('^setting/check_email_available/$', 's_check_email_available', name='web_s_check_email_available'),
    url('^setting/upload_avatar/$', 'upload_avatar', name='web_upload_avatar'),
    url('^setting/update_avatar$', 'update_avatar', name='web_update_avatar')
)
