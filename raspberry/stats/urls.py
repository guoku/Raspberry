#encoding=utf8
__author__ = "shahuwang"

from django.conf.urls import patterns, url, include

urlpatterns = patterns("stats.stats",
    (r'^base/total/$', 'general_stat'),
    (r'^base/(.+)/$', 'feature_stat'),
)


