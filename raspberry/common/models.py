# coding=utf8
from django.contrib.auth.models import User
from django.db import models

class Entity(models.Model):
    entity_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    creator = models.ForeignKey(User) 
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    
