# coding=utf8
from django.contrib.auth.models import User
from django.db import models

class Category_Group(models.Model):
    title = models.CharField(max_length = 128, db_index = True)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']


class Category(models.Model):
    group = models.ForeignKey(Category_Group)
    title = models.CharField(max_length = 128, db_index = True)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']
 

class Entity(models.Model):
    entity_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    creator = models.ForeignKey(User) 
    category = models.ForeignKey(Category)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    
    class Meta:
        ordering = ['-created_time']
 
class Entity_Image(models.Model):
    entity = models.ForeignKey(Entity)
    image_url = models.URLField(max_length = 1024)
    is_chief = models.BooleanField(default = False)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)

