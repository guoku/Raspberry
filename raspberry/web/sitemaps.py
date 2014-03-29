from django.contrib.sitemaps import Sitemap
from base.models import User, Entity, Entity_Tag, Neo_Category
from datetime import datetime


class UserSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.6

    def items(self):
        return User.objects.using('slave').all().order_by('-date_joined')

    def lastmod(self, obj):
        return obj.last_login

    def location(self, obj):
        return "/u/%s/" % obj.id

class EntitySitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    now = datetime.now()
    def items(self):
        return Entity.objects.using('slave').filter(updated_time__lte=self.now, weight__gte=0)

    def lastmod(self, obj):
        return obj.updated_time

    def location(self, obj):
        return  obj.get_absolute_url()

class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    now = datetime.now()

    def items(self):
        return Entity_Tag.objects.using('slave').filter(created_time__lte=self.now, count__gte=0)

    def lastmod(self, obj):
        return obj.last_tagged_time

    def location(self, obj):
        return  obj.get_absolute_url()

class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    # now = datetime.now()
    def items(self):
        return Neo_Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

__author__ = 'edison7500'
