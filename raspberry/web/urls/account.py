# coding=utf-8
from django.conf.urls import url, patterns
from web.views.account import RegisterWizard, ThirdPartyRegisterWizard
from web.forms.account import SignUpAccountFrom, SignUpAccountBioFrom

FORMS = [('register', SignUpAccountFrom),
         ('register-bio', SignUpAccountBioFrom)
        ]
urlpatterns = patterns(
    'web.views.account',
    url(r'^forget-passwd/', 'forget_passwd', name='web_forget_passwd'),
    url(r'^register/$', RegisterWizard.as_view(FORMS), name='web_register'),
    url(r'^thirdparty/register$', ThirdPartyRegisterWizard.as_view(FORMS), name='web_third_party_register'),

    url(r'^setting/$', 'setting', name='web_setting'),
    url(r'^setting/update_avatar$', 'update_avatar', name='web_update_avatar')
)
