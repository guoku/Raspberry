# coding=utf8
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    pid = models.IntegerField(default = 0)
    title = models.CharField(max_length = 256)
    status = models.IntegerField(default = 1, db_index = True)

class Entity(models.Model):
    entity_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    creator = models.ForeignKey(User) 
    category = models.ForeignKey(Category)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    
    class Meta:
        ordering = ['-created_time']
 
