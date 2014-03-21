from django.contrib.sitemaps import Sitemap
from base.models import Entity, Tag
from datetime import datetime

class EntitySitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    now = datetime.now()
    def items(self):
        return Entity.objects.filter(updated_time__lte=self.now, weight__gte=0)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return  obj.get_absolute_url()

class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    now = datetime.now()

    def items(self):
        return Tag.objects.filter(updated_time__lte=self.now)

    def lastmod(self, obj):
        return obj.updated_time

    def location(self, obj):
        return  obj.get_absolute_url()

__author__ = 'edison7500'
