from django.conf.urls import url, patterns


urlpatterns = patterns(
    "seller.views",
    url(r'^commodities/$', 'commodities', name = 'seller_commodities'),
    url(r'^verify/$', 'verify', name = 'seller_verify'),
    url(r'^guokuprice/apply/$', 'apply_guoku_price', name = 'seller_apply_guoku_price'),
)
