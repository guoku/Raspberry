from django.conf.urls import url, patterns


urlpatterns = patterns(
    "seller.views",
    url(r'^commodities/$', 'commodities', name = 'commodities'),
)
