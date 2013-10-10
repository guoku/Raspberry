# coding=utf8
from django.contrib.auth.models import User
from django.db import models

class User_Profile(models.Model):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, u'男'),
        (Woman,  u'女'),
        (Other,  u'其他')
    )
    
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length = 64, db_index = True, unique = True)
    location = models.CharField(max_length = 32, null = True, default = u'北京')
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES, default = Other)
    bio = models.CharField(max_length = 1024, null = True, blank = True)
    website = models.CharField(max_length = 1024, null = True, blank = True)
    email_verified = models.BooleanField(default = False)

    def __unicode__(self):
        return self.nickname

class Category_Group(models.Model):
    title = models.CharField(max_length = 128, db_index = True)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']


class Category(models.Model):
    group = models.ForeignKey(Category_Group)
    title = models.CharField(max_length = 128, db_index = True, unique = True)
    status = models.IntegerField(default = 1, db_index = True)
    class Meta:
        ordering = ['id']
 

class Entity(models.Model):
    entity_id = models.CharField(max_length = 32, unique = True, db_index = True)
    entity_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    creator = models.ForeignKey(User) 
    category = models.ForeignKey(Category)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    class Meta:
        ordering = ['-created_time']
 
