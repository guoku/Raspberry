from django.conf.urls.defaults import *


urlpatterns = patterns("seller.views",
    (r"^commodities/$", "commodities")
)
