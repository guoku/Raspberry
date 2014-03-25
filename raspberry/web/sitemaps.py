from django.contrib.sitemaps import Sitemap
from base.models import Entity, Entity_Tag
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
        return Entity_Tag.objects.filter(created_time__lte=self.now, count__gte=0)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return  obj.get_absolute_url()

__author__ = 'edison7500'
