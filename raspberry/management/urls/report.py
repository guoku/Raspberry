from django.conf.urls import url, patterns

urlpatterns = patterns(
    'management.views.report',
    url(r'^$', 'report_list', name = 'management_report_list'),
)

__author__ = 'edison7500'
